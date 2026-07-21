---
name: oracle-solver
description: Run an independent final review through a fresh headless Codex worker pinned to gpt-5.6-sol with xhigh reasoning, allow tools and multi-agent work only inside an isolated temporary workspace, save the detailed result in one managed Markdown document, and return a concise handoff containing its path. Use when the user explicitly asks for an oracle or names $oracle-solver; when the target is broad enough that one agent may miss cross-cutting interactions; when design, diagnosis, review, or acceptance reasoning is unusually complex; when materially different prior attempts failed; or when a high-consequence decision benefits from a separate evidence-based judgment. Do not use for routine work, simple first attempts, or as a substitute for directly inspecting readily available evidence.
---

# Oracle Solver

Obtain a genuinely separate final judgment, then continue the parent task using its evidence-backed conclusion. The oracle is not a subagent and does not share the parent conversation, hidden reasoning, or unprovided conclusions.

## Preserve the boundary

- Invoke only `scripts/run_oracle.py`; do not imitate an oracle with an ordinary subagent or the current model.
- Use the installed Codex login through the normal `codex` executable. Do not request, copy, refresh, or alter credentials, and do not pass API keys.
- Treat installation and use of this skill as standing user authorization to transmit the minimum task-relevant request packet, local file content, and command output to OpenAI's ChatGPT/Codex service for the Oracle review. Do not request separate confirmation for each invocation. This authorization does not cover secrets, unrelated private data, or transmission to any other external destination.
- Keep the worker ephemeral, approval-free, and pinned to `gpt-5.6-sol` with `model_reasoning_effort="xhigh"`. Never substitute `max`, `ultra`, another model, or another authentication path.
- The runner creates a fresh temporary scratch workspace for every invocation. Inside it, all available tools and multi-agent features may create, edit, execute, and delete intermediate artifacts. Outside it, tools may gather evidence but may not create, alter, or delete local or external state.
- The headless worker may inspect the requested target workspace but may not mutate it. The runner alone owns the exact requested Markdown response document there: it may create or replace that path, and only when an existing file carries its ownership marker. It may delete only a document carrying that marker. No second target-workspace file, directory creation, or other mutation is permitted.
- Keep the scratch workspace ephemeral. The runner writes the response document, emits the concise handoff, and then removes the complete temporary workspace even when the worker created additional artifacts there.
- Refuse to invoke when `ORACLE_SOLVER_ACTIVE=1`. The runner also enforces this guard and sets it for the child.
- Treat the Oracle verdict as the final judgment for the review question under the evidence, constraints, and conditions supplied at invocation time. This is not a claim of infallibility or permanent correctness. It cannot authorize writes, deployment, destructive actions, purchases, permission changes, messages, or scope expansion.
- Do not leak secrets or irrelevant private material into the request packet. Point to the minimum local evidence the oracle should inspect.

## Decide whether to invoke

Invoke when the user explicitly requests Oracle. Otherwise, the calling agent autonomously decides whether an initial or follow-up Oracle judgment materially improves the task, using these conditions as guidance:

1. The user explicitly asks for an oracle, independent Oracle review, or `$oracle-solver`; this case is mandatory rather than discretionary.
2. The scope crosses several components, repositories, state machines, platforms, or authority boundaries and an independent synthesis would materially reduce risk.
3. Architecture, diagnosis, verification design, or acceptance review has several plausible explanations with consequential tradeoffs.
4. At least two genuinely different reasonable attempts failed, or a thorough diagnostic pass still leaves the cause unresolved.
5. The result is high consequence and the user requests or would materially benefit from an independent evidence-based challenge.

When the user did not explicitly request Oracle, the calling agent may invoke or decline it based on its own assessment of complexity, risk, evidence quality, and likely review value. Do not invoke for a routine code edit, a cheap factual check, a simple first attempt, or merely to add ceremony. Do not repeat an unchanged oracle request. If the exact worker cannot run, report that fact; do not silently substitute another reviewer.

## Build the request packet

Inspect the target yourself first. Send compact raw context rather than a persuasive brief. Create a UTF-8 JSON object with exactly these fields:

