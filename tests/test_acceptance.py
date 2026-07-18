#!/usr/bin/env python3
"""Acceptance tests for the portable codex-policy installer."""

from __future__ import annotations

import hashlib
import json
import os
import fcntl
import shutil
import stat
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path
from typing import Dict, Optional, Sequence


sys.dont_write_bytecode = True
REPO = Path(__file__).resolve().parent.parent
SCRIPT = REPO / "bin" / "codex-policy"
GLOBAL_POLICY = REPO / "global" / "AGENTS.md"


def digest(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


class CodexPolicyAcceptance(unittest.TestCase):
    def setUp(self) -> None:
        self.scratch = Path(tempfile.mkdtemp(prefix="codex-policy-test-"))
        self.home = self.scratch / "codex-home"

    def tearDown(self) -> None:
        shutil.rmtree(self.scratch)

    def run_policy(
        self,
        *arguments: str,
        home: Optional[Path] = None,
        extra_environment: Optional[Dict[str, str]] = None,
    ) -> subprocess.CompletedProcess[str]:
        environment = os.environ.copy()
        environment["CODEX_HOME"] = str(home if home is not None else self.home)
        environment["PYTHONDONTWRITEBYTECODE"] = "1"
        if extra_environment:
            environment.update(extra_environment)
        return subprocess.run(
            [sys.executable, str(SCRIPT)] + list(arguments),
            cwd=str(REPO),
            env=environment,
            text=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            check=False,
        )

    def assert_sanitized(self, result: subprocess.CompletedProcess[str]) -> None:
        combined = result.stdout + result.stderr
        self.assertNotIn(str(self.scratch), combined)
        self.assertNotIn(str(self.home), combined)

    def transaction_directories(self) -> Sequence[Path]:
        root = self.home / ".codex-policy" / "transactions"
        return sorted(root.iterdir()) if root.exists() else []

    def test_default_plan_is_read_only(self) -> None:
        self.assertFalse(self.home.exists())
        result = self.run_policy()
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertIn("codex-policy plan", result.stdout)
        self.assertFalse(self.home.exists())
        self.assert_sanitized(result)

    def test_empty_home_install_verify_and_idempotence(self) -> None:
        result = self.run_policy("apply", "--yes")
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertEqual((self.home / "AGENTS.md").read_bytes(), GLOBAL_POLICY.read_bytes())
        config = (self.home / "config.toml").read_text(encoding="utf-8")
        self.assertIn("max_threads = 6", config)
        self.assertIn("max_depth = 1", config)
        self.assertIn("job_max_runtime_seconds = 1800", config)
        self.assertEqual(stat.S_IMODE((self.home / "config.toml").stat().st_mode), 0o600)
        self.assertEqual(stat.S_IMODE((self.home / "AGENTS.md").stat().st_mode), 0o644)
        verify = self.run_policy("verify", "--json")
        self.assertEqual(verify.returncode, 0, verify.stderr)
        self.assertEqual(json.loads(verify.stdout)["verified"], "passed")
        transactions = self.transaction_directories()
        self.assertEqual(len(transactions), 1)
        before = (self.home / "config.toml").read_bytes()
        second = self.run_policy("apply", "--yes")
        self.assertEqual(second.returncode, 0, second.stderr)
        self.assertIn("result: none", second.stdout)
        self.assertEqual((self.home / "config.toml").read_bytes(), before)
        self.assertEqual(self.transaction_directories(), transactions)

    def test_unowned_toml_text_and_semantics_are_preserved(self) -> None:
        self.home.mkdir(mode=0o700)
        original = (
            '# retained root comment\n'
            'model    = "example-model" # retained spacing\n'
            'message = """\n'
            '[this.is.text]\n'
            '"""\n'
            'items = [{ name = "one", enabled = true }]\n'
            '\n'
            '[custom.dotted]\n'
            'answer = 42 # retained value\n'
            '\n'
            '[agents]\n'
            'max_threads  = 2 # owned comment retained\n'
            'unowned = "keep"\n'
            '\n'
            '[mcp_servers.example]\n'
            'url = "https://example.invalid/mcp"\n'
            '\n'
            '[mcp_servers.openaiDeveloperDocs]\n'
            'url = "https://private.invalid/mcp"\n'
            'bearer_token_env_var = "PRIVATE_TOKEN"\n'
            'enabled = false\n'
        ).encode("utf-8")
        (self.home / "config.toml").write_bytes(original)
        (self.home / "AGENTS.md").write_text("old policy\n", encoding="utf-8")
        result = self.run_policy("apply", "--yes")
        self.assertEqual(result.returncode, 0, result.stderr)
        updated = (self.home / "config.toml").read_text(encoding="utf-8")
        for retained in (
            '# retained root comment',
            'model    = "example-model" # retained spacing',
            '[this.is.text]',
            'items = [{ name = "one", enabled = true }]',
            '[custom.dotted]',
            'answer = 42 # retained value',
            'unowned = "keep"',
            '[mcp_servers.example]',
            'url = "https://example.invalid/mcp"',
            '[mcp_servers.openaiDeveloperDocs]',
            'url = "https://private.invalid/mcp"',
            'bearer_token_env_var = "PRIVATE_TOKEN"',
            'enabled = false',
            'max_threads  = 6 # owned comment retained',
        ):
            self.assertIn(retained, updated)
        first = updated.encode("utf-8")
        second = self.run_policy("apply", "--yes")
        self.assertEqual(second.returncode, 0, second.stderr)
        self.assertEqual((self.home / "config.toml").read_bytes(), first)

    def test_private_values_and_paths_never_reach_output(self) -> None:
        self.home.mkdir(mode=0o700)
        canary = "sk-" + "A" * 24
        config = 'private_note = "{}"\n'.format(canary)
        (self.home / "config.toml").write_text(config, encoding="utf-8")
        result = self.run_policy("plan", "--json")
        self.assertEqual(result.returncode, 0, result.stderr)
        combined = result.stdout + result.stderr
        self.assertNotIn(canary, combined)
        self.assert_sanitized(result)
        override = self.home / "AGENTS.override.md"
        override.write_text(canary + "\n", encoding="utf-8")
        blocked = self.run_policy("apply", "--yes")
        self.assertEqual(blocked.returncode, 2)
        self.assertNotIn(canary, blocked.stdout + blocked.stderr)
        self.assertEqual((self.home / "config.toml").read_text(encoding="utf-8"), config)

    def test_invalid_toml_fails_without_writes(self) -> None:
        self.home.mkdir(mode=0o700)
        invalid = b"[broken\nvalue = 1\n"
        (self.home / "config.toml").write_bytes(invalid)
        result = self.run_policy("apply", "--yes")
        self.assertEqual(result.returncode, 2)
        self.assertEqual((self.home / "config.toml").read_bytes(), invalid)
        self.assertFalse((self.home / "AGENTS.md").exists())
        self.assertFalse((self.home / ".codex-policy").exists())
        self.assert_sanitized(result)

    @unittest.skipIf(os.name == "nt", "symlink behavior differs on Windows")
    def test_symlink_target_is_rejected(self) -> None:
        self.home.mkdir(mode=0o700)
        outside = self.scratch / "outside.toml"
        outside.write_text("safe = true\n", encoding="utf-8")
        (self.home / "config.toml").symlink_to(outside)
        result = self.run_policy("apply", "--yes")
        self.assertEqual(result.returncode, 2)
        self.assertEqual(outside.read_text(encoding="utf-8"), "safe = true\n")
        self.assertFalse((self.home / "AGENTS.md").exists())

    @unittest.skipIf(os.name == "nt", "symlink behavior differs on Windows")
    def test_symlinked_transaction_state_is_rejected(self) -> None:
        self.home.mkdir(mode=0o700)
        outside = self.scratch / "outside-state"
        outside.mkdir()
        (self.home / ".codex-policy").symlink_to(outside, target_is_directory=True)
        result = self.run_policy("apply", "--yes")
        self.assertEqual(result.returncode, 2)
        self.assertEqual(list(outside.iterdir()), [])
        self.assertFalse((self.home / "AGENTS.md").exists())

    def test_injected_failure_restores_exact_originals(self) -> None:
        self.home.mkdir(mode=0o700)
        old_policy = b"old global policy\n"
        old_config = b'model = "unchanged"\n'
        (self.home / "AGENTS.md").write_bytes(old_policy)
        (self.home / "config.toml").write_bytes(old_config)
        result = self.run_policy(
            "apply",
            "--yes",
            extra_environment={"CODEX_POLICY_TEST_FAIL_AFTER": "1"},
        )
        self.assertEqual(result.returncode, 2)
        self.assertEqual((self.home / "AGENTS.md").read_bytes(), old_policy)
        self.assertEqual((self.home / "config.toml").read_bytes(), old_config)
        preview = self.run_policy("recover")
        self.assertEqual(preview.returncode, 0, preview.stderr)
        self.assertIn("result: none", preview.stdout)

    def test_interrupted_transaction_recovery(self) -> None:
        self.home.mkdir(mode=0o700)
        before = b"pre-transaction policy\n"
        after = GLOBAL_POLICY.read_bytes()
        (self.home / "AGENTS.md").write_bytes(after)
        transaction = self.home / ".codex-policy" / "transactions" / "fixture"
        transaction.mkdir(parents=True, mode=0o700)
        (transaction / "AGENTS.md.before").write_bytes(before)
        journal = {
            "schema": 1,
            "kind": "apply",
            "state": "applying",
            "files": {
                "AGENTS.md": {
                    "before_present": True,
                    "before_sha256": digest(before),
                    "after_sha256": digest(after),
                    "mode": 0o644,
                }
            },
            "replaced": [],
        }
        (transaction / "state.json").write_text(json.dumps(journal), encoding="utf-8")
        (self.home / ".codex-policy.lock").write_text("stale\n", encoding="utf-8")
        preview = self.run_policy("recover")
        self.assertEqual(preview.returncode, 0, preview.stderr)
        self.assertIn("required", preview.stdout)
        self.assertEqual((self.home / "AGENTS.md").read_bytes(), after)
        recovered = self.run_policy("recover", "--apply", "--yes")
        self.assertEqual(recovered.returncode, 0, recovered.stderr)
        self.assertEqual((self.home / "AGENTS.md").read_bytes(), before)
        state = json.loads((transaction / "state.json").read_text(encoding="utf-8"))
        self.assertEqual(state["state"], "recovered")

    def test_live_advisory_lock_blocks_concurrent_apply(self) -> None:
        self.home.mkdir(mode=0o700)
        lock_path = self.home / ".codex-policy.lock"
        with lock_path.open("w", encoding="utf-8") as handle:
            fcntl.flock(handle.fileno(), fcntl.LOCK_EX | fcntl.LOCK_NB)
            result = self.run_policy("apply", "--yes")
            self.assertEqual(result.returncode, 2)
            self.assertIn("holds the update lock", result.stderr)
            self.assertFalse((self.home / "AGENTS.md").exists())

    def test_normal_clone_origin_allowlist_is_exact(self) -> None:
        source = self.scratch / "source"
        shutil.copytree(REPO, source, ignore=shutil.ignore_patterns(".git", "__pycache__"))
        subprocess.run(["git", "init", "-b", "main"], cwd=str(source), check=True, stdout=subprocess.DEVNULL)
        subprocess.run(["git", "config", "user.name", "fixture"], cwd=str(source), check=True)
        fixture_email = "fixture" + "@" + "example.invalid"
        subprocess.run(["git", "config", "user.email", fixture_email], cwd=str(source), check=True)
        subprocess.run(["git", "add", "--all"], cwd=str(source), check=True)
        subprocess.run(["git", "commit", "-m", "Fixture"], cwd=str(source), check=True, stdout=subprocess.DEVNULL)
        remote = self.scratch / "remote.git"
        clone = self.scratch / "clone"
        subprocess.run(
            ["git", "clone", "--bare", str(source), str(remote)],
            check=True,
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
        )
        subprocess.run(
            ["git", "clone", str(remote), str(clone)],
            check=True,
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
        )
        for allowed_origin in (
            "https://github.com/taekimax/codex-policy",
            "git@github.com:taekimax/codex-policy.git",
        ):
            subprocess.run(
                ["git", "remote", "set-url", "origin", allowed_origin],
                cwd=str(clone),
                check=True,
            )
            result = subprocess.run(
                [sys.executable, str(clone / "bin" / "codex-policy"), "audit-repo"],
                cwd=str(clone),
                env={**os.environ, "PYTHONDONTWRITEBYTECODE": "1"},
                text=True,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                check=False,
            )
            self.assertEqual(result.returncode, 0, result.stderr)
            self.assertEqual(result.stdout.strip(), "repository audit: passed")

        subprocess.run(
            ["git", "remote", "set-url", "origin", "https://github.com/taekimax/codex-policy.git"],
            cwd=str(clone),
            check=True,
        )
        rejected = subprocess.run(
            [sys.executable, str(clone / "bin" / "codex-policy"), "audit-repo"],
            cwd=str(clone),
            env={**os.environ, "PYTHONDONTWRITEBYTECODE": "1"},
            text=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            check=False,
        )
        self.assertEqual(rejected.returncode, 2)
        self.assertIn("unexpected origin URL", rejected.stderr)

        subprocess.run(["git", "remote", "remove", "origin"], cwd=str(clone), check=True)
        missing = subprocess.run(
            [sys.executable, str(clone / "bin" / "codex-policy"), "audit-repo"],
            cwd=str(clone),
            env={**os.environ, "PYTHONDONTWRITEBYTECODE": "1"},
            text=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            check=False,
        )
        self.assertEqual(missing.returncode, 2)
        self.assertIn("unexpected Git remote", missing.stderr)

        subprocess.run(
            ["git", "remote", "add", "origin", "https://github.com/taekimax/codex-policy"],
            cwd=str(clone),
            check=True,
        )
        subprocess.run(
            ["git", "remote", "set-url", "--add", "--push", "origin", "https://example.invalid/codex-policy"],
            cwd=str(clone),
            check=True,
        )
        push_override = subprocess.run(
            [sys.executable, str(clone / "bin" / "codex-policy"), "audit-repo"],
            cwd=str(clone),
            env={**os.environ, "PYTHONDONTWRITEBYTECODE": "1"},
            text=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            check=False,
        )
        self.assertEqual(push_override.returncode, 2)
        self.assertIn("unexpected origin push URL", push_override.stderr)

        subprocess.run(
            ["git", "config", "--unset-all", "remote.origin.pushurl"],
            cwd=str(clone),
            check=True,
        )
        subprocess.run(
            ["git", "remote", "set-url", "--add", "origin", "git@github.com:taekimax/codex-policy.git"],
            cwd=str(clone),
            check=True,
        )
        multiple_fetch_urls = subprocess.run(
            [sys.executable, str(clone / "bin" / "codex-policy"), "audit-repo"],
            cwd=str(clone),
            env={**os.environ, "PYTHONDONTWRITEBYTECODE": "1"},
            text=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            check=False,
        )
        self.assertEqual(multiple_fetch_urls.returncode, 2)
        self.assertIn("unexpected origin URL", multiple_fetch_urls.stderr)

    def test_write_commands_require_explicit_confirmation(self) -> None:
        result = self.run_policy("apply")
        self.assertEqual(result.returncode, 2)
        self.assertFalse(self.home.exists())
        recover = self.run_policy("recover", "--apply")
        self.assertEqual(recover.returncode, 2)
        self.assertFalse(self.home.exists())

    def test_repository_audit_and_reviewed_policy_hash(self) -> None:
        result = self.run_policy("audit-repo")
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertEqual(result.stdout.strip(), "repository audit: passed")
        self.assertEqual(
            digest(GLOBAL_POLICY.read_bytes()),
            "9f1521c1aedbcbd7342e940e662c39c078cf297371b37ac326984d5eee3f23db",
        )


if __name__ == "__main__":
    unittest.main(verbosity=2)
