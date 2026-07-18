# codex-policy

`codex-policy` is a small, public, portable source of truth for personal Codex defaults. It lets a new Codex session diagnose drift and safely update the global policy on another machine without exporting that machine's private Codex state.

The repository follows Codex's documented configuration boundaries: global guidance belongs in `$CODEX_HOME/AGENTS.md` (normally `~/.codex/AGENTS.md`), global user configuration belongs in `$CODEX_HOME/config.toml`, and more-specific project guidance can override global guidance. See the official [AGENTS.md guide](https://learn.chatgpt.com/docs/agent-configuration/agents-md) and [configuration guide](https://learn.chatgpt.com/docs/config-file/config-basic).

## What it manages

| Artifact | Owned scope |
| --- | --- |
| `global/AGENTS.md` | The complete global policy, installed byte-for-byte |
| `global/config.owned.toml` | Only the semantic keys listed in `global/owned-keys.txt` |

The initial managed configuration covers only portable multi-agent limits. It deliberately does not manage the main-session model, reasoning effort, service tier, MCP servers, permissions, sandbox, approval policy, project trust, local paths, environment variables, credentials, plugins, marketplaces, feature flags, UI state, or runtime fingerprints.

Everything outside the owned-key manifest is preserved. The tool uses a pinned, vendored round-trip TOML parser so comments, ordering, formatting, dotted keys, arrays, and unrelated tables survive an update.

## Use from a new machine

Requirements: macOS or Linux and Python 3.9 or newer. The Codex CLI is needed only for the optional official diagnostic check.

```bash
git clone https://github.com/taekimax/codex-policy.git
cd codex-policy
./bin/codex-policy doctor
./bin/codex-policy apply --yes
./bin/codex-policy verify
```

Then start a new Codex session so guidance discovery runs again. Opening Codex in this repository also loads the repo-level `AGENTS.md`, which directs the session through the same safe workflow.

The command honors `CODEX_HOME`, which makes isolated testing and non-default installations possible. It never prints the expanded home path, existing configuration values, diffs, backup contents, or hashes.

## Commands

```text
codex-policy                      read-only plan
codex-policy plan [--json] [--check]
codex-policy doctor [--json]     plan plus a suppressed-output Codex diagnostic
codex-policy apply --yes          transactional install/update
codex-policy verify [--json]     require the managed state to be current
codex-policy recover              preview recovery after an interrupted apply
codex-policy recover --apply --yes
codex-policy audit-repo           public-repository safety audit
```

`plan` is the default and creates nothing. `apply` takes an operating-system advisory lock, recomputes the plan, writes private local backups, atomically replaces only changed targets, and restores originals if an ordinary failure occurs. The operating system releases the lock after a crash; an interrupted process is detected on the next run and must be recovered before another apply. A no-op apply creates no backup transaction.

An existing `AGENTS.override.md`, invalid TOML, symlinked target, ambiguous owned path, concurrent modification, or unfinished transaction blocks writes. The tool reports only a sanitized status.

Backups stay under the target Codex home with owner-only permissions and may contain the machine's original configuration. They are never repository inputs and must never be committed or shared.

## Development and release checks

```bash
python3 tests/test_acceptance.py
./bin/codex-policy audit-repo
git status --short
git diff --check
```

CI runs the acceptance suite and repository audit on macOS and Ubuntu with read-only repository permissions. CI actions and the vendored TOML parser are pinned. The vendored `tomlkit` 0.15.1 package is distributed under its included MIT license; its wheel was verified against SHA-256 `177a05aece5a8ca5266fd3c448abb47b8d352f09d477d3ca8332db4d89b24304` from PyPI before extraction.

This repository intentionally contains no general project license. Public visibility alone does not grant reuse rights beyond licenses attached to third-party components.
