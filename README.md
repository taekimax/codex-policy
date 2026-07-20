# codex-policy

`codex-policy` is a small, public, portable source of truth for personal Codex defaults. It lets a new Codex session diagnose drift and safely update the global policy on another machine without exporting that machine's private Codex state.

The repository follows Codex's documented configuration boundaries: global guidance belongs in `$CODEX_HOME/AGENTS.md` (normally `~/.codex/AGENTS.md`), global user configuration belongs in `$CODEX_HOME/config.toml`, and more-specific project guidance can override global guidance. See the official [AGENTS.md guide](https://learn.chatgpt.com/docs/agent-configuration/agents-md) and [configuration guide](https://learn.chatgpt.com/docs/config-file/config-basic).

## What it manages

| Artifact | Owned scope |
| --- | --- |
| `global/AGENTS.md` | The complete global policy, installed byte-for-byte |
| `global/config.owned.toml` | Only the semantic keys listed in `global/owned-keys.txt` |
| `global/official-skills.json` | Reviewed skill/plugin catalog decisions and exact named disable policy |

The core installer manages only portable multi-agent limits. It deliberately does not manage the main-session model, reasoning effort, service tier, MCP servers, permissions, sandbox, approval policy, project trust, local paths, environment variables, credentials, marketplaces, feature flags, UI state, or runtime fingerprints.

Official skills and plugins use a separate, explicit workflow. `bin/codex-skills-policy` dynamically resolves installed plugin and skill locations by logical name, disables only the reviewed skill set, and preserves all unrelated configuration. The reviewed state adds no standalone curated, experimental, or optional plugin; apply may restore a missing retained primary-runtime or bundled package from the host's current supported marketplace. It removes stale local Canva and GitHub duplicates, and also removes Game Studio because clean-session tests did not register its skills. Remote connector bundles remain externally managed.

The reviewed connector policy keeps only GitHub `yeet` and the five Google Drive skills active. It disables all Canva, Gmail, and Slack skills plus GitHub's broad triage, review-fix, and CI-routing skills, preserving narrow task-scoped workflows and avoiding catalog crowding while leaving connector accounts untouched.

Everything outside the owned-key manifest is preserved. The tool uses a pinned, vendored round-trip TOML parser so comments, ordering, formatting, dotted keys, arrays, and unrelated tables survive an update.

## Use from a new machine

Requirements: macOS or Linux and Python 3.9 or newer. The core policy needs the Codex CLI only for its optional diagnostic check; the skill/plugin workflow requires it for sanitized inventory and supported plugin operations.

```bash
git clone https://github.com/taekimax/codex-policy
cd codex-policy
./bin/codex-policy doctor
./bin/codex-policy apply --yes
./bin/codex-policy verify
./bin/codex-skills-policy plan
./bin/codex-skills-policy apply --yes
./bin/codex-skills-policy verify
```

The HTTPS clone is intentionally anonymous and suitable for public bootstrap and CI. Contributors with write access should use the repository's SSH origin for authenticated Git operations:

```bash
git remote set-url origin git@github.com:taekimax/codex-policy.git
```

Generate and register a separate SSH key on each machine. Never copy a private key between machines. GitHub API operations continue to use the separately authenticated `gh` client.

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

## Official skill and plugin policy

```text
codex-skills-policy                 read-only plan
codex-skills-policy plan [--json] [--check]
codex-skills-policy doctor [--json]
codex-skills-policy apply --yes
codex-skills-policy verify [--json]
```

This workflow is opt-in because plugin add/remove commands use the host's current supported configured marketplace snapshot. Planning and verification suppress raw Codex output and never print paths or target configuration. Apply uses supported Codex plugin commands and a private configuration backup. After an ordinary failure it compensates completed operations and restores the exact configuration backup only when the current bytes are still the initial snapshot or the exact candidate written by this transaction; a concurrent edit is preserved and forces recovery. Rollback succeeds only when affected plugin presence, enabled state, version, and source identity also match the initial inventory; otherwise it leaves a recovery-required journal. An unexpected standalone curated skill, unsafe or incomplete discovery state, review-required retained state, or unfinished transaction blocks writes for manual review. Installed-but-disabled retained plugins remain a manual block rather than being riskily re-enabled, and the tool never recursively deletes a skill directory.

Only `skills.config` entries whose exact manifest spec resolves to a safe existing target are reconciled. An unresolved user, connector, or plugin tombstone is left untouched, but a canonical unresolved entry must already be an unambiguous `enabled = false` tombstone. An installed retained plugin must expose exactly its declared top-level skills, and a present connector bundle must match its declaration; either mismatch blocks writes. Documents, Presentations, Template Creator, three Canva skills, Gmail, `find-skills`, and `web-design-guidelines` remain disabled when safely discovered. Context7 and Oracle Solver absence is advisory. When Context7 is present, its runtime policy must allow implicit invocation so `$context7-cli` is reachable, while its skill description must restrict triggering to explicit `ctx7`, `Context7`, or `$context7-cli` mentions and reject generic library-documentation routing. Review-required Context7 state and missing runtime system skills block verification. External and system source trees are never rewritten by this repository.

The catalog revisions in `global/official-skills.json` are evidence for the recorded review decisions, not install pins. Retained primary-runtime and bundled packages use the host's current supported marketplace, while the allowlisted stable plugin and skill IDs remain fixed. The official standalone repository no longer contains an experimental catalog at the reviewed revision. Re-run the catalog review before changing that manifest; do not treat a newer marketplace snapshot as implicit authorization to install more skills.

## Development and release checks

```bash
python3 tests/test_acceptance.py
./bin/codex-policy audit-repo
./bin/codex-skills-policy doctor
git status --short
git diff --check
```

CI runs the acceptance suite and repository audit on macOS and Ubuntu with read-only repository permissions. CI actions and the vendored TOML parser are pinned. The vendored `tomlkit` 0.15.1 package is distributed under its included MIT license; its wheel was verified against SHA-256 `177a05aece5a8ca5266fd3c448abb47b8d352f09d477d3ca8332db4d89b24304` from PyPI before extraction.

This repository intentionally contains no general project license. Public visibility alone does not grant reuse rights beyond licenses attached to third-party components.
