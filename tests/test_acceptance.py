#!/usr/bin/env python3
"""Acceptance tests for the portable codex-policy installer."""

from __future__ import annotations

import hashlib
import io
import json
import os
import fcntl
import runpy
import shutil
import stat
import subprocess
import sys
import tempfile
import unittest
from contextlib import redirect_stdout
from unittest import mock
from pathlib import Path
from typing import Dict, Optional, Sequence


sys.dont_write_bytecode = True
REPO = Path(__file__).resolve().parent.parent
SCRIPT = REPO / "bin" / "codex-policy"
SKILLS_SCRIPT = REPO / "bin" / "codex-skills-policy"
GLOBAL_POLICY = REPO / "global" / "AGENTS.md"
OFFICIAL_SKILLS = REPO / "global" / "official-skills.json"
ORACLE_SKILL = REPO / "global" / "skills" / "oracle-solver"
ORACLE_FILES = ("SKILL.md", "agents/openai.yaml", "scripts/run_oracle.py")
REQUIRED_PLUGIN_SKILLS = {
    "documents@openai-primary-runtime": {"documents"},
    "pdf@openai-primary-runtime": {"pdf"},
    "spreadsheets@openai-primary-runtime": {"spreadsheets", "excel-live-control"},
    "presentations@openai-primary-runtime": {"presentations"},
    "template-creator@openai-primary-runtime": {"template-creator"},
    "sites@openai-bundled": {"sites-building", "sites-hosting"},
    "browser@openai-bundled": {"control-in-app-browser"},
    "chrome@openai-bundled": {"control-chrome"},
    "computer-use@openai-bundled": {"computer-use"},
    "visualize@openai-bundled": {"visualize"},
}


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

    def make_fake_codex(self, installed: Sequence[Dict[str, object]]) -> Dict[str, str]:
        fake_bin = self.scratch / "fake-bin"
        fake_bin.mkdir()
        state = self.scratch / "plugin-state.json"
        state.write_text(json.dumps({"installed": list(installed)}), encoding="utf-8")
        executable = fake_bin / "codex"
        executable.write_text(
            """#!/usr/bin/env python3
import json
import os
import sys

state_path = os.environ["CODEX_FAKE_STATE"]
with open(state_path, encoding="utf-8") as handle:
    state = json.load(handle)
args = sys.argv[1:]
if args == ["plugin", "list", "--json"]:
    print(json.dumps(state))
    raise SystemExit(0)
if len(args) >= 4 and args[0] == "plugin" and args[1] in {"add", "remove"} and args[-1] == "--json":
    action, plugin_id = args[1], args[2]
    state["installed"] = [item for item in state["installed"] if item["pluginId"] != plugin_id]
    if action == "add":
        name, marketplace = plugin_id.split("@", 1)
        state["installed"].append({
            "pluginId": plugin_id,
            "enabled": True,
            "version": os.environ.get("CODEX_FAKE_ADD_VERSION", "fixture-v1"),
            "source": {"source": "local", "path": os.path.join(os.environ["CODEX_FAKE_SOURCES"], name)},
        })
    if os.environ.get("CODEX_FAKE_MUTATE_CONFIG") == "1":
        config = os.path.join(os.environ["CODEX_HOME"], "config.toml")
        with open(config, "a", encoding="utf-8") as handle:
            handle.write("# fake plugin mutation " + action + " " + plugin_id + "\\n")
    concurrent_edit = os.environ.get("CODEX_FAKE_CONCURRENT_EDIT")
    if concurrent_edit:
        config = os.path.join(os.environ["CODEX_HOME"], "config.toml")
        with open(config, "a", encoding="utf-8") as handle:
            handle.write(concurrent_edit + "\\n")
    failure = os.environ.get("CODEX_FAKE_FAIL_COMMAND")
    command_key = action + ":" + plugin_id
    failed = state.setdefault("failed_commands", [])
    should_fail = failure == command_key and command_key not in failed
    if should_fail:
        failed.append(command_key)
    with open(state_path, "w", encoding="utf-8") as handle:
        json.dump(state, handle)
    if should_fail:
        raise SystemExit(1)
    print("{}")
    raise SystemExit(0)
raise SystemExit(2)
""",
            encoding="utf-8",
        )
        executable.chmod(0o755)
        sources = self.scratch / "plugin-sources"
        sources.mkdir()
        return {
            "PATH": str(fake_bin) + os.pathsep + os.environ.get("PATH", ""),
            "HOME": str(self.scratch / "user-home"),
            "CODEX_FAKE_STATE": str(state),
            "CODEX_FAKE_SOURCES": str(sources),
        }

    def run_skills_policy(
        self,
        *arguments: str,
        extra_environment: Optional[Dict[str, str]] = None,
    ) -> subprocess.CompletedProcess[str]:
        environment = os.environ.copy()
        environment["CODEX_HOME"] = str(self.home)
        environment["PYTHONDONTWRITEBYTECODE"] = "1"
        if extra_environment:
            environment.update(extra_environment)
        return subprocess.run(
            [sys.executable, str(SKILLS_SCRIPT)] + list(arguments),
            cwd=str(REPO),
            env=environment,
            text=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            check=False,
        )

    @staticmethod
    def plugin_record(
        plugin_id: str,
        source: Path,
        *,
        version: str = "fixture-v1",
        enabled: bool = True,
        source_kind: str = "local",
    ) -> Dict[str, object]:
        return {
            "pluginId": plugin_id,
            "enabled": enabled,
            "version": version,
            "source": {"source": source_kind, "path": str(source)},
        }

    @staticmethod
    def write_skill(path: Path) -> None:
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text("---\nname: fixture\ndescription: fixture\n---\n", encoding="utf-8")

    def write_required_plugin_skills(self, sources: Path) -> None:
        for plugin_id, skills in REQUIRED_PLUGIN_SKILLS.items():
            plugin = plugin_id.split("@", 1)[0]
            for skill in skills:
                self.write_skill(sources / plugin / "skills" / skill / "SKILL.md")

    def required_plugin_records(self, sources: Path) -> Sequence[Dict[str, object]]:
        return [self.plugin_record(plugin_id, sources / plugin_id.split("@", 1)[0]) for plugin_id in REQUIRED_PLUGIN_SKILLS]

    def write_system_skills(self) -> None:
        for skill in ("imagegen", "openai-docs", "plugin-creator", "skill-creator", "skill-installer"):
            self.write_skill(self.home / "skills" / ".system" / skill / "SKILL.md")

    def write_current_context7(self) -> None:
        skill = self.home / "skills" / "context7-cli" / "SKILL.md"
        skill.parent.mkdir(parents=True, exist_ok=True)
        skill.write_text(
            "---\nname: context7-cli\n"
            "description: Fetch docs. Use only when the user explicitly mentions ctx7 or Context7, "
            "or explicitly invokes $context7-cli. Do not trigger for generic library-documentation questions.\n"
            "---\n",
            encoding="utf-8",
        )
        policy = skill.parent / "agents" / "openai.yaml"
        policy.parent.mkdir(parents=True, exist_ok=True)
        policy.write_text("policy:\n  allow_implicit_invocation: true\n", encoding="utf-8")

    def write_current_oracle(self) -> None:
        target = self.home / "skills" / "oracle-solver"
        for relative in ORACLE_FILES:
            destination = target / relative
            destination.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(ORACLE_SKILL / relative, destination)

    def make_current_skills_environment(
        self,
        extra_installed: Sequence[Dict[str, object]] = (),
    ) -> Dict[str, str]:
        sources = self.scratch / "plugin-sources"
        installed = list(self.required_plugin_records(sources)) + list(extra_installed)
        environment = self.make_fake_codex(installed)
        self.write_required_plugin_skills(sources)
        self.write_system_skills()
        return environment

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

    def test_official_skills_plan_apply_verify_and_idempotence(self) -> None:
        sources = self.scratch / "plugin-sources"
        installed = [
            self.plugin_record("documents@openai-primary-runtime", sources / "documents"),
            self.plugin_record("presentations@openai-primary-runtime", sources / "presentations"),
            self.plugin_record("template-creator@openai-primary-runtime", sources / "template-creator"),
            self.plugin_record("canva@openai-curated", sources / "canva"),
            self.plugin_record("game-studio@openai-curated", sources / "game-studio"),
            self.plugin_record("github@openai-curated", sources / "github"),
        ]
        environment = self.make_fake_codex(installed)
        self.write_required_plugin_skills(sources)
        self.write_system_skills()
        for skill in (
            "canva-branded-presentation",
            "canva-resize-for-all-social-media",
            "canva-translate-design",
        ):
            self.write_skill(
                self.home / "plugins" / "cache" / "openai-curated-remote" / "canva" / "9.0.0" / "skills" / skill / "SKILL.md"
            )
        for skill in ("gmail", "gmail-inbox-triage"):
            self.write_skill(
                self.home / "plugins" / "cache" / "openai-curated-remote" / "gmail" / "0.1.5" / "skills" / skill / "SKILL.md"
            )
        for skill in ("gh-address-comments", "gh-fix-ci", "github", "yeet"):
            self.write_skill(
                self.home / "plugins" / "cache" / "openai-curated-remote" / "github" / "0.1.8" / "skills" / skill / "SKILL.md"
            )
        for skill in ("google-drive", "google-docs", "google-drive-comments", "google-sheets", "google-slides"):
            self.write_skill(
                self.home / "plugins" / "cache" / "openai-curated-remote" / "google-drive" / "0.1.10" / "skills" / skill / "SKILL.md"
            )
        for skill in (
            "slack", "slack-channel-summarization", "slack-daily-digest",
            "slack-notification-triage", "slack-outgoing-message", "slack-reply-drafting",
        ):
            self.write_skill(
                self.home / "plugins" / "cache" / "openai-curated-remote" / "slack" / "0.1.4" / "skills" / skill / "SKILL.md"
            )
        for skill in ("find-skills", "web-design-guidelines"):
            self.write_skill(Path(environment["HOME"]) / ".agents" / "skills" / skill / "SKILL.md")
        self.write_current_context7()
        self.write_current_oracle()
        self.home.mkdir(parents=True, exist_ok=True)
        stale = self.home / "plugins" / "cache" / "openai-curated-remote" / "canva" / "9.0.0" / "skills" / "canva-branded-presentation" / "SKILL.md"
        unrelated = self.scratch / "unrelated" / "SKILL.md"
        self.home.joinpath("config.toml").write_text(
            'model    = "keep-me" # preserve formatting\n'
            '\n'
            '[[skills.config]]\n'
            'path = "{}"\n'
            'enabled = true\n'
            '\n'
            '[[skills.config]]\n'
            'path = "{}"\n'
            'enabled = true\n'.format(unrelated, stale),
            encoding="utf-8",
        )

        plan = self.run_skills_policy("plan", "--json", extra_environment=environment)
        self.assertEqual(plan.returncode, 0, plan.stderr)
        self.assertEqual(json.loads(plan.stdout)["action"], "update")
        self.assertEqual(json.loads(plan.stdout)["connector_skills"], "current")
        self.assert_sanitized(plan)

        applied = self.run_skills_policy("apply", "--yes", extra_environment=environment)
        self.assertEqual(applied.returncode, 0, applied.stderr)
        self.assertIn("result: updated", applied.stdout)
        config = self.home.joinpath("config.toml").read_text(encoding="utf-8")
        self.assertIn('model    = "keep-me" # preserve formatting', config)
        self.assertIn(str(unrelated), config)
        self.assertEqual(config.count("enabled = false"), 19)
        state = json.loads(Path(environment["CODEX_FAKE_STATE"]).read_text(encoding="utf-8"))
        plugin_ids = {item["pluginId"] for item in state["installed"]}
        required = {
            "documents@openai-primary-runtime", "pdf@openai-primary-runtime",
            "spreadsheets@openai-primary-runtime", "presentations@openai-primary-runtime",
            "template-creator@openai-primary-runtime", "sites@openai-bundled",
            "browser@openai-bundled", "chrome@openai-bundled", "computer-use@openai-bundled",
            "visualize@openai-bundled",
        }
        self.assertTrue(required.issubset(plugin_ids))
        self.assertFalse(
            plugin_ids.intersection(
                {"canva@openai-curated", "game-studio@openai-curated", "github@openai-curated"}
            )
        )

        verified = self.run_skills_policy("verify", "--json", extra_environment=environment)
        self.assertEqual(verified.returncode, 0, verified.stderr)
        self.assertEqual(json.loads(verified.stdout)["verified"], "passed")
        before = self.home.joinpath("config.toml").read_bytes()
        second = self.run_skills_policy("apply", "--yes", extra_environment=environment)
        self.assertEqual(second.returncode, 0, second.stderr)
        self.assertIn("result: none", second.stdout)
        self.assertEqual(self.home.joinpath("config.toml").read_bytes(), before)

    def test_official_skills_preserves_unresolved_tombstones(self) -> None:
        environment = self.make_current_skills_environment()
        user_tombstone = Path(environment["HOME"]) / ".agents" / "skills" / "find-skills" / "SKILL.md"
        connector_tombstone = (
            self.home / "plugins" / "cache" / "openai-curated-remote" / "canva" / "old"
            / "skills" / "canva-branded-presentation" / "SKILL.md"
        )
        original = (
            'model = "preserved"\n\n'
            '[[skills.config]]\npath = "{}"\nenabled = false\n\n'
            '[[skills.config]]\npath = "{}"\nenabled = false\n'.format(user_tombstone, connector_tombstone)
        ).encode("utf-8")
        self.home.joinpath("config.toml").write_bytes(original)

        applied = self.run_skills_policy("apply", "--yes", extra_environment=environment)
        self.assertEqual(applied.returncode, 0, applied.stderr)
        updated = self.home.joinpath("config.toml").read_text(encoding="utf-8")
        self.assertIn(str(user_tombstone), updated)
        self.assertIn(str(connector_tombstone), updated)
        self.assertEqual(updated.count("enabled = false"), 5)
        verified = self.run_skills_policy("verify", "--json", extra_environment=environment)
        self.assertEqual(verified.returncode, 0, verified.stderr)

    def test_official_skills_disables_retired_codex_home_skills_and_survives_removal(self) -> None:
        environment = self.make_current_skills_environment()
        retired = ("code-auditor", "feature-implementing", "test-fixing")
        paths = []
        for skill in retired:
            path = self.home / "skills" / skill / "SKILL.md"
            self.write_skill(path)
            paths.append(path)

        applied = self.run_skills_policy("apply", "--yes", extra_environment=environment)
        self.assertEqual(applied.returncode, 0, applied.stderr)
        config = self.home.joinpath("config.toml").read_text(encoding="utf-8")
        for path in paths:
            self.assertIn(str(path), config)
        self.assertEqual(config.count("enabled = false"), 6)

        for path in paths:
            path.unlink()
            path.parent.rmdir()

        verified = self.run_skills_policy("verify", "--json", extra_environment=environment)
        self.assertEqual(verified.returncode, 0, verified.stderr)
        self.assertEqual(json.loads(verified.stdout)["verified"], "passed")
        second = self.run_skills_policy("apply", "--yes", extra_environment=environment)
        self.assertEqual(second.returncode, 0, second.stderr)
        self.assertIn("result: none", second.stdout)

    def test_official_skills_accepts_current_global_setting_shape(self) -> None:
        environment = self.make_current_skills_environment()
        connector_root = self.home / "plugins" / "cache" / "openai-curated-remote"
        github_skill = connector_root / "github" / "0.1.8" / "skills" / "yeet" / "SKILL.md"
        gmail_skill = connector_root / "gmail" / "0.1.5" / "skills" / "gmail" / "SKILL.md"
        self.write_skill(github_skill)
        self.write_skill(gmail_skill)
        for skill in ("google-drive", "google-docs", "google-drive-comments", "google-sheets", "google-slides"):
            self.write_skill(connector_root / "google-drive" / "0.1.10" / "skills" / skill / "SKILL.md")
        (connector_root / "slack" / "0.1.4" / "skills").mkdir(parents=True)
        shared_skills = Path(environment["HOME"]) / ".agents" / "skills"
        for skill in ("find-skills", "web-design-guidelines"):
            self.write_skill(shared_skills / skill / "SKILL.md")
        self.write_current_context7()
        self.write_current_oracle()

        sources = Path(environment["CODEX_FAKE_SOURCES"])
        configured = [
            sources / "documents" / "skills" / "documents" / "SKILL.md",
            sources / "presentations" / "skills" / "presentations" / "SKILL.md",
            sources / "template-creator" / "skills" / "template-creator" / "SKILL.md",
            connector_root / "canva" / "removed" / "skills" / "canva-branded-presentation" / "SKILL.md",
            connector_root / "canva" / "removed" / "skills" / "canva-resize-for-all-social-media" / "SKILL.md",
            connector_root / "canva" / "removed" / "skills" / "canva-translate-design" / "SKILL.md",
            gmail_skill,
            shared_skills / "find-skills" / "SKILL.md",
            shared_skills / "web-design-guidelines" / "SKILL.md",
        ]
        original = "".join(
            '[[skills.config]]\npath = "{}"\nenabled = false\n\n'.format(path)
            for path in configured
        ).encode("utf-8")
        self.home.joinpath("config.toml").write_bytes(original)

        plan = self.run_skills_policy("plan", "--json", extra_environment=environment)
        self.assertEqual(plan.returncode, 0, plan.stderr)
        payload = json.loads(plan.stdout)
        self.assertEqual(payload["action"], "none")
        self.assertEqual(payload["connector_skills"], "not_present")
        self.assertEqual(payload["skill_disables"], "current")
        self.assertEqual(self.home.joinpath("config.toml").read_bytes(), original)
        verified = self.run_skills_policy("verify", "--json", extra_environment=environment)
        self.assertEqual(verified.returncode, 0, verified.stderr)

    def test_official_skills_blocks_unsafe_required_plugin_without_replacing_tombstone(self) -> None:
        sources = self.scratch / "plugin-sources"
        records = list(self.required_plugin_records(sources))
        records = [
            self.plugin_record(item["pluginId"], Path(item["source"]["path"]), source_kind="remote")
            if item["pluginId"] == "documents@openai-primary-runtime" else item
            for item in records
        ]
        environment = self.make_fake_codex(records)
        self.write_required_plugin_skills(sources)
        self.write_system_skills()
        tombstone = self.home / "plugins" / "cache" / "openai-primary-runtime" / "documents" / "old" / "skills" / "documents" / "SKILL.md"
        original = '[[skills.config]]\npath = "{}"\nenabled = false\n'.format(tombstone).encode("utf-8")
        self.home.joinpath("config.toml").write_bytes(original)

        plan = self.run_skills_policy("plan", "--json", extra_environment=environment)
        self.assertEqual(plan.returncode, 0, plan.stderr)
        self.assertEqual(json.loads(plan.stdout)["action"], "blocked")
        applied = self.run_skills_policy("apply", "--yes", extra_environment=environment)
        self.assertEqual(applied.returncode, 2)
        self.assertEqual(self.home.joinpath("config.toml").read_bytes(), original)

    def test_official_skills_blocks_missing_required_skill_file(self) -> None:
        environment = self.make_current_skills_environment()
        missing = Path(environment["CODEX_FAKE_SOURCES"]) / "documents" / "skills" / "documents" / "SKILL.md"
        missing.unlink()
        tombstone = self.home / "plugins" / "cache" / "openai-primary-runtime" / "documents" / "old" / "skills" / "documents" / "SKILL.md"
        original = '[[skills.config]]\npath = "{}"\nenabled = false\n'.format(tombstone).encode("utf-8")
        self.home.joinpath("config.toml").write_bytes(original)
        plan = self.run_skills_policy("plan", "--json", extra_environment=environment)
        self.assertEqual(plan.returncode, 0, plan.stderr)
        self.assertEqual(json.loads(plan.stdout)["action"], "blocked")
        self.assertEqual(self.home.joinpath("config.toml").read_bytes(), original)

    def test_official_skills_blocks_extra_required_plugin_skill(self) -> None:
        environment = self.make_current_skills_environment()
        extra = Path(environment["CODEX_FAKE_SOURCES"]) / "documents" / "skills" / "unreviewed-extra" / "SKILL.md"
        self.write_skill(extra)
        verify = self.run_skills_policy("verify", "--json", extra_environment=environment)
        self.assertEqual(verify.returncode, 1, verify.stderr)
        self.assertEqual(json.loads(verify.stdout)["action"], "blocked")

    def test_official_skills_blocks_unresolved_enabled_user_tombstone(self) -> None:
        environment = self.make_current_skills_environment()
        tombstone = Path(environment["HOME"]) / ".agents" / "skills" / "find-skills" / "SKILL.md"
        original = '[[skills.config]]\npath = "{}"\nenabled = true\n'.format(tombstone).encode("utf-8")
        self.home.joinpath("config.toml").write_bytes(original)
        verify = self.run_skills_policy("verify", "--json", extra_environment=environment)
        self.assertEqual(verify.returncode, 1, verify.stderr)
        self.assertEqual(json.loads(verify.stdout)["action"], "blocked")
        applied = self.run_skills_policy("apply", "--yes", extra_environment=environment)
        self.assertEqual(applied.returncode, 2)
        self.assertEqual(self.home.joinpath("config.toml").read_bytes(), original)

    def test_official_skills_blocks_unresolved_enabled_connector_tombstone(self) -> None:
        environment = self.make_current_skills_environment()
        tombstone = (
            self.home / "plugins" / "cache" / "openai-curated-remote" / "gmail" / "old"
            / "skills" / "gmail" / "SKILL.md"
        )
        original = '[[skills.config]]\npath = "{}"\nenabled = true\n'.format(tombstone).encode("utf-8")
        self.home.joinpath("config.toml").write_bytes(original)
        verify = self.run_skills_policy("verify", "--json", extra_environment=environment)
        self.assertEqual(verify.returncode, 1, verify.stderr)
        self.assertEqual(json.loads(verify.stdout)["action"], "blocked")
        self.assertEqual(self.home.joinpath("config.toml").read_bytes(), original)

    def test_official_skills_blocks_unsafe_connector_skill_sets(self) -> None:
        environment = self.make_current_skills_environment()
        github = self.home / "plugins" / "cache" / "openai-curated-remote" / "github"
        github_skills = github / "0.1.8" / "skills"
        for skill in ("gh-address-comments", "gh-fix-ci", "github"):
            self.write_skill(github_skills / skill / "SKILL.md")
        missing_active = self.run_skills_policy("verify", "--json", extra_environment=environment)
        self.assertEqual(missing_active.returncode, 1, missing_active.stderr)
        self.assertEqual(json.loads(missing_active.stdout)["connector_skills"], "review")

        shutil.rmtree(github)
        canva_skills = (
            self.home / "plugins" / "cache" / "openai-curated-remote" / "canva" / "9.0.0" / "skills"
        )
        for skill in (
            "canva-branded-presentation",
            "canva-resize-for-all-social-media",
            "canva-translate-design",
            "unreviewed-extra",
        ):
            self.write_skill(canva_skills / skill / "SKILL.md")
        unreviewed = self.run_skills_policy("verify", "--json", extra_environment=environment)
        self.assertEqual(unreviewed.returncode, 1, unreviewed.stderr)
        self.assertEqual(json.loads(unreviewed.stdout)["connector_skills"], "review")

    def test_official_skills_preserves_unrelated_cache_like_path(self) -> None:
        environment = self.make_current_skills_environment()
        unrelated = Path("/tmp") / "unrelated-policy-fixture" / "plugins" / "cache" / "openai-primary-runtime" / "documents" / "v1" / "skills" / "documents" / "SKILL.md"
        original_entry = '[[skills.config]]\npath = "{}"\nenabled = true\n'.format(unrelated)
        self.home.joinpath("config.toml").write_text(original_entry, encoding="utf-8")
        applied = self.run_skills_policy("apply", "--yes", extra_environment=environment)
        self.assertEqual(applied.returncode, 0, applied.stderr)
        updated = self.home.joinpath("config.toml").read_text(encoding="utf-8")
        self.assertIn(original_entry.strip(), updated)
        self.assertEqual(updated.count("enabled = false"), 3)

    def test_official_skills_review_and_missing_system_block_verification(self) -> None:
        sources = self.scratch / "plugin-sources"
        environment = self.make_fake_codex(self.required_plugin_records(sources))
        self.write_required_plugin_skills(sources)
        missing_system = self.run_skills_policy("verify", "--json", extra_environment=environment)
        self.assertEqual(missing_system.returncode, 1, missing_system.stderr)
        self.assertEqual(json.loads(missing_system.stdout)["retained_system"], "not_present")

        self.write_system_skills()
        self.write_skill(self.home / "skills" / "context7-cli" / "SKILL.md")
        external_review = self.run_skills_policy("verify", "--json", extra_environment=environment)
        self.assertEqual(external_review.returncode, 1, external_review.stderr)
        self.assertEqual(json.loads(external_review.stdout)["retained_external"], "review")

    def test_official_skills_context7_requires_true_policy_and_narrow_trigger(self) -> None:
        environment = self.make_current_skills_environment()
        self.write_current_context7()
        self.write_current_oracle()
        current = self.run_skills_policy("plan", "--json", extra_environment=environment)
        self.assertEqual(current.returncode, 0, current.stderr)
        self.assertEqual(json.loads(current.stdout)["retained_external"], "current")

        self.write_skill(self.home / "skills" / "context7-cli" / "SKILL.md")
        broad = self.run_skills_policy("plan", "--json", extra_environment=environment)
        self.assertEqual(broad.returncode, 0, broad.stderr)
        self.assertEqual(json.loads(broad.stdout)["retained_external"], "review")
        self.assertEqual(json.loads(broad.stdout)["action"], "blocked")

        self.write_current_context7()
        policy = self.home / "skills" / "context7-cli" / "agents" / "openai.yaml"
        policy.write_text("policy:\n  allow_implicit_invocation: false\n", encoding="utf-8")
        unreachable = self.run_skills_policy("verify", "--json", extra_environment=environment)
        self.assertEqual(unreachable.returncode, 1, unreachable.stderr)
        self.assertEqual(json.loads(unreachable.stdout)["retained_external"], "review")

    def test_official_skills_oracle_requires_exact_reviewed_source(self) -> None:
        environment = self.make_current_skills_environment()
        self.write_current_context7()
        self.write_current_oracle()
        current = self.run_skills_policy("plan", "--json", extra_environment=environment)
        self.assertEqual(current.returncode, 0, current.stderr)
        self.assertEqual(json.loads(current.stdout)["retained_external"], "current")

        runner = self.home / "skills" / "oracle-solver" / "scripts" / "run_oracle.py"
        runner.write_text(runner.read_text(encoding="utf-8") + "\n# drift\n", encoding="utf-8")
        drifted = self.run_skills_policy("plan", "--json", extra_environment=environment)
        self.assertEqual(drifted.returncode, 0, drifted.stderr)
        self.assertEqual(json.loads(drifted.stdout)["retained_external"], "review")
        self.assertEqual(json.loads(drifted.stdout)["action"], "blocked")

    def test_vendored_oracle_runner_enforces_document_only_write_contract(self) -> None:
        namespace = runpy.run_path(str(ORACLE_SKILL / "scripts" / "run_oracle.py"))
        response = {
            "schema_version": "oracle-review-v1",
            "status": "complete",
            "verdict": "proceed",
            "confidence": "high",
            "answer": "A concise answer.",
            "scope": {"reviewed": ["fixture"], "not_reviewed": []},
            "findings": [
                {
                    "id": "F1",
                    "severity": "info",
                    "statement": "The fixture is sound.",
                    "evidence": ["fixture:1"],
                    "reasoning": "The contract is explicit.",
                    "recommendation": "Proceed.",
                }
            ],
            "risks": [],
            "recommended_next_steps": [
                {
                    "order": 1,
                    "action": "Continue.",
                    "rationale": "The fixture passed.",
                    "verification": "Re-run the test.",
                }
            ],
            "assumptions": [],
            "unknowns": [],
        }
        document = namespace["normalize_document_path"](self.scratch / "review.md")
        namespace["require_document_in_workspace"](document, self.scratch)
        namespace["write_document"](document, namespace["render_document"](response))
        marker = namespace["DOCUMENT_MARKER"]
        self.assertTrue(document.read_text(encoding="utf-8").startswith(marker + "\n"))
        self.assertEqual({path.name for path in self.scratch.iterdir()}, {"review.md"})
        handoff = namespace["handoff"](response, document)
        self.assertEqual(handoff["schema_version"], "oracle-review-handoff-v1")
        self.assertEqual(handoff["document_path"], str(document))

        unmanaged = self.scratch / "unmanaged.md"
        unmanaged.write_text("user-owned\n", encoding="utf-8")
        with self.assertRaises(namespace["OracleError"]):
            namespace["normalize_document_path"](unmanaged)

        command = namespace["build_command"](
            "codex", self.scratch, self.scratch / "schema.json", self.scratch / "response.json"
        )
        self.assertIn("--search", command)
        self.assertIn("workspace-write", command)
        self.assertNotIn("read-only", command)
        self.assertNotIn("--disable", command)
        self.assertNotIn("--ignore-user-config", command)
        self.assertNotIn("mcp_servers={}", command)
        self.assertNotIn("--strict-config", command)
        contract = namespace["sanitized_contract"](command, document)
        self.assertEqual(contract["timeout"], "none")
        skill_text = (ORACLE_SKILL / "SKILL.md").read_text(encoding="utf-8")
        self.assertNotIn("read-only", skill_text.lower())
        self.assertIn("1, 2, 4, 8, 16, and then 20 minutes", skill_text)
        self.assertIn("During planning for substantial multi-step work", skill_text)
        self.assertIn("Do not request a follow-up merely to confirm corrections", skill_text)
        self.assertNotIn("independent final reviewer", skill_text)
        self.assertIn("not a claim of infallibility", skill_text)
        self.assertEqual(namespace["delete_document"](document), document)
        self.assertFalse(document.exists())

        target = self.scratch / "target"
        target.mkdir()
        request = target / "request.json"
        request.write_text(
            json.dumps(
                {
                    "objective": "Review the fixture.",
                    "context": "Fixture context.",
                    "questions": ["Is it sound?"],
                    "constraints": [],
                    "prior_attempts": [],
                    "evidence": [],
                    "excluded_actions": [],
                    "requested_deliverable": "A verdict.",
                }
            ),
            encoding="utf-8",
        )
        managed_document = target / "oracle-review.md"
        captured: Dict[str, Path] = {}

        def fake_run(command, prompt, scratch_workspace, environment):
            captured["scratch"] = scratch_workspace
            self.assertNotEqual(scratch_workspace, target)
            self.assertEqual(environment["TMPDIR"], str(scratch_workspace))
            self.assertIn(str(target), prompt)
            (scratch_workspace / "intermediate.txt").write_text("scratch", encoding="utf-8")
            output = Path(command[command.index("--output-last-message") + 1])
            output.write_text(json.dumps(response), encoding="utf-8")
            return ""

        main = namespace["main"]
        with mock.patch.dict(
            main.__globals__,
            {
                "resolve_codex": lambda environment: "codex",
                "verify_model_contract": lambda executable, environment: None,
                "run_codex": fake_run,
            },
        ):
            stdout = io.StringIO()
            with redirect_stdout(stdout):
                result = main(
                    [
                        "--workspace",
                        str(target),
                        "--request-file",
                        str(request),
                        "--document",
                        str(managed_document),
                    ]
                )
        self.assertEqual(result, 0)
        self.assertTrue(managed_document.exists())
        self.assertEqual(json.loads(stdout.getvalue())["document_path"], str(managed_document.resolve()))
        self.assertFalse(captured["scratch"].exists())

    def test_official_skills_partial_failure_restores_exact_config_and_plugin_state(self) -> None:
        sources = self.scratch / "plugin-sources"
        canva = self.plugin_record("canva@openai-curated", sources / "canva")
        environment = self.make_current_skills_environment([canva])
        environment.update({
            "CODEX_FAKE_FAIL_COMMAND": "remove:canva@openai-curated",
        })
        original = b'model = "exact-backup"\n'
        self.home.joinpath("config.toml").write_bytes(original)
        applied = self.run_skills_policy("apply", "--yes", extra_environment=environment)
        self.assertEqual(applied.returncode, 2)
        self.assertIn("original state was restored", applied.stderr)
        self.assertEqual(self.home.joinpath("config.toml").read_bytes(), original)
        state = json.loads(Path(environment["CODEX_FAKE_STATE"]).read_text(encoding="utf-8"))
        restored = next(item for item in state["installed"] if item["pluginId"] == "canva@openai-curated")
        self.assertEqual(restored["version"], "fixture-v1")
        transaction = next((self.home / ".codex-policy" / "skills-transactions").iterdir())
        journal = json.loads((transaction / "state.json").read_text(encoding="utf-8"))
        self.assertEqual(journal["state"], "rolled_back")
        self.assertEqual(journal["plugin_before"]["canva@openai-curated"]["version"], "fixture-v1")

    def test_official_skills_changed_compensation_requires_recovery(self) -> None:
        sources = self.scratch / "plugin-sources"
        canva = self.plugin_record("canva@openai-curated", sources / "canva")
        environment = self.make_current_skills_environment([canva])
        environment.update({
            "CODEX_FAKE_FAIL_COMMAND": "remove:canva@openai-curated",
            "CODEX_FAKE_ADD_VERSION": "fixture-v2",
        })
        original = b'model = "exact-even-on-recovery"\n'
        self.home.joinpath("config.toml").write_bytes(original)
        applied = self.run_skills_policy("apply", "--yes", extra_environment=environment)
        self.assertEqual(applied.returncode, 2)
        self.assertIn("requires manual recovery", applied.stderr)
        self.assertEqual(self.home.joinpath("config.toml").read_bytes(), original)
        transaction = next((self.home / ".codex-policy" / "skills-transactions").iterdir())
        journal = json.loads((transaction / "state.json").read_text(encoding="utf-8"))
        self.assertEqual(journal["state"], "recovery_required")

    def test_official_skills_concurrent_failure_edit_is_not_overwritten(self) -> None:
        sources = self.scratch / "plugin-sources"
        canva = self.plugin_record("canva@openai-curated", sources / "canva")
        environment = self.make_current_skills_environment([canva])
        environment.update({
            "CODEX_FAKE_FAIL_COMMAND": "remove:canva@openai-curated",
            "CODEX_FAKE_CONCURRENT_EDIT": "concurrent_note = true",
        })
        original = b'model = "do-not-overwrite-concurrent"\n'
        self.home.joinpath("config.toml").write_bytes(original)
        applied = self.run_skills_policy("apply", "--yes", extra_environment=environment)
        self.assertEqual(applied.returncode, 2)
        self.assertIn("requires manual recovery", applied.stderr)
        current = self.home.joinpath("config.toml").read_bytes()
        self.assertTrue(current.startswith(original))
        self.assertIn(b"concurrent_note = true", current)
        self.assertNotEqual(current, original)
        transaction = next((self.home / ".codex-policy" / "skills-transactions").iterdir())
        journal = json.loads((transaction / "state.json").read_text(encoding="utf-8"))
        self.assertEqual(journal["state"], "recovery_required")

    def test_official_skills_blocks_unexpected_standalone_without_deleting(self) -> None:
        environment = self.make_fake_codex([])
        standalone = self.home / "skills" / "playwright" / "SKILL.md"
        self.write_skill(standalone)
        plan = self.run_skills_policy("plan", "--json", extra_environment=environment)
        self.assertEqual(plan.returncode, 0, plan.stderr)
        self.assertEqual(json.loads(plan.stdout)["action"], "blocked")
        applied = self.run_skills_policy("apply", "--yes", extra_environment=environment)
        self.assertEqual(applied.returncode, 2)
        self.assertTrue(standalone.exists())
        self.assert_sanitized(applied)

    def test_official_skills_checks_shared_user_discovery_root(self) -> None:
        environment = self.make_fake_codex([])
        standalone = Path(environment["HOME"]) / ".agents" / "skills" / "gh-fix-ci" / "SKILL.md"
        self.write_skill(standalone)
        plan = self.run_skills_policy("plan", "--json", extra_environment=environment)
        self.assertEqual(plan.returncode, 0, plan.stderr)
        self.assertEqual(json.loads(plan.stdout)["standalone_curated"], "blocking")
        applied = self.run_skills_policy("apply", "--yes", extra_environment=environment)
        self.assertEqual(applied.returncode, 2)
        self.assertTrue(standalone.exists())

    def test_official_skills_write_requires_confirmation(self) -> None:
        environment = self.make_fake_codex([])
        result = self.run_skills_policy("apply", extra_environment=environment)
        self.assertEqual(result.returncode, 2)
        self.assertFalse(self.home.exists())

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
            "f02c56dd8ba2f922c27afdb842428ef88c0917a8b8666d1f8a974593d16398f8",
        )
        self.assertEqual(
            digest(OFFICIAL_SKILLS.read_bytes()),
            "90d273e3e3f1a76a86d1a162f49dfa4cf12779986b27106d121af6c9bf0676e5",
        )
        self.assertEqual(
            {relative: digest((ORACLE_SKILL / relative).read_bytes()) for relative in ORACLE_FILES},
            {
                "SKILL.md": "142ee16180a4c183f384854dedb588d241c54689fc8387defc85938b95c7c318",
                "agents/openai.yaml": "a634149a74b503317eaeed16e1120eba4ee26e6dbf5b0c17508d7703c0c236b1",
                "scripts/run_oracle.py": "0cdd8059b2aa46ee0dc89438765323827d7088e21db31ca8431a697bef7beaa1",
            },
        )


if __name__ == "__main__":
    unittest.main(verbosity=2)
