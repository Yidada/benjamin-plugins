---
name: sdlc-test
description: "Verify software changes, diagnose failing checks, review a diff with severity-ranked passes, or run evals on a model, prompt, skill, hook or instruction change. Use for testing, validation or review tasks."
---

# 测试、评估与代码审查

## Scope

- Apply this skill to its named software task. Do not load `$ai-native-sdlc`, bootstrap `.sdlc`, or start other lifecycle stages unless the user explicitly invokes the coordinator.
- If the coordinator is already active, write results into the corresponding change artifacts and obey its current risk decisions. Otherwise return the requested result in the existing project format.
- Read applicable project instructions and preserve user scope and existing authorization. Use plain explanations with observable examples. Do not change global configuration as a side effect.

## Workflow

This is the Test play plus the review passes from Deploy: continuous evals woven through implementation, and the same review passes for every diff.

1. Read the requested behavior, the plan and spec when they exist, and the changed boundary before selecting tests. Verify the current commit or diff and whether existing results still cover it.
2. Select the smallest tests that could disprove correctness: unit logic, integration, API contracts, browser or device flow, accessibility or performance as applicable. Use repository-required checks. For a bug, the failing test comes first and stays unedited during the fix.
3. Diagnose failures using actual logs. Separate environment failures, flaky tests and product defects with evidence. Do not silently weaken assertions or skip failures to obtain green output.
4. For a change to a model, prompt, skill, hook or `AGENTS.md`, run evals: real tasks with expected outcomes, including negative cases for scope, permissions, uncertainty and failure handling. Treat a pass-rate drop as a blocker for that change, and add an eval for each production incident. A format validator alone cannot prove behavior; a model judge does not replace human acceptance criteria.
5. For reviews, run the passes in order: bugs and logic errors, security and vulnerabilities, compliance against the spec, the plan and project standards. Report each finding with location, trigger, impact and suggested correction. Rank Important before Nit, cap nits at five, skip generated paths and what CI already enforces, and never invent findings to fill a quota. A finding informs the code owner; it does not approve or block by itself, and a review of your own code is labeled self-review. A review request stays read-only unless fixes are authorized.
6. Record exact command or method, environment, outcome and coverage gap. Rerun affected checks after material changes. When a mistake appears for the second time, propose the `AGENTS.md` correction.

Output: findings or verification result, supporting evidence and unresolved gaps. Existing evidence.md and review.md are the handoff when the lifecycle is active.
