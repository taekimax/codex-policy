---
name: loop-init
description: Use when the user explicitly asks to initialize one selected project repository with a project-local .loop workspace, or when applicable global or project policy identifies a new repository task likely to benefit from durable, resumable records. Policy-triggered use is inspect-only until the user confirms the detected root and mode; it creates no global policy or configuration.
---

# Loop Init

## Purpose

Initialize a small, project-local `.loop/` workspace when durable project records will materially improve an extended or resumable task. `.loop/` records context; it never overrides an explicit current user instruction, existing repository policy, or verified source and test evidence.

## Boundaries

- Use after the user explicitly requests initialization, or when applicable global or project policy identifies a selected new repository task that is likely to benefit from durable, resumable records.
- A policy-triggered use starts with read-only `inspect`; it does not authorize initialization.
- Detect and show the candidate root first. If inside Git, use its top-level directory; otherwise use the current working directory.
- Modify only that root's `.loop/` files and its project `AGENTS.md` managed section.
- Do not edit global `AGENTS.md`, global Codex configuration, other skills, or any path outside the selected root.
- Do not initialize an existing `.loop/` without first reporting its state and obtaining the user's choice of mode.
- The default is `create-missing`. `append-sections` and `overwrite` require the user's explicit mode choice.
- Do not record secrets, credentials, private configuration, or unrequested operational data.

## Workflow

1. Run `inspect` and show the selected root, existing standard files, additional files, and `AGENTS.md` state.
2. Confirm the root and requested mode with the user. Even when policy triggered the inspection, an explicit request naming the root and mode is confirmation.
3. Run `apply --yes` only after confirmation. The helper preflights the complete target topology and all managed markers before it writes.
4. Report created, skipped, updated, and backed-up files. If it reports an error, do not assume initialization succeeded; run `inspect` before retrying.

Use the reviewed helper in this skill directory:

```bash
python3 <skill-dir>/scripts/init_loop.py inspect --root /path/to/project
python3 <skill-dir>/scripts/init_loop.py apply --root /path/to/project --mode create-missing --yes
```

## Modes

| Mode | Use only when | Behavior |
| --- | --- | --- |
| `create-missing` | the user confirmed initialization | Creates missing standard files and directories; leaves existing files unchanged. |
| `append-sections` | the user explicitly chose it after inspection | Appends only missing marked template sections and backs up every changed existing file. |
| `overwrite` | the user explicitly chose it after inspection | Backs up and replaces standard loop files. |

## Standard Structure

```text
.loop/
  README.md
  00_request.md
  01_spec.md
  02_contract.md
  03_plan.md
  04_progress.md
  05_decisions.md
  06_log.md
  traces/
  reports/
  artifacts/
    screenshots/
    test_outputs/
    notes/
```

## Project `AGENTS.md` Section

The helper may create or update exactly one section bounded by:

```markdown
<!-- BEGIN MODEL LOOP POLICY -->
...
<!-- END MODEL LOOP POLICY -->
```

It rejects zero-or-more-than-one unmatched or duplicate marker pair before writing anything. Existing non-managed content is preserved. Any existing file that changes, including `AGENTS.md`, is backed up under `.loop/backups/<timestamp>/`.

The managed guidance makes loop records optional and task-scoped: it asks an agent to use the smallest useful durable record and to use planners, generators, or evaluators only when their expected value justifies their cost. It does not grant authority for an otherwise-unapproved write.

## Next Action

For a loop-backed task, fill the request, specification, contract, and plan with task-specific facts before implementation. Keep progress, decisions, and logs concise and current; do not create ceremony for a small task.
