# Loop Workspace

## Purpose

`.loop/` holds the minimum durable continuation state for this repository. It complements the current user request, repository policy, source, and test evidence; it does not override any of them.

## Operating Rule

Use only the smallest record needed for the active task. Files `00_request.md` through `04_progress.md` describe current work; keep them current and remove superseded requirements. Decisions and logs are historical evidence, not current authority or automatic acceptance gates. Do not store secrets, credentials, or private configuration. Specialist roles are optional and must earn their coordination cost.
