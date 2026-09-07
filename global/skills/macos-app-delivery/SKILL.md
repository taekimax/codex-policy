---
name: macos-app-delivery
description: Package, install, update, replace, or deliver a named macOS app using its existing build and signing workflow, with recoverable replacement and separate evidence for each requested stage.
---

# macOS App Delivery

Complete the requested delivery stages using the project's existing commands and the global recoverable-install preference. A packaging request alone does not imply installation, launch, cleanup, commit, or push; carry forward stages already authorized in the conversation.

## Resolve the project adapter

Read the project's delivery script or short delivery document for the repository, bounded build/staging command, exact staged bundle and installed destination, app-owned workers, and executable/service payloads to compare. Keep these app-specific details there. Derive missing routine details from the build settings and bundle; ask only when ambiguity affects the destination or requested outcome. Keep signing identities and credentials in the existing local setup, outside this shared skill.

## Stage and replace

1. Inspect Git state and the installed destination. Build and sign with the existing project workflow and an explicit bounded job count. Use one stable signed app identity for permission-bearing live checks. Verify the staged bundle's signature (`codesign --verify --deep --strict`) and required payloads before replacement. Reuse that checked stage unless the source changes.
2. For requested installation, quit the existing app and its identified workers, then move its bundle to the user's Trash under a unique timestamped name. Copy the staged bundle to the resolved destination. Preserve the staged build and rollback bundle until normal execution is confirmed; retain any further recovery assets the user needs.
3. Verify the installed signature and compare the staged and installed core executable and service payloads, using byte comparison or cryptographic hashes. Confirm the installed bundle path. Signature success alone does not prove launch, system consent, provider access, or functional behavior.
4. Launch when included in scope and exercise the requested user flow. If a locked Mac or system consent requires user action, report the exact action once and save the current checkpoint. Preserve successful packaging/installation evidence while the live check remains incomplete.

If replacement or verification fails, retain both bundles, identify the exact failed stage, and use the preserved original for recovery when appropriate within scope. Do not bypass a macOS denial or escalate privileges. A routine failure can be investigated and retried within existing authority; stop dependent delivery stages while the installation is unresolved.

## Finish requested stages

For cleanup, inventory the proposed residues and account for dirty changes before removing a checkout. Move obsolete builds, temporary packages, and duplicate app copies to timestamped Trash or another recoverable location. Preserve the current installed app, app data, models, active packages, useful outputs, unrelated work, and needed recovery assets. Do not turn cleanup into a new build or reinstall.

Commit the intended files when requested, after checking the scoped diff and relevant validation. Push only when requested. A later cleanup or commit failure does not erase a successful installation.

Report the requested stages separately and concisely: staged/installed path, rollback location, launch and user-flow result, cleanup result, and commit result. Label relevant checks PASS, FAIL, or NOT RUN; state the remaining user-visible gap when one exists.
