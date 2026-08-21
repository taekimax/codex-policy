# Plan

## Outcome

Update, deploy, commit, and publish a smaller risk-proportional global workflow policy.

## Steps

1. Inspect current policy, repository history, Loop records, related project guidance, and relevant user-owned diff.
2. Identify only missing or contradictory global rules.
3. Refine global continuity, verification, local-artifact, safety, and subagent language; align Loop guidance and tests.
4. Review the exact diff and references, update reviewed hashes, and run repository acceptance and audit gates.
5. Apply and verify the core policy, then report separately gated plugin-policy drift without changing it.
6. Verify Git identity, SSH remote, public visibility, and remote ancestry; commit, push, refetch, and prove parity.

## Risks

- Over-generalizing one project's workflow could weaken valid release or data-boundary checks.
- Leaving old exact-string assertions or reviewed hashes would create broken policy references.
- Updating completed Loop task files without preserving decision and log history could confuse evidence with authority.
