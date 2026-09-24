# Impeccable integration boundary

Use this reference when the detector or an Impeccable context artifact is relevant to the task.

## Contents

1. Adopted capabilities
2. Detector workflow
3. Context artifacts
4. Prohibited capabilities
5. Current official sources

## 1. Adopted capabilities

Use only these ideas from Impeccable:

- the four per-surface modes: Persuade, Operate, Read, Experience
- durable context split between `PRODUCT.md`, `DESIGN.md`, surface briefs, and generated metadata
- optional detector evidence for a relevant design question
- design-system-aware checks when `DESIGN.md` exists
- bounded comparison when a visual change calls for it

Do not vendor or depend on the full Impeccable skill bundle. `codex-design` owns routing and uses the public detector CLI only when appropriate.

## 2. Detector workflow

Run the detector only when it can resolve a relevant uncertainty. Prefer the smallest representative source path. Use a URL only when a rendered server already exists and the task permits browser/network access. Use an existing local command; do not fetch a package for a routine check.

```bash
# Directory
impeccable detect src/

# One source file
impeccable detect src/components/Card.tsx

# Machine-readable output
impeccable detect --json src/

# Narrow one design domain
impeccable detect --scope type src/
impeccable detect --scope layout src/

# One raw scan without local design-system checks
impeccable detect --no-design-system src/
```

If comparing before and after, use the same target, configuration, and flags. Save output in a temporary directory outside the project unless the user asks for a committed report.

Interpret exit codes:

- `0`: no findings
- `2`: findings detected; the command succeeded
- `1`: command failed

The detector covers design-relevant HTML/CSS and source text such as JSX, TSX, Vue, Svelte, Astro, and CSS modules. URL scans inspect rendered pages. It checks signals including contrast, typography drift, overflow, generic AI-design tells, brittle motion, and `DESIGN.md` violations.

Do not treat a clean result as proof of accessibility or responsive correctness. Inspect the rendered behavior relevant to the change, such as focus order, dynamic states, reflow, contrast, or the primary flow.

If no local detector is available, use relevant source and rendered evidence. Mention its absence only when that limits the conclusion.

Never add ignores, inline disable comments, or detector config merely to improve the after count. A requested waiver needs a specific reason.

## 3. Context artifacts

- `PRODUCT.md`: product strategy and truth.
- `DESIGN.md`: user-owned visual source of truth.
- `.impeccable/surfaces/*`: per-surface mode/job/direction; preserve if present.
- `.impeccable/design.json`: generated automation metadata; do not hand-edit.
- `.impeccable/config.json` and local config: detector/hook behavior; do not mutate during a normal audit or design task.

The detector reads a local `DESIGN.md` by default and may use the generated sidecar for richer token/ramp data. Staleness is a finding to report, not permission to regenerate files.

## 4. Prohibited capabilities

Do not run or install:

- `npx impeccable install` or `update`
- Impeccable hooks or `.codex/hooks.json` changes
- Impeccable Live Mode or its localhost server
- telemetry/analytics setup
- `OPENAI_API_KEY` or Impeccable's direct image-generation script
- automatic ignore or waiver writes

Use Codex's own browser/computer tools for inspection when available. Use the `imagegen` skill only when image creation is explicitly in scope.

## 5. Current official sources

Re-check these sources before relying on version-sensitive behavior:

- Repository: https://github.com/pbakaus/impeccable
- Documentation: https://impeccable.style/docs/
- Context: https://impeccable.style/docs/context/
- Detector: https://impeccable.style/docs/detector/
- Hooks: https://impeccable.style/docs/hooks/
- Privacy: https://impeccable.style/privacy/

At integration time (2026-08-04), the official repository package was `impeccable` 3.5.0 at commit `620ba1fe7d87a39039a8528bfaa319ecfa893cb2`. Treat this as provenance, not a permanent pin; the public workflow may evolve.
