# Global instruction audit — 2026-09-06

## Scope and state

Review and implement global instructions for GPT-6 Astra and personal private projects. The live root is the host's Codex home; `global/AGENTS.md` and `global/skills/` are canonical. The source checkout and deployed core policy matched at the start. The host already selected GPT-6 Astra with high reasoning. Model, permission, credential, and unrelated plugin settings are outside the changes.

The task covers source edits, live deployment, and retirement of redundant skills. The follow-up requests a repository update for consistency across multiple Macs and Windows machines, checking remote origin first. The user explicitly directed removal of Oracle and the independent xhigh reviewer. Old active Loop files have been removed; older decision/log files remain historical evidence only.

## Decisions

| Layer | Decision and reason |
| --- | --- |
| Global `AGENTS.md` | Simplify: one guide for intent, authority, judgment, continuity, verification, and communication. Preserve concise recurring preferences. |
| Global Loop policy / Loop Init | Delete: normal judgment and a short continuity paragraph cover the useful behavior without a framework or initialization approval loop. |
| Oracle Solver / dedicated xhigh reviewer | Delete, as explicitly requested. Ordinary bounded subagents remain available. |
| Google Workspace Artifact QA | Keep and simplify: native conversion, inherited fonts, and physical geometry need specialized guidance; fold duplicated Google checks here and remove universal gates and redundant repair approval. |
| Local Document Extraction | Keep and simplify: executable OCR and offline conversion add capability; shorten procedures and make verification task-proportional. |
| Context7 | Keep unchanged: narrow, explicitly requested version-aware lookup; externally managed. |
| OpenAI Docs / Skill Creator | Keep unchanged: system-owned references. User intent governs their use; no generic migration workflow or system-cache fork. |
| Root `AGENTS.md` and repository records | Simplify: source/deployment ownership only; remove duplicated global behavior and stale active authority. |
| Core deployment | Keep and extend: preserves host config, applies portable sources, and transactionally retires the six formerly managed skill files on existing hosts. Keep legacy transaction names for recovery; remove duplicate hardcoded prose hashes. |
| Skill/plugin catalog | Keep separate: add exact retirement entries using the existing mechanism; do not reconcile unrelated marketplace drift. |

## Evidence and verification

Official references: [Astra guidance](https://developers.openai.com/api/docs/guides/latest-model), [instruction discovery](https://learn.chatgpt.com/docs/agent-configuration/agents-md), and [configuration precedence](https://learn.chatgpt.com/docs/config-file/config-basic).

Confirmed no global override or parent instruction file on this host. The old required DOCX verifier path was missing, so the global guide now directs task-appropriate artifact verification without that dependency. Global instructions had grown to 17,318 bytes and repeated decision and verification rules across sections. A dedicated skill and eight repository records added further context and stale task authority.

Completed source edits and live deployment. The global guide is 8,166 bytes, down from 17,318 (53%). Core deployment reports current policy, current managed settings, current retained skills, and a clean transaction. The live configuration was preserved byte-for-byte. Oracle and Loop Init matched their original reviewed source before being moved to timestamped Trash directories outside discovery.

- PASS: 46 acceptance tests under Python 3.12, including installer preservation, rollback, retirement, source parity, extraction fixtures, and repository audit.
- PASS: both retained skill validators, source/reference review, and diff whitespace checks.
- PASS: core apply/verify and removal of both retired live skill directories. Fresh installs omit the skills; older installations now remove the six declared files with exact backups, local-extra preservation, rollback, and interrupted recovery.
- PASS: repository audit used a temporary candidate index; the checkout's actual index remained unchanged.
- Resolved during verification: removed shared test imports were restored; the Docling fixture requires Python 3.10+ and therefore rejects the host's default Python 3.9. The core installer itself still supports Python 3.9.
- NOT RUN: fresh-session model behavior, live Google artifact workflows, real OCR/Docling conversion, and optional marketplace/plugin reconciliation. Fixture and deployment checks do not establish those outcomes.

Remote origin was verified as the public SSH `taekimax/codex-policy` repository with default branch `main`; fetch confirmed no divergence from `7538eaf` before this update. GitHub account and Git author match the repository owner. The current Git revision and its CI run are the authority for publication and platform status. Start a new Codex session to refresh global instructions and skill discovery. Older project-local instructions and externally managed system/plugin skills may still supply additional constraints; this task did not rewrite those layers. The catalog retains its historical marketplace decisions, so any later reconciliation should review its current plan.

## Cross-machine update

Normal core apply now converges fresh and existing installations without separately reconciling plugins. Retired-file backups remain private to each host; unknown files and project records are preserved. The six original symbolic target names remain recognized so an old interrupted installation can be recovered before retirement. No remote machine's Codex home is copied or modified by this checkout.

CI uses Python 3.12 on macOS, Ubuntu, and Windows, plus focused Python 3.9 core coverage. The Windows fake-CLI launcher uses the test interpreter, and temporary-path fixtures are portable. Local focused Python 3.9 tests passed. Windows and Linux execution await the published revision's CI run; POSIX-only extraction fixtures remain skipped on Windows. The README supplies per-platform pull/apply/verify instructions and distinguishes policy installation from extraction-runtime provisioning.
