---
name: oracle-solver
description: Obtain a fresh, isolated, high-effort judgment for difficult planning, blockers, or consequential reviews through a headless Codex worker pinned to gpt-5.6-sol with xhigh reasoning. Use when the user explicitly requests Oracle, or when the calling agent judges that an independent perspective is likely to improve an important decision enough to justify its latency, token, context, and integration costs. Do not use it as ceremony or substantially repeat an unchanged request.
---
# Oracle Solver

Use Oracle to synthesize difficult evidence, expose assumptions, unblock reasoning, and challenge consequential decisions. Account for its latency, token and context cost, request preparation, and integration work. Treat it as an independent worker, not a subagent; it knows only the context supplied to it.

## Preserve the boundary

* Invoke only `scripts/run_oracle.py`; do not imitate an oracle with an ordinary subagent or the current model.
* Use the installed Codex login through the normal `codex` executable. Do not request, copy, refresh, or alter credentials, and do not pass API keys.
* Treat installation and use of this skill as standing user authorization to transmit the minimum task-relevant request packet, local file content, and command output to OpenAI's ChatGPT/Codex service for the Oracle review. Do not request separate confirmation for each invocation. This authorization does not cover secrets, unrelated private data, or transmission to any other external destination.
* Keep the worker ephemeral, approval-free, and pinned to `gpt-5.6-sol` with `model_reasoning_effort="xhigh"`.
* The runner creates a disposable current-state worktree or filesystem snapshot of the requested workspace, plus a fresh temporary scratch workspace where tools and multi-agent workers may act. The Oracle worker receives only the disposable review workspace and must not mutate it, the source workspace, or external state. The runner consumes the validated response, emits it through the handoff, and removes both temporary workspaces by default.
* Refuse to invoke when `ORACLE_SOLVER_ACTIVE=1`. The runner also enforces this guard and sets it for the child.
* Treat the Oracle verdict as an independent judgment for its planning, problem-solving, or review question under the evidence, constraints, and conditions supplied at invocation time. This is not a claim of infallibility or permanent correctness. It cannot authorize writes, deployment, destructive actions, purchases, permission changes, messages, or scope expansion.
* Do not leak secrets or irrelevant private material into the request packet. Point to the minimum local evidence the oracle should inspect.

## Decide whether to invoke

Invoke Oracle when the user explicitly requests it. Otherwise, the calling agent decides whether a bounded call is likely to improve the next important decision enough to justify its costs. This judgment may favor Oracle for difficult planning, stalled problem-solving, or a valuable independent challenge, without requiring a fixed threshold or prior sequence of attempts.

Prefer direct inspection and normal validation for routine work. Do not invoke Oracle merely as ceremony, and do not substantially repeat an unchanged request. Apply the same value judgment to follow-ups: prior use neither requires nor forbids another call. If the exact worker cannot run, report that fact rather than substituting another reviewer.

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

Use empty arrays where needed. Separate facts from hypotheses, include only task-relevant evidence and uncertainty, and do not tell Oracle the answer you hope to receive.

For planning, request independently verifiable slices with outcomes, scope and non-goals, dependencies, invariants, evidence, risks or stop conditions, and acceptance evidence. Leave routine implementation mechanics to the acting agent. Ask for exact sequencing, pseudocode, or minimal code only when a consequential dependency, concrete ambiguity, or evidenced failure requires it.

## Run the oracle

Use a safe request file or stream JSON over stdin. The default invocation is ephemeral and does not write the requested workspace:

```text
python3 <skill-dir>/scripts/run_oracle.py \
  --workspace <primary-target-root> \
  --request-file <request.json>
```

The runner mirrors the current workspace, including dirty and untracked files, into a disposable review worktree or snapshot. A Git worktree is used when available; non-Git directories use a filesystem snapshot. The source workspace is never used as Oracle's review target, and the disposable copy is cleaned after the response is consumed. The default JSON handoff contains the validated detailed report in `report_markdown`, together with its digest; the report remains available to the calling agent without creating a file.

When a durable report is explicitly needed, add a managed Markdown document path inside the source workspace:

```text
python3 <skill-dir>/scripts/run_oracle.py \
  --workspace <primary-target-root> \
  --request-file <request.json> \
  --document <existing-directory>/<review-name>.md
```

That explicit `--document` is the only source-workspace write. Choose a new `.md` path in an existing directory, or reuse a document previously created by this runner. Never target a user-authored file. The runner sets timeout at 81 minutes. When the command runs asynchronously, check for its result with exponential backoff at 1, 2, 4, 8, 16, 20, 30 minutes. If the host requires more frequent keepalive updates, use them only to preserve liveness rather than to restart or duplicate the Oracle request. Do not start another oracle concurrently for the same decision.

The runner returns exit code 0 only after validating that every request question is answered, rendering the report, consuming it, and cleaning the disposable review and scratch workspaces. With `--document`, it also atomically publishes the managed document and returns `document_path` and `document_sha256`. Standard output is a JSON handoff containing status, verdict, confidence, a bounded summary, and the report digest; ephemeral runs additionally contain `report_markdown`, while persistent runs contain `document_path`. Diagnostics are bounded and never include the request packet.

When cleanup is explicitly in scope, delete only a document produced by the runner:

```text
python3 <skill-dir>/scripts/run_oracle.py \
  --delete-document <existing-managed-review.md>
```

The runner refuses symlinks, non-Markdown paths, missing parents, oversized files, and replacement or deletion of files without its ownership marker. The cleanup contract applies to both clean and failed review attempts; a cleanup failure is reported as an Oracle-runner failure rather than silently treated as success.

## Interpret the response

For an ephemeral run, assess the `report_markdown` in the handoff; for a persistent run, open the managed document. In either case, assess the verdict, scope, evidence, risks, recommendations, assumptions, and unknowns. Check material recommendations against current evidence and the user's authority boundary. Explain meaningful discrepancies rather than treating the judgment as infallible or valid after its evidence and conditions change.

After review, continue the parent task within its original authority. If implementation is requested, re-check accepted advice against current evidence and translate it into bounded task packets rather than forwarding the full report by default. Preserve each slice's outcome, scope, constraints, rationale, ownership, acceptance evidence, and stop conditions while leaving implementation choices to the acting agent. Increase specificity only at a demonstrated ambiguity or failure; reassign judgment-heavy work instead of turning Oracle guidance into an implementation script. If the user requested review only, report the oracle result and your verification without implementing.

Keep the user-facing response short: state the verdict and confidence, summarize the answer in one or two sentences, and provide a clickable absolute path only when a persistent document was requested. Do not duplicate the detailed findings in chat unless the user asks.
