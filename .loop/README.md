# Global environment review — 2026-09-09

## Request and scope

Review this host's global Codex settings, instructions, and skills for useful additions to the repository that shares the user's environment across machines. The follow-up authorizes committing and pushing the completed review and existing policy work. This review changes repository documentation and publishes the already prepared policy edits; proposed new skill ownership, runtime setup, and host-setting changes remain recommendations.

The inspected runtime is Codex CLI 0.153.2 on macOS. Findings below come from current files, the core plan/verify commands, the optional skill plan, and the supported plugin inventory. No live configuration, skills, account connections, or permissions were changed. The older audit below is historical evidence.

## Findings and recommended inclusion

| Priority | Finding | Recommendation |
| --- | --- | --- |
| Publish now | The live global guide and handoff template match the working checkout, but the keep-awake and revised implementation-handoff preferences are uncommitted. Two earlier local commits, `4cbd564` and `ad2052e`, are also ahead of the remote. | Publish this existing work with the review. It includes shared macOS delivery guidance, the handoff template, prerequisite and cleanup guidance, bounded keep-awake behavior, and the requested handoff orchestration preference. |
| Next addition | `naver-blog-to-notes` exists only in the host's user-skill directory and is absent from the repository catalog and installer. | Include its `SKILL.md` and `agents/openai.yaml` through the existing core transaction after making the prerequisites explicit: macOS, Apple Notes, supported Computer Use, and an available import path. Replace the fixed `node_repl` reference with the available runtime's documented interface. Preserve exact article text, image ordering, and destination rules. |
| Next addition | `context7-cli` is recognized as externally retained, but its customized instructions and reference are not distributed. A fresh core installation will omit it. | Consider moving its `SKILL.md`, `agents/openai.yaml`, and `references/docs.md` into reviewed ownership. Support host-appropriate executable discovery, align exact-version versus fallback guidance between files, and use narrow public-library queries rather than a full private question. Keep CLI installation and authentication separate. |
| Maintenance | The optional skill reconciler reports `plugins: blocked` and `connector skills: review` even though all ten required local plugin source checks match. | Review current connector packaging before revising the historical catalog. The selected GitHub cache version has no `skills` directory and lacks the required `yeet`; Gmail and Slack also lack the expected directories. Google Drive's skill set matches. This diagnostic does not establish failed account authentication. |
| Optional preferences | Model, reasoning, personality, and desktop preferences are preserved locally, so core deployment alone does not reproduce the complete interaction experience. | Keep a documented host setup choice. If uniform defaults are desired later, `personality = "pragmatic"` is a small candidate; model and reasoning choices must account for destination availability. Extend the existing owned-key mechanism only after choosing what should become enforced policy. |

The two proposed skill additions comprise five reviewed text files. No credentials, personal article examples, or machine-specific user paths were found in them. Adding them would require updating the core file inventory, optional catalog ownership/validation, repository allowlist, and installer acceptance coverage. Do not introduce a second copying or deployment mechanism.

## Current coverage

- **Instructions:** The canonical `global/AGENTS.md` and installed guide match byte-for-byte. No nonempty global override or home/parent instruction file was found. The installed handoff template also matches. The guide already addresses autonomy, scope, preservation, proportionate verification, communication, skills, signing prerequisites, and recovery; no additional generic policy layer is needed.
- **Owned configuration:** All three declared agent values match: six threads, depth one, and a 1,800-second job runtime. Other settings remain host-owned. Application/system instructions and session-specific tool availability are supplied by Codex and cannot be reproduced by copying `AGENTS.md` alone.
- **Managed skills:** All eleven files across `google-workspace-artifact-qa`, `local-document-extraction`, and `macos-app-delivery` match their installed copies. Their responsibilities remain distinct and useful. Retired Oracle Solver and Loop Init managed files are absent.
- **Other skill sources:** All five declared system skills are present. Context7's narrow invocation policy passes the existing check. The two generic skills under the separate user skill root are disabled. System and plugin caches should continue to be supplied by their owners rather than vendored here.
- **Local settings:** The host selects Astra with high reasoning and pragmatic personality. Desktop choices include steering follow-ups, showing context usage, and preventing sleep while running. Local notification commands, MCP process paths/environment, font availability, account connections, and project trust need host-specific setup rather than importing the complete live configuration.
- **Features:** The installed CLI reports `js_repl` and `terminal_resize_reflow` as removed. It reports `context_management` as under development and `prevent_idle_sleep` as experimental. The quoted `context_management.experimental_mode` key parses, but is not listed as a recognized CLI feature; successful parsing does not prove that it has an effect. None should be copied into portable policy merely because they exist locally. Stable app and memory capabilities still depend on the destination runtime; memory contents remain local.
- **Portability:** Core installation supports macOS, Linux, and Windows. The extraction launchers still require POSIX tools and separately provisioned dependencies. macOS delivery needs the destination machine's signing setup. Naver-to-Notes would be usable on Macs, while Context7 executable discovery needs POSIX and PowerShell wording. The handoff model names also require destination availability; the guide already allows an explicit user override.

## Verification and publication

- PASS: live core plan and verify; all managed sources and settings current, retired files absent, no override, clean transaction.
- PASS: supported plugin inventory and focused source checks for all ten required local plugins; current Google Drive skill set matches the catalog.
- FAIL: optional reconciliation cannot converge against the selected connector caches; it reports `action: blocked`. No reconciliation or cache repair was applied.
- PASS: all 47 acceptance tests under Python 3.12, including installation, preservation, rollback, retirement, handoff-template recovery, and optional-catalog fixtures.
- PASS: repository audit, whitespace and local-reference checks, and review of the intended diff including both previously unpublished commits.
- NOT RUN: this revision's remote CI at the time this record was committed; the configured macOS, Windows, Linux, and minimum-Python jobs run after publication.
- NOT RUN: live Notes import, Context7 network lookup, real OCR/Docling conversion, signing/delivery, fresh-session behavior, or installation on another physical machine. These are outside this review.

The verified publication destination is the public `taekimax/codex-policy` repository, `origin/main`, using SSH. Git author and the authenticated GitHub account match its owner. Fetch showed two local commits ahead and no remote-only commits. Publication includes those existing commits without rewriting them.

Official references used to check configuration and discovery: [configuration reference](https://learn.chatgpt.com/docs/config-file/config-reference) and [global instruction discovery](https://learn.chatgpt.com/docs/agent-configuration/agents-md). Current source and CLI results determine the host-specific findings above. Follow the README's pull/apply/verify sequence on another machine and start a new session after applying an update.

---

# Historical global instruction audit — 2026-09-06

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
