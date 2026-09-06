# Codex Policy Repository

`global/AGENTS.md` is the canonical global instruction file. `global/config.owned.toml` and `global/owned-keys.txt` define the configuration this repository owns. Reviewed user skills live under `global/skills/`; the host's installed copies are deployment targets.

Read `README.md` for the existing deployment workflow. A request to implement and apply policy changes authorizes editing these sources and running `./bin/codex-policy plan`, `apply --yes`, and `verify`. Read-only audit requests remain read-only. Use `./bin/codex-skills-policy` only for requested skill/plugin reconciliation; inspect its plan because it may include unrelated marketplace changes.

Preserve configuration outside the declared ownership and unrelated user work. Do not import private live configuration, credentials, sessions, or backups into this public repository. Keep repository guidance separate from the global payload, and avoid reverse-sync or a second deployment mechanism.

Keep core deployment portable across macOS and Windows. When retiring a previously managed file, preserve its transaction target name and use the existing backup, apply, and recovery path so updating an older host reaches the same state as a fresh install. Retain unknown local files and keep optional runtime provisioning separate from policy deployment.

Use focused checks for documentation and relevant installer checks for deployment changes. Before an authorized commit or push, run the existing acceptance suite and repository audit, inspect the intended diff, and verify Git identity and destination. Publication requires current authorization; old task records do not supply it.

The `.loop/README.md` file records the latest policy audit. Other files in `.loop/` are historical evidence, not active instructions. There is no global Loop workflow or required record structure.

Global guidance and skill discovery refresh in a new Codex session. Tell the user when verified live changes require that refresh.
