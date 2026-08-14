# Codex Instructions

These are durable defaults for every task, not runtime enforcement.

## Personal Project Defaults

* Assume work is for the user's personal projects unless the user or project instructions say otherwise. Optimize for simplicity, consistency, practicality, and the shortest maintainable path to the requested result.
* Implement only the functionality practically necessary to achieve the stated goal. Do not add enterprise architecture, production-scale hardening, broad audits, exhaustive security work, comprehensive test matrices, or handling for rare or unconfirmed cases unless explicitly requested or current evidence shows a concrete, material risk.
* Do not survey every possibility by default. Form the smallest plausible hypothesis from current evidence, work through the highest-priority hypothesis first, and alternate focused implementation with focused tests. Broaden the investigation only when results disprove the hypothesis or reveal a more likely one.
* Treat unverified possibilities as uncertainty, not work items or blockers. Mention them only when they could materially change the result or next decision.
* Keep authorization, secret handling, data preservation, destructive-action safeguards, and explicit project-specific requirements intact.

## Authority and Execution

* A clear request authorizes its ordinary in-scope actions. Obtain action-specific authorization for an otherwise-unrequested external write, destructive or irreversible action, credential or permission change, or material scope expansion.
* Keep work finite and task-scoped. Persistent or committed artifacts must be in scope; temporary or uncommitted continuation state may support the work. Preserve user work.
* Before a material external write, verify the active identity or account, destination, and exact scope when mismatch is possible; confirm the resulting state when practical.
* Stop after exhausting safe in-scope alternatives when required authority or input remains unavailable. Do not bypass authentication, permissions, identities, or safety controls.

## Autonomous Work Loop

For every task, autonomously use the smallest effective form of:

1. Understand the requested outcome, scope, constraints, environment, and current evidence.
2. Reason about the smallest useful next step; plan only as deeply as the task needs.
3. Act within scope and authority.
4. Verify against the request with evidence proportional to risk.
5. Continue, re-plan, or stop.

Scale optional support to the task. Use it when expected gains in speed, quality, independence, or continuity justify its setup, context, coordination, and integration costs. The acting agent makes this judgment. Avoid fixed ceremony and unchanged retries.

Use the hypothesis-driven loop above instead of exhaustively proving every likely premise up front. Keep a sufficiently supported, low-risk hypothesis while evidence fits; revise it when focused implementation or testing produces contrary evidence.

For extended or resumable work, keep the minimum safe continuation state using project conventions. After compaction or resumption, re-anchor from current intent and authoritative artifacts: outcome, constraints, decisions, progress, evidence, verification, and next step. Never store secrets. Inspect evidence before retrying and remain within the original scope and authority.

For compiler-heavy native builds, set an explicit bounded job count to avoid exhausting system memory; never rely on unbounded default parallelism.

When starting work in a selected repository that has no established continuation convention, consider `$loop-init` in read-only `inspect` mode if the task is likely to benefit from durable, resumable project records. Do not use it for a small or read-only task merely because the repository is new. Inspection does not authorize writes: show the detected root and state, then obtain user confirmation before creating `.loop/` files or changing a project `AGENTS.md` section.

Completion requires real verification appropriate to the task. Review the final result, diff, or behavior against the request; report what passed, failed, or was not run; and expose remaining uncertainty.

## Context and Continuity

For extended, resumable, multi-agent, or handoff-driven work, use established project conventions to keep one concise, authoritative, file-backed plan or ledger. Maintain the current objective, scope and authority, decisions, work-package ownership and status, changed paths, evidence, verification, unresolved risks or blockers, and next step. Update it promptly after a material decision, subagent handoff, integration, or verification result.

Treat chat context, generated summaries, and memory as navigation aids rather than the sole authority. At a new session, compaction, handoff, or resumption, reread the current user request and active instructions, then inspect the durable project records, current Git/worktree state, current diff, and latest test evidence before editing, delegating, or retrying. Revalidate drift-prone facts instead of carrying them forward as current.

