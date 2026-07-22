# Codex Policy Repository

This public repository maintains a portable global Codex policy. `global/AGENTS.md` is the exact deployable policy; `global/config.owned.toml` and `global/owned-keys.txt` define the only configuration values this repository owns; and `global/skills/oracle-solver` plus `global/skills/loop-init` are the reviewed public source snapshots installed by the core policy workflow.

## Operating Rules

- Read `README.md`, then use `./bin/codex-policy` for core policy work and `./bin/codex-skills-policy` for the separately gated skill/plugin policy. Both default commands are read-only plans.
- Treat diagnose, review, and plan requests as read-only. When the user explicitly asks to install or update, run `plan`, then `apply --yes`, then `verify`.
- Never copy the live Codex home into this repository. The reviewed skill mirrors are `global/skills/oracle-solver` and `global/skills/loop-init`; `codex-policy apply --yes` is the explicit authorization to synchronize only their declared files after source-level validation. Do not open, print, log, or export raw authentication, session, cache, history, backup, trust, or configuration state; let the policy tool parse target configuration privately.
- Preserve every target configuration value outside `global/owned-keys.txt` and the exact logical `skills.config` entries declared in `global/official-skills.json`. Never add ownership of permissions, sandboxing, approvals, project trust, credentials, arbitrary paths, marketplaces, UI state, or runtime fingerprints without explicit user direction and a security review.
- Keep repo-root instructions separate from the byte-exact deployable `global/AGENTS.md`. Do not add a repo `.codex/config.toml`, automatic reverse-sync, or networked install step.
- This repository is public. Before any commit or push, run `python3 tests/test_acceptance.py` and `./bin/codex-policy audit-repo`, inspect the intended diff and Git identity, and verify the exact remote and visibility.
- A successful global-file update is visible to newly started Codex sessions. Tell the user to start a new session after `verify` passes.

---
<!-- BEGIN MODEL LOOP POLICY -->
## Optional Loop Workspace

Use `.loop/` only for work that benefits from durable, resumable project records. Read the minimum relevant files before continuing a loop-backed task.

`.loop/` records complement the current user request, repository guidance, source, and test evidence; it does not override any of them or authorize an otherwise-unapproved action.

For loop-backed work:
- keep the request, specification, contract, plan, progress, decisions, and log concise and task-specific
- keep changes within the active contract and record meaningful decisions or blockers
- use a planner, generator, evaluator, or another specialist only when its expected value justifies the coordination cost
- verify completion against the current request and available evidence
- never record secrets, credentials, or private configuration
<!-- END MODEL LOOP POLICY -->
---
