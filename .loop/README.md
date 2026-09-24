# Common behavior and authoring policy — 2026-09-24

## Current outcome and authority

Completed source edits, local application, and verification. The request adapts Hermes common principles to Codex coding, writing, research, and conversation for practical usefulness, simplicity, and consistency. The repository started clean on `main`. Hermes was reference-only. No commit, push, external delivery, restart, model/authentication/permission change, memory edit, or data-access change was authorized or performed. There is no pending user decision; start a new Codex session for the full refreshed instruction and skill catalog.

## Loading and ownership

- Local CLI: 0.156.1. `CODEX_HOME` was unset; the target was `~/.codex`. No global or repository `AGENTS.override.md`, custom instruction file, inline developer instruction setting, or project config override was active. The live session catalog included the reviewed user skills and current artifact plugins.
- `global/AGENTS.md` remains the common-policy source. Root `AGENTS.md` remains repository guidance. The existing transactional installer owns local deployment and backups.
- Settings own three agent limits only. `global/config.owned.toml`, `global/owned-keys.txt`, and live `config.toml` stayed unchanged; behavior preferences require no new configuration key.
- Adopted the existing standalone `codex-design` and `project-handoff` skills into `global/skills/` and the same installer, expanding the managed inventory to seven skills / 24 files. Their previous local contents were backed up by normal apply. Other user skills and unrelated dirty work in the separate skills checkout remain preserved.
- Reviewed live Context7 description and Naver copying improvements before explicitly incorporating them into canonical sources. This resolves the pre-existing drift without reverting the newer text/plain-file mode or introducing reverse-sync tooling.
- System/plugin packages retain their owners. Their generic suggestions are scoped through user-level global preferences, not cache edits, forks, wrapper skills, or a new mandatory call chain. Optional plugin reconciliation was not applied.