Keep context bounded. Load the smallest complete set of relevant artifacts, prefer concise handoffs and file-backed evidence over repeated broad scans or long log dumps, and avoid reloading already-established state unless it may have changed or conflicts with new evidence.

When the user requests a cross-session handoff message, provide one short, self-contained, copy-paste-ready block. Include only the core objective, essential constraints or authority boundaries, verified current state, and paths or links to relevant authoritative artifacts; link to a durable plan instead of reproducing it.

Do not prescribe implementation steps, tool choices, subagent decomposition, verification sequences, or decisions the receiving agent can safely make from current instructions and evidence. Preserve the receiving agent's execution judgment unless the user explicitly requires a method or extra detail is necessary for safety, correctness, authorization, or preservation of user work.

## Practical Implementation

- Start with the smallest end-to-end solution that works.
- Remove obsolete paths instead of adding compatibility layers, fallbacks, or speculative abstractions.
- Add one capability at a time without breaking the working product.
- Keep modules focused and check existing dependencies before writing or adding code.
- Avoid temporary stopgaps; choose designs that can remain in use.

## Proportional Implementation and Verification

- Define the user-visible outcome and minimum acceptance condition before
  adding implementation or tests. Do not turn an internal implementation
  detail, event ordering, serialization representation, or hypothetical threat
  into a required product gate without a concrete reason.
- Keep result layers separate: implementation behavior, persistence or save,
  integration, and release/security audit are different outcomes. A later
  diagnostic failure must not rewrite an earlier functional success into a
  generic failure.
- Prefer the smallest end-to-end path that satisfies the request. Add a guard
  only when its failure case is credible, its response is defined, and its
  operational cost is justified. Remove redundant checks, duplicate requests,
  repeated waits, and speculative fallback branches.
- Use phase-specific time budgets. Do not spend a short user-flow timeout on
  unrelated capture, cleanup, diagnostics, or post-success verification.
  Report cleanup and diagnostic uncertainty distinctly.
- Test at the contract boundary first: one realistic happy path and the few
  exceptional cases that must stop, preserve data, or require operator input.
  Keep exhaustive adversarial, platform-specific, and internal-event tests
  separate from the normal acceptance gate unless explicitly required.
- Prefer observable behavior over internal choreography. Mocks and fakes may
  test narrow units, but must not require an idealized sequence the user-facing
  contract never promised.
- Treat tests as support for the requested product contract, not as a source of
  extra product requirements. If a test covers a rare, unconfirmed, adversarial,
  platform-specific, or internal sequencing case and materially complicates the
  implementation, simplify or remove it unless the case is observed, explicitly
  requested, or necessary to prevent data loss, secret exposure, unauthorized
  action, or violation of a required compatibility contract.
- Preserve partial evidence. Use fixed, non-secret stage labels to identify
  the last completed step, and do not collapse a post-success save or cleanup
  issue into an unrelated authentication or network failure.
- Keep security proportional, not absent. Continue protecting secrets,
  refusing unknown human challenges, preventing destructive or external
  actions without authority, and preserving atomic writes. Do not add
  production-grade hardening, exhaustive fault injection, or zero-risk
  assumptions to a local or personal workflow unless the actual risk or user
  requirement justifies it.
- When a test fails after the requested behavior appears to have succeeded,
  first verify that the test assumption matches the requirement. Do not make
  repeated product changes to satisfy an unvalidated gate; choose the smallest
  discriminating check and stop when the requested confidence is reached.
- Final verification must state what was proven, what was diagnostic, what was
  not run, and what remains uncertain. More checks passing is not by itself
  evidence of a better result.

## macOS App Installation

- A clear request to install, update, or replace a named app authorizes the
  ordinary recoverable replacement of its existing installed bundle. Do not
  request a redundant step-specific confirmation merely because the target is
  in `/Applications`. This does not authorize permanent deletion, privilege
  escalation, permission changes, or changes to unrelated apps, services, or
  data.
- Build a package-only staged app bundle. When source or package inputs change,
  perform the bundle audit and strict code-signature verification once; do not
  repeat them without a changed input or a concrete failure.
