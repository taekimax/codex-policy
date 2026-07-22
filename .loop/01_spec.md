# Specification

## Objective

Add `global/skills/loop-init` as a reviewed user-skill source and make `codex-skills-policy` detect source drift without managing unrelated skills.

## Scope

- Initialize this repository with `.loop/` in create-missing mode.
- Replace mandatory role and stale-chat authority language with optional, task-scoped durable-record guidance.
- Reject duplicate or malformed managed `AGENTS.md` markers before writing.
- Preflight target topology and roll back ordinary write failures.
- Permit only exact local `refs/codex/turn-diffs/...` capture/checkpoint patterns in the repository audit.

## Out of Scope

- Global configuration ownership, permissions, credentials, marketplaces, and unrelated skills.
- Broad Git-ref allowlisting or a networked install path.

- Acceptance tests cover reviewed source drift, marker rejection, initialization behavior, and the constrained Git-ref exception.
- `codex-policy` and `codex-skills-policy` plan/apply/verify report a clean state after approved deployment.

## Unknowns

- Runtime-specific ref formats may change; unexpected refs must remain blocked.
