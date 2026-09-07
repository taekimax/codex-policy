# codex-policy

Canonical sources and a portable installer for consistent personal Codex defaults across Macs and Windows machines. Git distributes the reviewed policy; each host applies it to its own Codex home while preserving host-specific settings and accounts. The global guide expresses intent, autonomy, proportionate risk judgment, and communication preferences; specialized skills contain task-specific guidance and tools.

## Sources and loading

| Layer | Source and role |
| --- | --- |
| Global instructions | `global/AGENTS.md`, deployed byte-for-byte to `$CODEX_HOME/AGENTS.md` |
| Repository instructions | Root `AGENTS.md`, applicable only when working in this repository |
| Owned settings | `global/config.owned.toml` and `global/owned-keys.txt`: portable agent limits |
| Artifact QA | `global/skills/google-workspace-artifact-qa/`: native Google layout and typography checks |
| Local extraction | `global/skills/local-document-extraction/`: OCR and offline structured conversion tools |
| macOS delivery | `global/skills/macos-app-delivery/`: recoverable app delivery using project adapters |
| Handoff template | `global/templates/session-handoff.txt`, deployed to `$CODEX_HOME/templates/` |
| Optional catalog reconciliation | `global/official-skills.json` and `bin/codex-skills-policy` |
| Audit record | `.loop/README.md`; older decisions and logs are historical only |

Codex normally uses `~/.codex` as its global root, or `CODEX_HOME` when set. A nonempty global `AGENTS.override.md` takes precedence over `AGENTS.md`; more-specific project instructions are layered afterward. The installer refuses to write through an override. See the official [instruction discovery guide](https://learn.chatgpt.com/docs/agent-configuration/agents-md) and [configuration precedence](https://learn.chatgpt.com/docs/config-file/config-basic).

The instruction review follows the [GPT-6 Astra guidance](https://developers.openai.com/api/docs/guides/latest-model): make autonomy and skill precedence explicit, specify useful communication, and calibrate delegation and testing. Model selection remains host-owned. This repository does not install an API migration or modify credentials, permissions, sandboxing, approvals, project trust, runtime feature flags, or unrelated host settings.

## Apply the core policy

Requires Python 3.9 or newer. The core command works locally on macOS, Linux, and Windows; Windows uses native locking and verifies content without POSIX mode checks. It honors `CODEX_HOME` for alternate installations and isolated tests.

```bash
./bin/codex-policy plan
./bin/codex-policy apply --yes
./bin/codex-policy verify
```

The core installer manages the global guide, declared settings, eleven files belonging to the three retained user skills, and the short handoff template. It validates source metadata and script syntax, preserves unowned TOML through the vendored round-trip parser, and atomically replaces changed files with private local backups and rollback after ordinary failures. It checks installed content against the canonical source; prose changes do not require updating duplicate hardcoded content hashes.

The same transaction retires the six previously managed Oracle Solver and Loop Init files. `plan` and `verify` report whether any retired files remain, so an existing installation must remove them before it is considered current. Their current bytes, including local modifications, are backed up before removal. Unknown files in those directories and all project-local records are preserved. An ordinary failure restores the files, and `recover` also understands interrupted transactions from versions that installed these skills.

A no-op apply creates no backup transaction. Invalid TOML, unsafe targets, concurrent changes, or unfinished transactions are reported before further writes. Use `recover` to preview interrupted recovery, then `recover --apply --yes` when recovery is intended. `doctor` adds an optional Codex diagnostic. Backups under the target Codex home can contain private configuration and are never repository inputs.

On Windows, invoke the commands with Python, for example `python bin/codex-policy apply --yes`. Core policy deployment and retirement use native filesystem operations; no shell or WSL is needed. The optional local extraction skill's supplied launchers and provisioner are POSIX tools, so installing its guidance does not establish a working native Windows OCR runtime.

Start a new Codex session after a successful live update. System and plugin skills are supplied by their owners and are not rewritten here. The reviewed host currently discovers managed user skills under `$CODEX_HOME/skills`; revalidate discovery before moving to a different runtime location rather than installing duplicates.

## Synchronize another machine

After a reviewed change is published to `origin/main`, update each machine's checkout and apply from it. Preserve local edits when reconciling an existing checkout; do not reset it to force a pull.

For the first checkout, an anonymous public clone works without sharing credentials between machines:

```text
git clone https://github.com/taekimax/codex-policy
cd codex-policy
```

On macOS, from the existing checkout:

```bash
git pull --ff-only origin main
python3 bin/codex-policy plan
python3 bin/codex-policy apply --yes
python3 bin/codex-policy verify
```

On Windows, from PowerShell in the existing checkout:

```powershell
git pull --ff-only origin main
python bin/codex-policy plan
python bin/codex-policy apply --yes
python bin/codex-policy verify
```

For authenticated Git operations, use `git@github.com:taekimax/codex-policy.git` with each machine's own SSH setup; GitHub API work uses existing `gh` OAuth. Do not copy a Codex home or its backups between machines. `CODEX_HOME` selects a non-default local target. Restart Codex after verification passes.

Loop Init and Oracle Solver are retired through this normal apply workflow; fresh installs omit both. The global guide contains the useful continuity and ordinary subagent guidance, without a required `.loop/` framework or dedicated independent xhigh reviewer. The optional catalog policy retains exact disable entries for legacy installations, but plugin reconciliation is not needed to retire the core-managed files.

## Optional skill and plugin reconciliation

```bash
./bin/codex-skills-policy plan
./bin/codex-skills-policy apply --yes
./bin/codex-skills-policy verify
```

This is separate from core deployment. Its manifest records earlier catalog decisions; dates and marketplace snapshots are historical evidence, not current install pins or permission to change a host. Review the plan against the requested scope before applying. Current marketplace drift can affect this diagnostic without invalidating a successful core policy update.

The tool reconciles only declared plugin operations and exact skill-disable entries, preserves unrelated configuration and connector accounts, and uses the host's supported plugin commands. It verifies retained user-skill files against canonical sources but does not copy them. The narrow Context7 lookup stays externally managed, and system skill sources are never rewritten here.

## Verification and maintenance

```bash
git diff --check
python3 tests/test_acceptance.py
./bin/codex-policy audit-repo
```

Use Python 3.10 or newer for the full suite because its Docling runtime fixture checks that minimum; the core installer supports Python 3.9. Use the checks relevant to a change. Acceptance tests cover installation, preservation, rollback, retirement policy, and extraction behavior. The public repository audit checks allowed files and Git state; its index check requires intended file additions and deletions to be staged before release. An isolated index can check a candidate without staging the working checkout.

CI runs the full suite and audit on macOS, Ubuntu, and Windows with Python 3.12, plus focused core installer checks on Python 3.9. POSIX-only extraction checks are skipped on Windows. Configured CI coverage is not evidence of a successful run until that revision has executed there. The vendored `tomlkit` 0.15.1 parser retains its MIT license; this repository has no general project license.