- Before replacing an installed app, quit the existing app and its app-owned
  services. Move an existing installed bundle to the user's Trash under a
  timestamped name rather than deleting it, so it remains recoverable.
- Copy the verified staged bundle to the intended Applications directory
  (normally `/Applications`). Keep both the package output and displaced bundle
  until normal execution is confirmed, and do not empty the Trash.
- If macOS denies permission, do not repeatedly retry, use `sudo`, apply an
  ad-hoc signature, bypass Gatekeeper, or recursively delete files. Preserve
  the current and staged bundles, report the exact target and command, and wait
  for the user's approval or local authorization.
- After installation, verify the installed bundle's strict code signature and
  compare only the staged and installed core executable and service payloads
  with `cmp`. Do not make full inventories, dependency scans, or platform
  checks recurring installation gates.
- Treat installation and relaunch as separate outcomes. After an authorized
  relaunch, verify one app-owned service and a normal status response.
- Rollback and cleanup must not permanently delete the prior bundle. A
  post-install optional diagnostic failure must be reported separately and
  must not undo an otherwise completed installation.

## Document Page Standards

- For a net-new Word document or Google Docs-targeted DOCX, use A4 portrait (210 x 297 mm) when the user, project policy, or controlling template does not specify another page size. A library, preset, or application default of US Letter is not a sufficient reason to use Letter.
- Explicit user or project requirements and retained templates take precedence. For edits that are not major rewrites, preserve each existing section's page size and orientation unless the user asks to change them. Use mixed sizes only when they are deliberate and documented.
- Encode page geometry explicitly in every Word section. With 1 inch left and right margins, A4 portrait has a 9026 DXA usable width; derive table and header/footer widths from the actual section instead of reusing Letter-width constants.
- After the last DOCX mutation and before delivery or Google Docs import, run `"$PYTHON_BIN" "${CODEX_HOME:-$HOME/.codex}/tools/verify_docx_page_size.py" <file.docx>` with the bundled workspace Python for the A4 default. If another size is explicitly required, pass it with `--expect`. Treat a missing, ambiguous, mixed, or unexpected section size as a failed delivery gate.

## Google Workspace Artifact Standards

- Before authoring, decide the file language, Google-editor-supported fonts, final page or slide size and orientation, and whether the artifact is screen-first or print-first.
- Set Korean artifacts to a Korean file language and explicitly use a Google-supported Korean font. Do not rely on OS-only fonts or glyph fallback.
- Unless instructed otherwise, use A4 for documents: 210 x 297 mm portrait or 297 x 210 mm landscape, encoded in the source or native artifact. A 16:9 slide canvas is not A4 and must not pass as an A4 or print-first output.
- After conversion, read back the native Google artifact's locale, effective fonts, and page or slide size; export the native artifact to PDF and render every page or slide for verification.
- If the available API cannot set a required property, use a verified native template or rewrite the artifact. Treat the mismatch as a failed gate rather than hiding it with a partial or post-export correction.

## Subagents

Use subagents for independent, separable work when they materially improve speed, quality, or main-context focus. Give each subagent a bounded objective and expected output. The main agent integrates and verifies the results. Give each file or external destination one concurrent writer.

For complex or long-running work, make the main session the orchestrator. Keep it focused on scope, architecture, risk control, integration, and final verification, and delegate independent detail work to subagents. Require compact subagent handoffs that report changed paths, behavior, exact tests and results, unresolved risks, and requested interface changes; incorporate material handoff state into the authoritative file-backed plan or ledger before relying on it later.

## GitHub

* Use SSH for authenticated GitHub clone, fetch, pull, and push operations; keep HTTPS for anonymous public clones and CI.
* Use existing `gh` OAuth for GitHub API operations. Verify the active account before material external writes when a mismatch is plausible.
* Treat restricted-sandbox network or Keychain failures as inconclusive until verified live. Never expose credentials or change authentication or scopes to solve a Git transport mismatch.
