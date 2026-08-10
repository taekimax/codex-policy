# Plan

## Outcome

Publish and deploy a managed Google Workspace Artifact QA skill and the corresponding portable global invariants.

## Steps

1. Inspect the clean checkout, README, existing managed-skill implementation, official authoring skills, and current read-only policy plans.
2. Create the skill with the standard initializer and implement the read-only QA contract.
3. Update global policy, project documentation, inventory, installers, audit allowlists and reviewed hashes, and acceptance coverage.
4. Validate the skill, run focused and full local gates, and forward-test the QA behavior against a realistic converted Slides case.
5. Review the exact diff, apply the core policy and managed skill live, and verify source/live parity plus skills-policy state.
6. Verify Git identity, SSH remote and public visibility; commit, push, refetch, and confirm local/remote parity.

## Risks

- Inherited text styles can hide Arial substitution unless every effective font is resolved.
- Google APIs may expose required root properties as read-only; the skill must fail rather than imply repair.
- Hash-pinned public audit data must be updated only after the reviewed artifacts are final.
