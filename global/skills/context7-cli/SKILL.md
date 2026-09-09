---
name: context7-cli
description: Fetch version-aware library documentation through the already-installed ctx7 CLI. Use only when the user explicitly mentions ctx7 or Context7, or explicitly invokes $context7-cli. Do not trigger for generic library-documentation questions, skill discovery or installation, MCP setup, login, or account configuration.
---

# Context7 Documentation

Use the local `ctx7` CLI as an explicit, documentation-only lookup path.

## Preconditions

- Resolve `ctx7` with the host shell (`command -v ctx7` on POSIX shells or
  `Get-Command ctx7` on PowerShell) and inspect `ctx7 --version`.
- Use the installed version as-is. Never run `npm install -g`, `npx ...@latest`,
  `ctx7 setup`, or `ctx7 login` as part of a documentation lookup.
- If `ctx7` is missing or the installed version cannot perform the requested
  lookup, report the exact gap. Install, update, setup, and authentication are
  separate user-authorized actions.
- Context7 queries use the network. Follow the active sandbox and approval
  policy rather than weakening it or changing credentials.

## Lookup Workflow

```bash
ctx7 library <name> <specific-query>
ctx7 docs <library-id> <specific-query>
```

1. Read the project manifest or lockfile first when the requested library and
   version can be determined locally.
2. Resolve the canonical Context7 library ID with `ctx7 library`, unless the
   user already provided a library ID. Use a narrow query that describes the
   public API or behavior being verified.
3. Prefer an exact version-specific ID when Context7 lists the project's
   version. Otherwise state that the result targets the latest indexed docs.
4. Query only the focused topic with `ctx7 docs`.
5. Compare the result with the repository's installed version and source code
   before applying advice. Context7 is supporting evidence, not authority over
   a pinned local dependency.
6. Stop after three resolution attempts or three docs queries. Use the best
   evidence available or report that Context7 did not resolve the question.

Read [references/docs.md](references/docs.md) for result-selection and query
details when a lookup is actually needed.

## Data And Output Boundaries

- Never send secrets, credentials, personal data, proprietary source, or raw
  private prompts in a Context7 query.
- Do not inspect, print, create, or change Context7 credentials.
- Do not use Context7's skill-management, setup, or generation commands from
  this skill. Use the built-in official installer for official Codex skills and
  the documented Codex configuration/plugin mechanisms for setup work.
- Report the selected library ID and version, summarize the relevant guidance,
  and distinguish Context7-derived evidence from locally verified behavior.
