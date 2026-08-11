# codex-policy

`codex-policy` is a small, public, portable source of truth for personal Codex defaults. It lets a new Codex session diagnose drift and safely update the global policy on another machine without exporting that machine's private Codex state.

The repository follows Codex's documented configuration boundaries: global guidance belongs in `$CODEX_HOME/AGENTS.md` (normally `~/.codex/AGENTS.md`), global user configuration belongs in `$CODEX_HOME/config.toml`, and more-specific project guidance can override global guidance. See the official [AGENTS.md guide](https://learn.chatgpt.com/docs/agent-configuration/agents-md) and [configuration guide](https://learn.chatgpt.com/docs/config-file/config-basic).

## What it manages

| Artifact | Owned scope |
| --- | --- |
| `global/AGENTS.md` | The complete global policy, installed byte-for-byte |
| `global/config.owned.toml` | Only the semantic keys listed in `global/owned-keys.txt` |
| `global/official-skills.json` | Reviewed skill/plugin catalog decisions and exact named disable policy |
| `global/skills/google-workspace-artifact-qa/` | Reviewed read-only Google Docs/Slides final-QA skill, installed by the core policy workflow |
| `global/skills/local-document-extraction/` | Reviewed local OCR and offline structured-extraction skill, installed by the core policy workflow |
| `global/skills/oracle-solver/` | Reviewed public source snapshot, installed by the core policy workflow |
| `global/skills/loop-init/` | Reviewed public source snapshot, installed by the core policy workflow |

The core installer manages the global policy file, portable multi-agent limits, and the fifteen declared files of the reviewed Google Workspace Artifact QA, Local Document Extraction, Oracle Solver, and Loop Init user skills. `codex-policy apply --yes` validates those local sources, atomically installs or updates only their declared files, preserves unrelated skill files, and restores changed files after an ordinary failure. It does not manage the main-session model, reasoning effort, service tier, MCP servers, permissions, sandbox, approval policy, project trust, local paths, environment variables, credentials, marketplaces, feature flags, UI state, or runtime fingerprints. The Local Document Extraction provisioner is deliberately separate: it requires its own explicit `--yes`, installs only into an isolated Codex runtime, and never mutates a bundled plugin runtime.

Official skills and plugins use a separate, explicit workflow. `bin/codex-skills-policy` dynamically resolves installed plugin and skill locations by logical name, disables only the reviewed skill set, and preserves all unrelated configuration. The reviewed state adds no standalone curated, experimental, or optional plugin; apply may restore a missing retained primary-runtime or bundled package from the host's current supported marketplace. It removes stale local Canva and GitHub duplicates, and also removes Game Studio because clean-session tests did not register its skills. Remote connector bundles remain externally managed.

The reviewed connector policy keeps only GitHub `yeet` and the five Google Drive skills active. It disables all Canva, Gmail, and Slack skills plus GitHub's broad triage, review-fix, and CI-routing skills, preserving narrow task-scoped workflows and avoiding catalog crowding while leaving connector accounts untouched.

The reviewed user-skill policy also retires `code-auditor`, `feature-implementing`, and `test-fixing` because their global workflow rules duplicate `AGENTS.md` and impose project-specific ceremony. The policy disables those exact Codex-home skill paths when present but does not vendor or back up their contents, so the local files can be removed and a current version downloaded later if the policy decision changes.

Everything outside the owned-key manifest is preserved. The tool uses a pinned, vendored round-trip TOML parser so comments, ordering, formatting, dotted keys, arrays, and unrelated tables survive an update.

## Use from a new machine

Requirements: Python 3.9 or newer. On macOS and Linux the installer uses POSIX advisory locks and file modes; on Windows it uses the standard-library `msvcrt` byte-range lock and relies on the Codex home Windows ACL. Windows does not expose POSIX mode bits through Python, so the Windows path verifies content and filesystem types but does not treat mode bits as drift. The core policy needs the Codex CLI only for its optional diagnostic check; the skill/plugin workflow requires it for sanitized inventory and supported plugin operations.

