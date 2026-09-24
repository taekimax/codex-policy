---
name: codex-design
description: Design, redesign, or visually review a web-rendered UI and its design system. Use for requested visual direction, UI consistency, accessibility or responsive review, and scoped frontend visual changes in web apps, extensions, or Electron renderers. A routine frontend behavior fix alone does not trigger this skill.
---

# Codex Design

Work from the user's purpose, the visible surface, and the project's existing visual system. A review request stays read-only; a request to fix, apply, build, or redesign authorizes the corresponding in-scope edits. Do not require a separate confirmation for decisions already covered by the request. Ask only when a missing choice materially changes the result.

## Route the work

| Need | Read |
| --- | --- |
| Review a UI or implement a scoped visual fix | [workflows.md](references/workflows.md) |
| Create, review, or change `PRODUCT.md`, `DESIGN.md`, or `.impeccable` context | [design-context.md](references/design-context.md) |
| Set a new direction, redesign, or use a visual reference | [design-language.md](references/design-language.md) |
| Run the Impeccable detector or interpret its files | [impeccable.md](references/impeccable.md) |

Read only the references needed for the task. Combine them when the requested result spans those needs.

## Work to the surface

1. Read applicable project instructions and inspect the requested route, component, or flow with its relevant tokens, styles, components, and existing design context. Preserve unrelated work. An established UI is evidence even when `DESIGN.md` is absent.
2. For a review, report observed issues and scoped remedies. For a change, reuse the existing design system and implement the smallest coherent result. Create context documents only when requested or needed for the design decision.
3. Verify the actual outcome in proportion to the change. Inspect the rendered surface when layout or appearance matters and it is available. Check affected responsive sizes, keyboard/focus behavior, accessibility, and states where relevant. Run project checks that exercise the changed behavior. Use the detector when it can add useful evidence, and compare like targets if running before and after.
4. Lead with the result and material evidence. Mention unresolved limitations or decisions only when they affect use. Do not imply that source checks, a clean detector result, or a build alone prove visual quality.

## Boundaries

- Preserve established `PRODUCT.md`, `DESIGN.md`, `.impeccable/design.json`, `.impeccable/surfaces/*`, brand commitments, and source facts. Review their relevant content before changing them. `PRODUCT.md` owns product truth; `DESIGN.md` owns durable visual decisions; surface files narrow one route; generated metadata is not hand-edited.
- Reuse project components, tokens, assets, and dependencies. Do not invent claims, metrics, or placeholder content for visual effect. Transform reference traits into original work; do not copy proprietary assets or layouts.
- Keep read-only reviews read-only. Add dependencies only when needed for the authorized result; keep deployment and publication within the request's scope. Impeccable installation, updates, hooks, Live Mode, telemetry, and direct key-based image generation remain outside this skill; see [impeccable.md](references/impeccable.md).
- Follow [design-context.md](references/design-context.md) when changing durable design context, and [design-language.md](references/design-language.md) when a new direction is in scope.