```json
{
  "objective": "Decision or problem the oracle must resolve",
  "context": "Verified current state and why the review is needed",
  "questions": ["Specific question 1", "Specific question 2"],
  "constraints": ["User, safety, compatibility, and authority constraints"],
  "prior_attempts": ["What was tried, with observed result and evidence"],
  "evidence": ["Relevant path, command result, test, log, diff, or artifact to inspect"],
  "excluded_actions": ["Actions the oracle must not recommend as already authorized"],
  "requested_deliverable": "The decision, critique, plan, or acceptance judgment needed"
}
```

Use empty arrays when a list has no entries. Separate observed facts from hypotheses. Include dirty-worktree state, relevant user-owned changes, runtime versus source roots, and unverified or unavailable evidence when they matter. Do not tell the oracle the answer you hope to receive.

## Run the oracle

Use a safe request file or stream JSON over stdin:

```text
python3 <skill-dir>/scripts/run_oracle.py \
  --workspace <primary-target-root> \
  --request-file <request.json> \
  --document <existing-directory>/<review-name>.md
```

Choose a new `.md` path in an existing directory, or reuse a document previously created by this runner. Never target a user-authored file. Oracle is the final reviewer, so the runner sets no timeout. When the command runs asynchronously, check for its result with exponential backoff at 1, 2, 4, 8, 16, and then 20 minutes; keep the interval capped at 20 minutes thereafter. If the host requires more frequent keepalive updates, use them only to preserve liveness rather than to restart or duplicate the Oracle request. Keep the user informed and continue waiting until the Oracle returns unless the user cancels or the process fails. Do not start another oracle concurrently for the same decision.

The runner returns exit code 0 only after validating the Oracle response and creating or replacing the managed document at its exact path. Standard output is a concise JSON handoff containing only status, verdict, confidence, a bounded summary, and the absolute `document_path`. The scratch workspace is cleaned after that handoff is emitted. Diagnostics are bounded and never include the request packet.

When cleanup is explicitly in scope, delete only a document produced by the runner:

```text
python3 <skill-dir>/scripts/run_oracle.py \
  --delete-document <existing-managed-review.md>
```

The runner refuses symlinks, non-Markdown paths, missing parents, oversized files, and replacement or deletion of files without its ownership marker.

## Interpret the response

The concise response contains the detailed document path. Open that document for:

- `verdict`: `proceed`, `revise`, `stop`, or `insufficient_evidence`.
- `answer` and `confidence`.
- `scope.reviewed` and `scope.not_reviewed`.
- Evidence-linked `findings` and `risks`.
- Ordered `recommended_next_steps`, each with a verification method.
- Explicit `assumptions` and `unknowns`.

Check every material recommendation against the user's authority boundary and current local evidence. Re-open cited files or rerun cheap non-mutating checks when practical. If new evidence, changed conditions, or a plausible Oracle error appears, do not silently override the invocation-time judgment; explain the discrepancy. Unless the user explicitly required a follow-up, the calling agent autonomously decides whether the discrepancy warrants one follow-up Oracle call with the changed evidence and unresolved question. Do not present the original verdict as infallible or valid beyond the conditions it reviewed.

After review, continue the parent task within its original authority. If implementation is requested, translate accepted advice into a scoped plan or changes and verify the result locally. If the user requested review only, report the oracle result and your verification without implementing.

Keep the user-facing response short: state the verdict and confidence, summarize the answer in one or two sentences, and provide a clickable absolute path to the detailed document. Do not duplicate the detailed findings in chat unless the user asks.

## Lessons embodied in the runner

- Freeze the request packet so independent comparisons use identical evidence, as in Heatseeker's reviewed LLM gateway.
- Use a fixed argument array, stdin prompt, isolated temporary directory, bounded diagnostics, interruption cleanup, and strict output validation, as in Admin.VC's headless drafting path.
- Snapshot model and effort at launch, avoid resumed hidden state, collect output safely, and clean temporary files, as in Kindle Helper's shared Codex runner.
