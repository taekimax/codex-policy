# Security

This repository is public and must contain only the allowlisted portable policy artifacts. Never contribute live Codex configuration, credentials, authentication files, session data, histories, logs, caches, backups, trust records, machine paths, environment values, or runtime fingerprints.

Skill/plugin policy must use logical names and reviewed public catalog revisions. Never copy resolved plugin paths, connected-account metadata, or local plugin inventory output. Skill contents are allowed only in the reviewed `global/skills/oracle-solver` source tree; never place them in `global/official-skills.json`. Reconciliation output must remain status-only and sanitized.

Run both checks before every public push:

```bash
python3 tests/test_acceptance.py
./bin/codex-policy audit-repo
```

If a secret reaches Git history, rotate or revoke it before attempting history cleanup. For an unpublished repository, recreate clean history from reviewed allowlisted files. Do not assume `.gitignore` or deletion from the current tree removes a secret from reachable history.

Do not disclose an active credential in a public issue. Use GitHub's private security-reporting surface when available; otherwise report the issue without including the credential and rotate it immediately.
