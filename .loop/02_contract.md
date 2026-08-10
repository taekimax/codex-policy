# Contract

## Objective

Add a fail-closed, read-only final QA layer without expanding configuration, credential, or official-plugin ownership.

## Constraints

- Keep global guidance concise and API-neutral; keep field-level checks in the QA skill.
- Default Korean font to `Noto Sans KR`, while allowing a user-selected Google-supported alternative.
- Treat Arial, unexpected or unresolved fonts, locale mismatch, and physical-size mismatch as errors.
- Never pass without native PDF export and inspection of every rendered page or slide.
- Do not mutate a target Google file unless a separate repair request authorizes it.

## Verification

- `quick_validate.py global/skills/google-workspace-artifact-qa`
- focused acceptance coverage and `python3 tests/test_acceptance.py`
- `./bin/codex-policy audit-repo` and `git diff --check`
- core policy plan/apply/verify plus skills-policy verification
- exact source/live byte and mode comparison for the two managed skill files
- Git identity, remote visibility, commit, push, and final remote parity

## Stop Conditions

- A required check would require modifying official plugin cache contents.
- Public audit, installer rollback/scope guarantees, or live verification cannot be preserved.
- The target Git identity, remote, or public visibility does not match the approved repository.
