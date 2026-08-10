# Specification

## Objective

Manage a portable Google Workspace artifact QA policy and skill that catch locale, effective-font, page-mode, physical-size, and rendered-output defects.

## Scope

- Add only common pre-authoring and post-conversion invariants to `global/AGENTS.md`.
- Add `global/skills/google-workspace-artifact-qa/{SKILL.md,agents/openai.yaml}` as an exact reviewed source.
- Extend the core installer, official inventory, cross-verification, public audit allowlist and hashes, README, and acceptance suite.
- Apply and verify the reviewed global policy and skill in the live Codex home, then publish the repository change.

## Out of Scope

- Modifying official `google-docs`, `google-slides`, or `presentations` plugin caches.
- Automatically repairing Google files during QA.
- Adding credentials, API permissions, marketplace ownership, or a Google-specific runtime client.

## Acceptance

- Korean locale and Google-supported font rules, A4 dimensions, 16:9 rejection for A4, native readback, native PDF export, and all-page render verification are explicit.
- Slides resolves every text run through inherited styles; Docs checks PAGES/PAGELESS, geometry, margins, and effective fonts.
- Managed install and drift detection cover both QA skill files.
- Skill validation, acceptance, repository audit, live plan/apply/verify, diff checks, and source/live parity pass.
