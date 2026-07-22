# Contract

## Objective

Maintain a portable, public reviewed source for Loop Init and preserve the policy’s fail-closed scope boundaries.

## Constraints

- Use only `global/skills/loop-init` as the reviewed source; do not copy the Codex home into the repository.
- Deployment to the user skill path is a user-authorized, one-way update after source verification.
- Existing project `AGENTS.md` content is preserved; only a single marked Loop Init block is managed.
- The Git audit exception is limited to syntactically exact, non-symbolic Codex turn-diff refs.

## Verification

- focused helper tests and policy-plan checks
- `python3 tests/test_acceptance.py`
- `./bin/codex-policy audit-repo`
- `./bin/codex-policy verify --json`
- `./bin/codex-skills-policy verify --json`

## Stop Conditions

- Required verification fails without an evidence-backed repair.
- The proposed change would require broader configuration, permissions, or Git-ref ownership.
