---
name: google-workspace-artifact-qa
description: Verify Google Docs and Slides layout after authoring or Office import, especially Korean typography and A4 print output. Use when native conversion or visual fidelity needs checking, or when the user requests artifact QA.
---

# Google Workspace Artifact QA

Check the delivered native Google artifact against the user's request or controlling template. Reuse evidence from the authoring workflow; this skill does not require a separate reviewer or duplicate a completed check. A review-only request stays read-only. When authoring or repair is already authorized, fix in-scope defects and verify the affected result without asking for another approval.

## Expected output

Infer language, fonts, page or slide size, orientation, and screen or print intent from the task and template. Default new documents to A4 portrait and Korean native artifacts to Korean language and a supported Korean font such as `Noto Sans KR`. Preserve an explicit font choice or controlling template when supported by the native editor. An OS-installed font or visually plausible fallback alone does not establish Google support.

A4 is 210 × 297 mm, about 595.276 × 841.890 points, or 7,560,000 × 10,692,000 EMU; swap dimensions for landscape. Compare physical size with a small conversion tolerance, up to 0.5 mm. A 16:9 slide canvas is appropriate for screen use and does not represent A4 print output.

## Native readback

Use the available Google read surfaces to inspect the exact destination and the properties relevant to the change:

- Slides: root `locale`, `pageSize`, and effective text fonts. Resolve inherited fonts through placeholders, layouts, masters, and defaults when the authored run does not specify a family.
- Docs: file language when exposed, page mode, section geometry, orientation, margins, and effective fonts from explicit and inherited styles. A4 print output needs paged mode; source DOCX geometry alone does not prove native geometry.

For a new artifact, conversion, or broad restyle, inspect the delivered text and layout throughout. For a narrow edit, focus on affected content and shared styles that could change other pages. Read notes, masters, or other hidden structures when they affect the requested output or typography; do not audit unrelated structures by default.

If an API cannot expose or change a property, check an available native editor or suitable template when useful. Do not infer locale from the text language, label an unresolved font as verified, or rewrite a usable document solely to satisfy an inaccessible metadata check. Treat uncertainty as a limitation unless it prevents meeting an explicit or materially important requirement.

## Rendered result

For conversion or layout-sensitive delivery, export the native file to PDF and inspect its page dimensions and rendered appearance. A local rendering of the Office source does not prove the Google result. Inspect all pages for a newly created or converted artifact; after a narrow edit, inspect affected pages and any pagination changes.

Look for missing glyphs, font substitution, clipping, overflow, unexpected wrapping, blank pages, inconsistent margins, and misplaced elements. Reuse a current export if the artifact has not changed. If export or full inspection is unavailable, identify the unverified scope without claiming full visual success.

## Report

State the target, meaningful checks as PASS, FAIL, or NOT RUN, located defects, and any limitation that affects the requested use. Distinguish actual defects from unavailable diagnostics. Continue authorized repairs; ask for a decision only when the remedy materially changes the requested result or exceeds scope.
