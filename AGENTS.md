# Codex Policy Repository

This public repository maintains a portable global Codex policy. `global/AGENTS.md` is the exact deployable policy; `global/config.owned.toml` and `global/owned-keys.txt` define the only configuration values this repository owns.

## Operating Rules

- Read `README.md`, then use `./bin/codex-policy` for diagnosis and installation. The default command is a read-only plan.
- Treat diagnose, review, and plan requests as read-only. When the user explicitly asks to install or update, run `plan`, then `apply --yes`, then `verify`.
- Never copy the live Codex home into this repository. Do not open, print, log, or export raw authentication, session, cache, history, backup, trust, or configuration state; let the policy tool parse target configuration privately.
- Preserve every target configuration value outside `global/owned-keys.txt`. Never add ownership of permissions, sandboxing, approvals, project trust, credentials, paths, plugins, UI state, or runtime fingerprints without explicit user direction and a security review.
- Keep repo-root instructions separate from the byte-exact deployable `global/AGENTS.md`. Do not add a repo `.codex/config.toml`, automatic reverse-sync, or networked install step.
- This repository is public. Before any commit or push, run `python3 tests/test_acceptance.py` and `./bin/codex-policy audit-repo`, inspect the intended diff and Git identity, and verify the exact remote and visibility.
- A successful global-file update is visible to newly started Codex sessions. Tell the user to start a new session after `verify` passes.