```bash
git clone https://github.com/taekimax/codex-policy
cd codex-policy
./bin/codex-policy doctor
./bin/codex-policy apply --yes
./bin/codex-policy verify
# Optional, separately gated marketplace/plugin reconciliation:
./bin/codex-skills-policy plan
./bin/codex-skills-policy apply --yes
./bin/codex-skills-policy verify
```

The HTTPS clone is intentionally anonymous and suitable for public bootstrap and CI. Contributors with write access should use the repository's SSH origin for authenticated Git operations:

```bash
git remote set-url origin git@github.com:taekimax/codex-policy.git
```

Generate and register a separate SSH key on each machine. Never copy a private key between machines. GitHub API operations continue to use the separately authenticated `gh` client.

The reviewed Google Workspace Artifact QA, Local Document Extraction, Oracle Solver, and Loop Init sources are installed by the explicit `codex-policy apply --yes` confirmation. The core workflow validates their source format and executable modes, then verifies the installed copies byte-for-byte and by mode. `codex-skills-policy verify` independently reports whether they still match its reviewed snapshot, but it does not copy vendored user skills itself. Google Workspace Artifact QA is a read/export-only final gate for native Docs and Slides artifacts and does not repair a target without a separate request. Local Document Extraction handles only local read-only OCR and structured conversion when the official PDF or Office skills are insufficient; its networked runtime provisioning remains a separate authorized action. Loop Init is a per-repository initializer: global or project policy may select it for read-only inspection of a new repository task that benefits from durable records, but it must still confirm a selected root and mode before writing project-local `.loop/` files or a managed project `AGENTS.md` section. The vendored sources are authoritative for their respective behavior.

OpenAI's current [skill documentation](https://learn.chatgpt.com/docs/build-skills) describes user skills under `$HOME/.agents/skills`, while the reviewed local Codex runtime for this policy revision still discovers policy-managed skills under `$CODEX_HOME/skills`. The installer intentionally writes only the runtime-confirmed location because identically named skills are independent entries rather than merged layers. Revalidate the installed runtime before migrating this target; do not keep duplicate copies in both locations.

Then start a new Codex session so guidance and skill discovery run again. Opening Codex in this repository also loads the repo-level `AGENTS.md`, which directs the session through the same safe workflow.

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

`plan` is the default and creates nothing. `apply` takes an operating-system advisory lock, recomputes the plan, writes private local backups, atomically replaces only changed policy, configuration, and reviewed-user-skill targets, and restores originals if an ordinary failure occurs. The operating system releases the lock after a crash; an interrupted process is detected on the next run and must be recovered before another apply. A no-op apply creates no backup transaction. On Windows, run the command with Python, for example `python bin/codex-policy apply --yes`; the same transaction and rollback rules apply.

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

Only `skills.config` entries whose exact manifest spec resolves to a safe existing target are reconciled. An unresolved user, connector, or plugin tombstone is left untouched, but a canonical unresolved entry must already be an unambiguous `enabled = false` tombstone. An installed retained plugin must expose exactly its declared top-level skills, and its disabled skills resolve only through the verified local source reported by the plugin inventory; cache fallback is not allowed. A present connector bundle must expose every reviewed active skill and no unreviewed skill, while reviewed disabled skills may be absent when an externally managed catalog contracts; violations block writes. Documents, Presentations, Template Creator, three Canva skills, Gmail, `code-auditor`, `feature-implementing`, `test-fixing`, `find-skills`, and `web-design-guidelines` remain disabled when safely discovered. Context7 and vendored-user-skill absence is advisory. A present Google Workspace Artifact QA, Local Document Extraction, Oracle Solver, or Loop Init skill must exactly match the reviewed files under its `global/skills/` source; drift blocks verification without rewriting the live skill. When Context7 is present, its runtime policy must allow implicit invocation so `$context7-cli` is reachable, while its skill description must restrict triggering to explicit `ctx7`, `Context7`, or `$context7-cli` mentions and reject generic library-documentation routing. Review-required Context7 or vendored-user-skill state and missing runtime system skills block verification. Other external and all system source trees are never rewritten by this repository.

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
