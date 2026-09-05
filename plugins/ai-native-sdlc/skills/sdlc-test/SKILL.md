---
name: sdlc-test
description: "Verify software changes, diagnose failing checks, review a diff, or evaluate a model/prompt/skill change against observable criteria. Use for testing, validation or review tasks."
---

# 测试、评估与代码审查

## Scope

- Apply this skill to its named software task. Do not load `$ai-native-sdlc`, bootstrap `.sdlc`, or start other lifecycle stages unless the user explicitly invokes the coordinator.
- If the coordinator is already active, write results into the corresponding change artifacts and obey its current risk decisions. Otherwise return the requested result in the existing project format.
- Read applicable project instructions and preserve user scope and existing authorization. Use plain explanations with observable examples. Do not change global configuration as a side effect.

## Workflow


1. Read the requested behavior and changed boundary before selecting tests. Verify current commit/diff and whether existing results still cover it.
2. Select the smallest tests that could disprove correctness: unit logic, integration, API contracts, browser/device flow, accessibility or performance as applicable. Use repository-required checks.
3. Diagnose failures using actual logs. Separate environment failures, flaky tests and product defects with evidence. Do not silently weaken assertions or skip failures to obtain green output.
4. For model/prompt/skill/tool changes, include representative successful cases and negative cases for scope, permissions, uncertainty and failure handling. A format validator alone cannot prove behavior.
5. For reviews, report actionable findings with location, trigger, impact and suggested correction. Rank by impact; do not invent findings to fill a quota. A review request stays read-only unless fixes are authorized.
6. Record exact command/method, environment, outcome and coverage gap. Label self-review accurately and rerun affected checks after material changes.

Output: findings or verification result, supporting evidence and unresolved gaps. Existing evidence.md/review.md are the handoff when the lifecycle is active.
