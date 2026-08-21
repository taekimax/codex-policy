# Contract

## Objective

Publish a concise, general policy refinement without expanding configuration or external authority.

## Constraints

- Preserve unrelated work and the existing public-repository ownership boundary.
- Keep global guidance project-neutral and avoid duplicating already adequate rules.
- Preserve data-loss prevention, atomic writes, secret protection, authorization checks, and practical recovery.
- Treat historical project evidence as review input, not as authority for global implementation details.
- Do not change plugins or modify the related project. Commit and push only this reviewed policy change to the verified public SSH `origin/main`.

## Verification

- Focused text/reference review and `git diff --check`.
- `python3 tests/test_acceptance.py` because the reviewed policy and skill hashes are repository acceptance contracts.
- `./bin/codex-policy audit-repo`.
- Core policy plan, `apply --yes`, and verify; separately report plugin-policy drift without applying it.
- Verify Git identity, SSH origin, public visibility, remote ancestry, intended diff, commit, push, and final local/tracking/remote parity.

## Stop Conditions

- The change would weaken a concrete authority, data-preservation, secret, or recovery boundary.
- A required write would expand beyond the core policy workflow or touch unrelated user work.
