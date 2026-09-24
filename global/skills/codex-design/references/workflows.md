# Visual review and implementation

Use this reference for a requested UI review or visual source change. Review-only work stays read-only. A request to fix or implement authorizes the in-scope design change.

## Establish evidence

Identify the exact page, component, or flow and its relevant styles, tokens, assets, and existing design decisions. Inspect the rendered surface when available and when appearance or interaction is at issue. Distinguish observations from inferences; source code alone cannot prove final layout, contrast, focus order, or runtime behavior.

For a review, inspect only the dimensions that could affect the requested outcome:

- **Purpose and hierarchy:** user job, action priority, content order, supported claims, and meaningful states.
- **Accessibility and interaction:** semantics, labels, keyboard reachability, visible focus, overlay return focus, form errors, and reduced motion where applicable.
- **Responsive behavior:** reflow, overflow, content extremes, touch targets, and the actual constrained container for an embedded or extension UI.
- **Visual system:** typography, color contrast, spacing, grouping, imagery, components, and state consistency against established tokens.
- **Performance and resilience:** layout shift, large media, expensive effects, slow or failed requests when the change touches them.

Group findings by cause. Give each actionable finding its evidence, user impact, location, and scoped remedy. Prioritize issues that impair the primary task or accessibility; omit optional polish unless the user requested it. If no actionable issue is found, say so.

## Make a change

1. Preserve the incumbent system for a refinement; use [design-language.md](design-language.md) for a requested redesign or new direction.
2. Translate the direction into existing tokens and component APIs, then implement a coherent scoped result. Preserve product content and behavior unless the request changes them.
3. Check the affected flow and relevant states. For visible layout changes, compare the actual rendered result at sizes that matter to the surface. Exercise keyboard or focus behavior when it changed or could regress. Run available project checks that cover the edited code.
4. Use the Impeccable detector only when it can add useful evidence; follow [impeccable.md](impeccable.md). A detector finding is a clue, not a substitute for observing the UI. Stop verification when the result is sufficiently established for the change.

Report the result, material design decisions, meaningful checks, and any unresolved issue that affects use. Do not add a fixed severity matrix, checklist, risk list, or approval section to an ordinary deliverable.

## Surface-specific considerations

- **Web apps:** account for relevant shared components, theme layers, hydration, and route behavior.
- **Extensions:** inspect the actual popup, panel, or overlay dimensions and relevant CSP, Shadow DOM, or host-page behavior.
- **Electron renderers:** check relevant window sizes and renderer interaction; preserve IPC and main-process boundaries.
- **HTML/CSS:** preserve semantics and progressive enhancement; a bounded visual task does not require a new framework.
