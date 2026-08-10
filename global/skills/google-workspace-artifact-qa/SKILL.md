---
name: google-workspace-artifact-qa
description: Perform read-only final QA for Google Docs and Google Slides artifacts, especially Korean-language documents, A4 or print-first outputs, and DOCX or PPTX files converted to native Google formats. Use after authoring, editing, or import to verify native language or locale, Google-supported effective fonts, Docs page mode and geometry, Slides page size, native PDF export, and rendered visual fidelity; do not automatically repair the target unless the user separately requests edits.
---

# Google Workspace Artifact QA

Run this skill as a final, independent gate after the applicable `google-docs`, `google-slides`, or `presentations` authoring workflow. Inspect the exact native destination and its native PDF export. Keep the QA phase read-only.

## Establish the expected contract

Before reading the artifact, record:

- the exact Google file URL or ID, native type, and revision when exposed;
- the expected file language or locale;
- the allowed Google-supported font family or families;
- the expected page or slide size and orientation;
- whether the output is `screen-first` or `print-first`;
- whether an imported Office file is only a source or also controls the final geometry.

For Korean-language artifacts, default the expected file language to Korean and the Slides root locale to `ko-KR`, and default the expected font to Google Fonts' `Noto Sans KR` when the user or controlling template does not specify another Google-supported Korean font. Accept another font only when the user selected it and current Google editor support or a verified native template establishes that it is supported. Never treat an OS-installed font, source Office font, or visually plausible glyph fallback as support evidence.

For documents without another size instruction, expect A4. Use these normalized dimensions and swap width and height for landscape:

| Surface | A4 portrait width x height |
| --- | --- |
| Millimeters | 210 x 297 mm |
| Google Slides EMU | 7,560,000 x 10,692,000 |
| PDF or Docs points | about 595.276 x 841.890 pt |

Allow only a small serialization tolerance, no greater than 0.5 mm after unit conversion. Compare physical dimensions, not aspect ratio alone. A `12,192,000 x 6,858,000` EMU 16:9 Slides canvas is screen-sized and is never A4. Accept 16:9 only when the contract explicitly calls for that screen-first canvas.

## Preserve the read-only boundary

Use native Google read APIs or connector reads, native Drive PDF export, and local PDF inspection or rendering. Do not issue `batchUpdate`, change file language, replace fonts, resize pages or slides, create a repaired copy, or use UI automation to mutate the target during QA.

If the user also requested repair, finish and report the read-only QA first, then treat repair as a separate authorized phase. After any repair, repeat this entire gate against the new native state and export.

## Inspect Google Slides

Read the complete native presentation resource and verify all of the following:

1. Compare the root `locale` with the expected locale. For a Korean artifact, an English locale such as `en-US` is an error.
2. Normalize the root `pageSize` width and height to physical dimensions and compare both size and orientation with the expected contract. Report A4-versus-16:9 mismatch as an error.
3. Enumerate every delivered slide, speaker-notes page, master, notes master, layout, placeholder relationship, shape, table cell, group member, and nonempty text element needed to resolve typography.
4. Resolve the effective font for every nonempty text run. Start with the run's explicit text style, then follow inherited placeholder, layout, master, and theme or default styles until an actual family is known. A missing explicit font is not a pass while its inherited family remains unresolved.
5. Compare every resolved family with the allowed font set. Report `Arial`, an unsupported family, an unresolved family, or any other unexpected family as an error. Count runs by effective family and retain slide and object locations for each defect.

Use the full-presentation readback and inherited-style parser from the active Google Slides workflow when available. Do not sample runs or rely on a visual screenshot to prove the font family.

The public Slides API exposes presentation `locale` and `pageSize` for readback but does not provide a request that changes those presentation-wide properties. Do not hide a mismatch with partial text edits or local export scaling. Fail the gate and require a verified native template or a rewrite under a separately authorized authoring task.

## Inspect Google Docs

Read the complete native document, including all tabs and text-bearing bodies, headers, footers, footnotes, tables, lists, and named-style definitions. Verify all of the following:

1. Read the native file language or locale from an available native readback surface and compare it with the expected value. If the available API or connector cannot expose it, mark the required property unverified and do not infer it from Korean text or fonts.
2. Read `documentStyle.documentFormat.documentMode` and report the effective mode as `PAGES` or `PAGELESS`. Require `PAGES` for A4 or print-first output. Accept `PAGELESS` only when the expected contract explicitly requires a pageless screen-first document.
3. Read page size, `flipPageOrientation` or equivalent orientation state, and all page margins. Normalize the effective width and height before comparing with the expected size and orientation. Report missing, mixed, or unexpected geometry and margins.
4. Resolve the effective font for every nonempty text run from its explicit `weightedFontFamily.fontFamily` or equivalent style and the applicable named, paragraph, or document default style. Inspect inherited styles as well as explicit runs; an unresolved inherited font is an error.
5. Compare every resolved family with the allowed font set. Report `Arial`, unsupported or unexpected families, and glyph-only fallback as errors, with tab and range locations when available.

For A4 or print-first output, treat `PAGELESS`, Letter geometry, landscape-versus-portrait mismatch, or A4 dimensions stored only in the Office source but not in the native Doc as blocking defects.

## Export and render the native result

Export the exact native Google file to PDF through the Google Drive export surface after structural readback. Do not substitute a locally rendered source DOCX or PPTX.

Then:

1. Inspect the PDF page boxes. For A4 output, verify every page is A4 in the expected orientation within the same physical tolerance.
2. Render every PDF page or slide to an image. For Slides, require the PDF page count and ordered render count to equal the delivered native slide count.
3. Inspect every rendered page individually at readable size. A contact sheet may support overview review but never replaces individual inspection.
4. Check for missing or substituted glyphs, clipped or overflowing text, unexpected wrapping, blank pages or slides, scaled print content, inconsistent margins, misplaced elements, and orientation errors.

Do not pass when export is unavailable, any page was not rendered, the page count is inconsistent, or visual inspection is incomplete.

## Decide and report

Return `PASS` only when every required native property readback, effective-font resolution, native PDF export, page-box check, and full render inspection succeeds.

Return `FAIL` for any mismatch, including:

- locale or file-language mismatch;
- `Arial`, unsupported, unresolved, or otherwise unexpected effective fonts;
- `PAGES` or `PAGELESS` mismatch;
- page size, slide size, orientation, or margin mismatch;
- A4 expected but 16:9, Letter, or another size found;
- native PDF or rendered visual defects.

Return `BLOCKED` rather than `PASS` when a required property or export cannot be read with the available authorized tools. State that the artifact is not verified; do not silently downgrade the check.

Keep the handoff concise and evidence-based:

```text
Status: PASS | FAIL | BLOCKED
Target: <native type and file id or URL>
Expected: <locale, font set, size/orientation, mode, screen/print intent>
Native readback: <locale/language, mode, dimensions, margins, font counts>
PDF/render: <export identity, page count, page boxes, all pages inspected>
Defects: <locations and expected-versus-actual values>
Required next action: <none, verified native template, or separate rewrite/repair request>
```