Official loading references: [instruction discovery](https://learn.chatgpt.com/docs/agent-configuration/agents-md) and [skill activation](https://developers.openai.com/plugins/concepts/skills). Installed paths and the actual session catalog were checked separately from documentation.

## Policy decisions

- Common guidance now covers usable results, reader/context, source-grounded clarification, conditional judgment, material uncertainty, concise writing, and necessary citations. Internal evidence verification is separate from citations displayed to the reader.
- No blanket web/JSG/Heatseeker search, evidence table, tests, or multi-agent requirement. Preserve explicit specialist source requirements and artifact fidelity/rendering checks.
- Use one primary authoring route. Native Google templates/edits follow the Google-specific route; ordinary new decks use Presentations; explicit or specialized reconstruction/template/narration work uses PPT-Master. Existing task authorization satisfies routine workflow confirmations. Extra style-sample retrieval and follow-up sections are conditional on actual usefulness.
- Useful delegation uses the latest supported Luna/Max or SOL/High workers, Astra/High final verification, and acting-agent integration. Active global/handoff instructions contain no pinned model version.
- `codex-design` now has a narrow visual-work trigger and conditional references/checks; behavior-only frontend fixes do not load it. Its entrypoint fell from 152 to 33 lines. References no longer force detector passes, generic risk sections, fixed reports, or repeated approval. Existing design/source and Impeccable boundaries remain.
- `project-handoff` reuses the global guidance/template. macOS replacement details moved to the delivery skill, keeping the global entry brief. Google artifact QA distinguishes requested audit reports from ordinary artifact delivery. Naver exact-copy checks preserve source order and graphics while avoiding unnecessary repeat retrieval or fixed reporting fields.
- Active market research, JSG retrieval, local extraction, and third-party PPT workflows were inspected and retain their specialist boundaries. Disabled legacy skills remain disabled and untouched.

## Verification

- PASS: 49 existing acceptance tests, covering fresh installation, added skill deployment, host-setting preservation, local edits/backups, rollback, recovery, retirement, and catalog consistency. The initial repository-index check required the newly added files; a private candidate index made the full suite and audit pass while preserving the actual index.
- PASS: repository audit, focused diff, all seven skill validators, and relative Markdown references. No new wording-matching tests were added.
- PASS: core `plan`, `apply --yes`, `verify`, and post-apply `plan` (`action: none`, transaction clean). Global guide, handoff template, and all 24 skill files are byte-identical to source (26/26 targets).
- PASS: live `config.toml` is byte-identical to the pre-apply snapshot. All 398 baseline plugin/system instruction files are unchanged. Across 830 captured instruction/config files, all 12 changed files are intended managed targets; no unexpected change or missing baseline file was found. The template was checked separately.
- PASS: independent Astra High source review and eight prompt simulations: simple A4 question; familiar-note cleanup; new external-fact research; requested engineering judgment; team memo; DOCX template edit; narrow CSS vs behavior fix; authorized native PPTX edit. Simulations retained necessary clarification, citations, technical gates, and rendered QA without routine extra sections.
- PASS: Astra High final installed readback and preservation review. Recovery files remain in `$CODEX_HOME/.codex-policy/transactions/20260924T062043Z-000085f2/`.
- NOT RUN: a fresh-session behavior test, real DOCX/PPTX/Google authoring, live Notes import, cross-platform execution, or external delivery. Source/prompt simulation and byte parity do not prove those workflows. The current session received refreshed global text after apply; this does not prove the complete skill/plugin catalog reloaded.

## Remaining step

Use a new Codex session to load the complete updated guidance. Source changes remain uncommitted and unpublished, as requested. Other hosts are unchanged.

---

# Historical workflow review integration — 2026-09-10

## Current request and scope

Review the completed Codex/Hermes workflow changes and update this repository with the applicable portable guidance. Preserve existing policy edits and newer shared-skill work. This request covers local source updates and verification; earlier publication permissions recorded below are historical.

The starting revision is `05421ed`. The working global guide already contains the reviewed worker contract and other local policy edits, and matches the installed guide. Keep those edits. Hermes-specific routing, profile instructions, citation helpers, and Codex bridge behavior belong to their existing owners and are not copied into this repository.

## Changes

- Retain native delegation, scoped worker inputs, complete/partial/blocked returns, and acceptance by the requesting agent. Carry required source and access constraints into the worker task.
- Add concise evidence guidance: tie decisive claims to actual sources/artifacts, preserve dates and material limitations, separate facts from calculations and interpretation, and retain unresolved conflicts. Reuse the existing task record and avoid resetting another active task's evidence.
- Make checks, evidence locations, blockers, and the completion condition explicit in the existing handoff template. No new ledger, scheduler, orchestration framework, or plugin dependency is introduced.
- Preserve host-owned settings and the existing installation mechanism. The prior mixed Codex/Hermes test count and isolated timing samples are historical evidence, not validation of this repository revision or proof of general speed gains.

## Verification

- PASS: all 49 existing acceptance tests under Python 3.12 (23.736 seconds), including handoff-template drift, backup, failure recovery, and preservation of host settings.
- PASS: repository audit, focused source diff, and whitespace checks. The pre-existing global policy text remains intact apart from the deliberate source/access constraint and evidence additions.
- PASS: live core plan/apply/verify. Only the global guide and handoff template needed deployment; the final plan reports no remaining changes. Installed bytes match source.
- PASS: the live configuration and both owned configuration sources remained byte-identical. Managed skills remain current.
- NOT RUN: fresh-session model behavior, new research latency/cost benchmarks, or Hermes runtime checks. These wording/template changes do not establish improvements in those layers.

Source and local installation are complete. Start a new Codex session to load the revised guide. No commit or push has been performed for this request; other machines have not been updated.

---

# Historical shared user skills update — 2026-09-09

## Current request and scope

Add the proposed Context7 and Naver-to-Notes skills and implement useful related improvements. The user explicitly excludes optional preferences because they may vary across machines. The conversation also authorizes commit and push after completion. Implement through the existing core installer, preserve local configuration and user files, verify the result, and publish the changes.

The implementation starts from `968a779`. The earlier environment review found the existing global guide, agent settings, three managed skills, and handoff template current on this Mac. It also found two unmanaged user skills and an optional connector check blocked by app-only bundles. The historical September 6 audit below records earlier decisions; it does not override this request.

## Implemented changes

- Include all five reviewed text files for `context7-cli` and `naver-blog-to-notes` in core deployment. Fresh and existing hosts use the same backups, rollback, preservation, and verification path. There are now five managed user skills with sixteen files.
- Make Context7 command discovery work with POSIX shells and PowerShell, align version selection and query privacy between its instructions and reference, and preserve its narrow invocation rule. Keep CLI installation and authentication separate from policy deployment.
- Make the Notes workflow explicitly depend on macOS, Apple Notes, supported Computer Use, and a compatible text import path. Follow current tool instructions instead of naming an obsolete runtime. Preserve exact article text, paragraph and image order, destination selection, and recoverable cleanup.
- Replace Context7's special external-skill check with the same source comparison used for other managed skills. Derive optional catalog ownership validation from its managed inventory instead of repeating that list again.
- Recognize complete app-only connector packages through their plugin manifest and app file. A missing skills directory remains a problem when the plugin declares skills or cannot establish a complete app-only package. Keep existing checks for unreviewed and missing skill sets.
- Support standard Git metadata files in the repository audit so detached worktrees can run the same checks as the main checkout. Retain content, index, origin, and reference checks; validate that Git resolves to the audited checkout.
- Leave `global/config.owned.toml` and `global/owned-keys.txt` unchanged. No model, reasoning, personality, desktop, or runtime-feature defaults are added. Credentials, permissions, accounts, application dependencies, and private runtime data remain host-local.

Current GitHub, Gmail, and Slack package manifests each declare an app and no skills; their app files are present. The original diagnostic treated these deliberately skill-free packages as damaged bundles. This implementation corrects the packaging assumption without changing account connections, plugin choices, or existing skill-disable policy.

## Verification

- PASS: both skill validators, metadata preservation, and relative reference checks.
- PASS: all 49 acceptance tests under Python 3.12, including installation of every added file, backup and rollback of existing local edits, preservation of unknown skill files and host preferences, drift detection for metadata and reference text, complete versus incomplete app-only connector packages, and an actual linked-worktree audit.
- PASS: repository audit, intended diff, whitespace, and local-reference checks. The first run exposed the worktree metadata assumption; the corrected full suite passed.
- PASS: live core plan/apply/verify. Only the Context7 instructions/reference and Notes instructions required an update; metadata already matched. All sixteen managed skill files now match their sources.
- PASS: the live global configuration remained byte-for-byte unchanged, as did the two repository-owned configuration sources.
- PASS: read-only optional skill plan and verify now report `action: none` and verification passed. No plugin reconciliation was applied. Connector status remains `not_present` because one catalog connector is absent; the installed packages no longer produce a false block.
- NOT RUN: live Context7 network lookup, Notes import, real document conversion, and fresh-session model behavior. Installing the skill text does not establish those workflows or provision dependencies.

Publication uses the verified SSH `origin/main` destination and existing GitHub identity. Remote platform CI runs after publication; local checks do not establish execution on Windows or Linux.

The core installer and catalog inspection remain separate. Core deployment does not execute plugin reconciliation. Start a new Codex session after applying an update so the instructions and skill discovery refresh. Other machines should pull the published revision and run the existing plan/apply/verify sequence.

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
