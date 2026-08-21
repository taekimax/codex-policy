# Decisions

Append decision records below. Do not rewrite prior decisions unless correcting a factual error.

## Decision Record

- Date: 2026-07-22
- Decision: Treat Loop Init as an explicitly managed, opt-in reviewed user skill, not a global mandatory workflow.
- Reason: Durable state is useful for extended work, but mandatory roles and artifact creation conflict with the policy’s smallest-effective-support rule.
- Alternatives Considered: Leave the runtime skill unmanaged; add it as a retained system skill; apply it implicitly for ordinary repository tasks.
- Reversal Condition: Reconsider only with evidence that an expanded default is needed and does not create policy conflicts.

- Date: 2026-07-22
- Decision: Let global policy select Loop Init for read-only inspection of suitable new-repository work, but retain user confirmation as the only authority for initialization.
- Reason: This makes durable continuation available without turning every new repository or small task into a mandatory workflow.
- Alternatives Considered: Keep explicit user invocation as the only trigger; automatically apply Loop Init to every new repository.
- Reversal Condition: Reconsider if policy-triggered inspection proves noisy or agents cannot reliably distinguish durable work from small tasks.

- Date: 2026-08-07
- Decision: Require extended, resumable, multi-agent, and handoff-driven work to keep one concise authoritative project plan or ledger and to re-anchor from current instructions, durable records, Git/diff state, and test evidence after a new session, compaction, handoff, or resumption.
- Reason: Existing global guidance covered minimum continuation state but did not explicitly require prompt ledger updates after subagent handoffs, compact evidence-bearing handoffs, or current worktree/diff/test inspection before resumed edits and delegation.
- Alternatives Considered: Keep the shorter existing paragraph; make `.loop/` mandatory globally; rely on chat summaries or memory as the handoff record.
- Reversal Condition: Narrow the rule if it creates repeated ceremony for small tasks; project conventions and the smallest-complete-artifact rule remain the guard against that outcome.

- Date: 2026-08-07
- Decision: Keep cross-session copy-paste handoffs short and outcome-focused, point to authoritative durable records instead of restating detailed plans, and avoid constraining implementation choices the receiving agent can safely make.
- Reason: Overly prescriptive handoffs duplicate durable plans, consume context, and unnecessarily restrict the receiving agent's evidence-based judgment.
- Alternatives Considered: Reproduce the full plan in every handoff; require fixed implementation steps, tools, delegation structure, and verification sequences.
- Reversal Condition: Add specificity only when explicitly requested or necessary for safety, correctness, authorization, or preservation of user work.

- Date: 2026-08-10
- Decision: Manage `google-workspace-artifact-qa` as a two-file reviewed user skill installed by the core policy workflow, while keeping the official Google Docs, Google Slides, and Presentations plugin sources untouched.
- Reason: The QA contract is user-specific and cross-cuts multiple authoring routes; a separate managed skill can fail closed on native output without forking official skills.
- Alternatives Considered: Patch official plugin caches; put all API-specific checks in global policy; rely only on authoring-skill visual checks.
- Reversal Condition: Reconsider packaging only if an official stable QA surface provides the same locale, effective-font, physical-size, native-export, and read-only guarantees.

- Date: 2026-08-10
- Decision: Treat unavailable required readback as `BLOCKED`, not `PASS`, and require a verified native template or separate rewrite when presentation-wide properties cannot be set.
- Reason: Locale and page-size defects cannot be safely hidden through partial text edits or export scaling.
- Alternatives Considered: Best-effort pass with warnings; automatic target mutation during QA.
- Reversal Condition: Narrow the rule only if the native APIs gain authoritative read/write support and the user separately authorizes repair.

- Date: 2026-08-21
- Decision: Replace the fixed complex-work orchestrator and delegation default with an expected-value choice between direct execution and orchestration.
- Reason: Task length or agent count alone does not justify separate planner, generator, evaluator, or re-review roles; concrete coordination or consequential-review value must justify their cost.
- Alternatives Considered: Keep the mandatory orchestrator wording; require independent evaluation for every completion candidate.
- Reversal Condition: Add a mandatory role only for a specific workflow with evidence that self-review cannot reliably detect a costly failure.

- Date: 2026-08-21
- Decision: Keep current request, contract, plan, and status separate from historical decisions, evaluations, hashes, and completed logs.
- Reason: Completed-task evidence was occupying active Loop files and could carry superseded gates into unrelated work.
- Alternatives Considered: Preserve every prior task in the active files; delete all historical evidence.
- Reversal Condition: Retain an older requirement as active only when the current user request or policy explicitly adopts it.

- Date: 2026-08-21
- Decision: Publish the completed policy refinement to the verified public SSH `origin/main` after rerunning the repository release gates.
- Reason: The user separately authorized system application, commit, and push after the source and live policy had already passed focused verification.
- Alternatives Considered: Leave the verified change uncommitted; reconcile the unrelated plugin-policy drift before publication.
- Reversal Condition: Stop publication if identity, remote visibility, ancestry, final gates, or push destination do not match the repository contract.
