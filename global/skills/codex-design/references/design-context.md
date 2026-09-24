# Product and design context

Use this reference only when creating, reviewing, merging, or interpreting `PRODUCT.md`, `DESIGN.md`, or `.impeccable` context artifacts.

## Contents

1. Ownership and preservation
2. PRODUCT.md
3. DESIGN.md
4. Extract, seed, merge, and review
5. Validation

## 1. Ownership and preservation

- Use the existing root `DESIGN.md` as the durable visual authority; do not create a competing document.
- Preserve existing files and history. Read the sections relevant to the requested change before editing.
- Prefer a scoped merge over replacement. An explicit redesign may replace the visual world within the user's authorized scope; preserve product truth and established brand commitments unless the request changes them.
- Do not let per-surface notes redefine global tokens. Promote a repeated decision into `DESIGN.md` only when it is meant to be system-wide.
- Treat `.impeccable/design.json` as generated automation metadata and `.impeccable/surfaces/*` as page/route strategy. Never hand-edit or overwrite them merely to satisfy this skill.

## 2. PRODUCT.md

Capture only durable product facts:

- platform and frontend surfaces
- audiences, jobs, frequency, and environment
- purpose, positioning, and differentiators
- real evidence, content constraints, and prohibited claims
- brand commitments, voice, legal/accessibility constraints

Do not put visual tokens, page layout, or temporary implementation plans here. Label assumptions that affect use and ask only about missing facts that materially change the design.

## 3. DESIGN.md

Follow the current Google Labs `DESIGN.md` shape: optional YAML frontmatter for normative tokens plus Markdown rationale. The spec is alpha; re-check the official source before depending on version-sensitive fields.

### Frontmatter

Use only observed or approved values. Typical groups are:

- `version`, `name`, `description`
- `colors`
- `typography`
- `rounded`
- `spacing`
- `components`

Use quoted sRGB hex colors and token references such as `{colors.primary}`. Express component state variants as sibling entries (`button-primary`, `button-primary-hover`), not nested state objects. Do not fabricate empty scales or normalize project-specific names without reason.

### Canonical body order

Include only relevant sections, in this order:

1. `## Overview`
2. `## Colors`
3. `## Typography`
4. `## Layout`
5. `## Elevation & Depth`
6. `## Shapes`
7. `## Components`
8. `## Do's and Don'ts`

Unknown existing sections may be preserved. Avoid duplicate section headings. Put responsive rules in Layout, shadows/layering in Elevation, radius/borders/form language in Shapes, and state behavior under Components.

Record exact values in frontmatter or code-derived examples; use prose for rationale, usage, hierarchy, and prohibitions. Do not duplicate the same token with conflicting values.

## 4. Extract, seed, merge, and review

### Extract from an existing UI

Inspect the relevant sources: CSS variables or global styles, framework theme, token files, canonical components, and a representative rendered screen when available.

Document the coherent incumbent system. Missing `DESIGN.md` is not permission to redesign.

### Seed a new system

Use enough product context and a concrete first surface. Make routine direction choices within the user's request; ask only when an unresolved brand or product choice materially changes the system. Mark provisional decisions, avoid exhaustive component inventories before implementation, and validate the seed against the first surface.

### Merge an existing document

- Preserve confirmed tokens and narrative.
- Add only evidence-backed missing rules.
- Reconcile code/document drift explicitly; do not silently choose one when authority is unclear.
- Make material token removals, renames, and global rule changes explicit in the result; ask first only when they exceed the request's authority.

### Review only

Check source traceability, internal consistency, token references, section order, accessibility claims, and whether page-specific ideas have leaked into global rules. Make no edits.

## 5. Validation

Check the sections, token references, and source consistency affected by the change. If an official lint or diff command is already installed and useful, run it. For a proposed replacement, compare the current and proposed content before adoption. Do not leave temporary proposal files behind unless requested.

Official source of truth:

- https://github.com/google-labs-code/design.md
- https://github.com/google-labs-code/design.md/blob/main/docs/spec.md

Do not fetch a package solely for this check. If the CLI is unavailable, validate relevant structure and references directly.
