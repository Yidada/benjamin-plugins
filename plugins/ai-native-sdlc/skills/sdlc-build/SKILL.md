---
name: sdlc-build
description: "Implement a scoped software feature, bug fix or refactor: plan mode first, then code and tests with the repository toolchain and a self-verifying feedback loop. Use for requests to change code."
---

# 实现与缺陷修复

## Scope

- Apply this skill to its named software task. Do not load `$ai-native-sdlc`, bootstrap `.sdlc`, or start other lifecycle stages unless the user explicitly invokes the coordinator.
- If the coordinator is already active, write results into the corresponding change artifacts and obey its current risk decisions. Otherwise return the requested result in the existing project format.
- Read applicable project instructions and preserve user scope and existing authorization. Use plain explanations with observable examples. Do not change global configuration as a side effect.

## Workflow

This is the Build play: nothing is implemented without an accepted plan, and the agent verifies its own work before a person sees it.

1. Resolve the target repo or package, project instructions, current diff, and the actual build, lint, typecheck and test commands. Prefer existing tools and lockfiles. Preserve unrelated work.
2. Plan mode first. Read the intent and spec (or restate the concrete behavior when there is none), inspect entry point → implementation → consumers and tests, and write the plan: files that change, order of work, risks, proof. Keep it proportional to the change; a trivial reversible edit needs one line. Interrogate the plan: what could this break, which step is most risky, what was rejected? A supplied and accepted plan is followed; when implementation departs from it, update the plan in the same commit.
3. Implement the smallest coherent slice. For a defect, write the failing test first: reproduce the failure, confirm it fails for the expected reason, then make it pass without editing the test. For UI work, exercise the changed flow against the approved design and iterate. Keep each slice reviewable.
4. Close the feedback loop. Run affected checks and every repository-required gate, prefer one command per check with a known healthy output, and make the target quantifiable. Do not add tests that merely duplicate implementation. Delegate recurring jobs to named subagents (verifier, researcher) only when delegation is authorized, and require an evidence-based report from each.
5. Inspect the final diff for accidental edits, changed test expectations, generated content, credentials, and public-contract drift. Complete necessary documentation within scope. When the same mistake happened twice, add the correction to the repository's `AGENTS.md` within scope.
6. Continue until the requested work is complete or a concrete blocker needs input. Do not add unrelated refactors, dependency upgrades or external delivery.

Output: delivered behavior, relevant changed paths, the plan followed, actual checks with output, and remaining limitation. Distinguish local, simulator, staging and production evidence.
