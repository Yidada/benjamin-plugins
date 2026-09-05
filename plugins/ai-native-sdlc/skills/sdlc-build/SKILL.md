---
name: sdlc-build
description: "Implement a scoped software feature, bug fix or refactor using the repository toolchain and observable validation. Use for requests to change code."
---

# 实现与缺陷修复

## Scope

- Apply this skill to its named software task. Do not load `$ai-native-sdlc`, bootstrap `.sdlc`, or start other lifecycle stages unless the user explicitly invokes the coordinator.
- If the coordinator is already active, write results into the corresponding change artifacts and obey its current risk decisions. Otherwise return the requested result in the existing project format.
- Read applicable project instructions and preserve user scope and existing authorization. Use plain explanations with observable examples. Do not change global configuration as a side effect.

## Workflow


1. Resolve target repo/package, project instructions, current diff and actual build/test commands. Prefer existing tools and lockfiles. Preserve unrelated work.
2. Restate the concrete behavior to deliver and inspect entry point → implementation → consumers/tests. Follow a supplied plan or create a short one proportional to the change.
3. For defects, reproduce the failure when feasible. Change the smallest coherent unit and verify the original boundary. For features, keep each implementation slice reviewable.
4. Run affected checks and all repository-required gates. A trivial reversible edit needs direct verification; do not add tests that merely duplicate implementation.
5. Inspect final diff for accidental edits, changed test expectations, generated content and public-contract drift. Complete necessary documentation within scope.
6. Continue until the requested work is complete or a concrete blocker needs input. Do not add unrelated refactors, dependency upgrades or external delivery.

Output: delivered behavior, relevant changed paths, actual checks and remaining limitation. Distinguish local, simulator, staging and production evidence.
