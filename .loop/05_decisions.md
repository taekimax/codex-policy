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
