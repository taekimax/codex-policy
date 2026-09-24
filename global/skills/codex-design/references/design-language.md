# Design direction and visual language

Use this reference for new surfaces, redesigns, aesthetic reference requests, or visual-quality repair.

## Contents

1. Start from authority
2. Compose before decorating
3. Establish one visual world
4. Use references without cloning
5. Anti-slop diagnostic
6. Direction output

## 1. Start from authority

Classify the visual state:

- **Established:** inherit the coherent system; extend it without a new identity exercise.
- **Incomplete:** preserve recognizable traits and fill only the gaps needed by the surface.
- **Explicit redesign:** preserve product truth, content, function, and constraints while replacing the old visual world.
- **Greenfield:** derive a world from audience, use context, product mechanism, cultural setting, and real assets.

Inspect the actual styles, components, or representative screen needed for the decision; the file tree alone is insufficient.

## 2. Compose before decorating

Choose a composition appropriate to the visitor's job. The Impeccable modes (Persuade, Operate, Read, Experience) can help when they clarify the decision:

- **Monitor:** glanceable state and change; density and prioritization beat a hero.
- **Act:** selection, actions, queues, or editing dominate.
- **Compare:** align alternatives and emphasize meaningful differences.
- **Configure:** progressive disclosure, validation, save state, and reversibility.
- **Decide/Learn:** one idea per section; a hero may be appropriate.
- **Explore:** filters, result organization, preview, and spatial navigation.
- **Command/Inspect:** keyboard speed, focus, and detail hierarchy.

Use the composition to guide hierarchy, content, and interaction before choosing colors or radii.

## 3. Establish one visual world

Resolve these as a connected system:

- **Hierarchy:** what is seen first, second, and acted on.
- **Density and rhythm:** spacing scale, grouping, content measure, alignment.
- **Typography:** deliberate family, scale, weights, numeric treatment, wrapping.
- **Palette:** neutrals, surfaces, ink, accent, semantic states, contrast posture.
- **Shape and depth:** radii, borders, shadows, blur, layering, clipping.
- **Components:** canonical control treatment and all relevant states.
- **Motion:** state communication, continuity, duration/easing, reduced motion.
- **Imagery and icons:** real assets first; original assets only when useful and authorized.

Prefer a small system with a clear point of view. Do not use minimalism as an excuse for weak hierarchy or density as an excuse for tiny text.

## 4. Use references without cloning

Translate a named brand into traits, then create an original system for the user's product. Exact values, assets, and current behavior require authorized, current source evidence.

Useful reference families distilled from the legacy catalog:

| Visual family | General traits | Example references |
|---|---|---|
| Precision monochrome | strict grid, crisp type, restrained radius, one high-contrast action | Vercel, HashiCorp, Cal.com |
| Quiet command UI | dense dark surfaces, keyboard affordances, subtle separation | Linear, Raycast, Superhuman, Warp |
| Technical editorial | strong reading hierarchy, code/mono accents, documentation rhythm | Mintlify, MongoDB, Replicate, Sanity |
| Expressive gradient | art-directed color fields, controlled motion, sparse high-impact sections | Stripe, Framer, Clay, Runway |
| Warm humanist | soft neutrals, friendly geometry, conversational hierarchy | Airbnb, Intercom, Notion, Wise |
| Playful systems | bold accents, irregular illustration or icon rhythm, approachable controls | Figma, Miro, PostHog, Zapier |
| Data-intensive dark | high information density, chart/state color discipline, compact controls | Sentry, Kraken, ClickHouse, Cohere |
| Cinematic premium | full-bleed media, large-scale type, restrained controls | Apple, BMW, SpaceX, ElevenLabs |
| Terminal-native | monospace-forward rhythm, stark contrast, command semantics | Ollama, OpenCode, xAI, VoltAgent |

Use a coherent visual direction; these examples are references, not a required palette of choices.

When the user names a brand, identify the useful traits and adapt them to the product. Keep layout, copy, assets, and identity original. Record durable system decisions in an existing `DESIGN.md` when that document is in scope.

## 5. Anti-slop diagnostic

Audit before repairing. Flag only observed tells:

1. default blue/purple gradient or generic tech hue
2. equal-weight icon + heading + sentence feature tiles
3. decorative accent rails, glows, blur, or icon toppers
4. oversized fake metrics or filler content
5. everything centered without a compositional reason
6. default typography chosen without intent
7. cards used for every grouping or nested without need
8. wrong composition for the visitor's job
9. motion that decorates instead of explaining state
10. inconsistent tokens, component states, or density

Repair at the right level:

- Wrong composition or hierarchy → re-layout.
- Accidental palette or typography → re-tokenize/re-typeset.
- Decorative clutter → remove and replace with spacing, scale, or alignment.
- System drift → consolidate into canonical tokens/components.

Review the repaired surface when useful. A deliberate brief may legitimately use a trait listed above.

## 6. Direction output

For planning-only work, explain the proposed direction at the level needed to make it usable: audience and job, composition and hierarchy, core visual choices, and relevant responsive or accessibility behavior. Include a decision or limitation only when it materially affects the result.

For implementation, translate the direction into existing tokens and component APIs. If a durable new decision conflicts with `DESIGN.md`, reconcile the document within the authorized scope or surface the specific unresolved conflict.
