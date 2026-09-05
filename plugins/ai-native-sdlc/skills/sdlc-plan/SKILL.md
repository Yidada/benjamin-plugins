---
name: sdlc-plan
description: "Clarify software requirements, feature scope, acceptance criteria and an implementation plan. Use for software planning or ambiguous development requests."
---

# 需求与任务规划

## Scope

- Apply this skill to its named software task. Do not load `$ai-native-sdlc`, bootstrap `.sdlc`, or start other lifecycle stages unless the user explicitly invokes the coordinator.
- If the coordinator is already active, write results into the corresponding change artifacts and obey its current risk decisions. Otherwise return the requested result in the existing project format.
- Read applicable project instructions and preserve user scope and existing authorization. Use plain explanations with observable examples. Do not change global configuration as a side effect.

## Workflow


1. Steelman the problem: who is affected, what fails today, the desired observable outcome, constraints and success examples. Distinguish evidence from assumptions.
2. Inspect the affected product/code path enough to challenge the proposed solution. Explain a material conflict with the user's goal. Do not treat the first suggested implementation as a fixed requirement unless the user makes it one.
3. Identify the smallest useful delivery. List scope, exclusions, relevant files/components, dependencies and the order of work.
4. Turn each criterion into a concrete check. Include failure behavior when it changes the result. Carry over existing decisions and source issue references.
5. Ask only for missing choices that change scope or correctness. Continue independent investigation. A request for a plan yields a plan; an implementation request continues into authorized work.

Output: a concise problem statement, acceptance list, scoped plan and unresolved decisions. Use an existing intent.md/plan.md when the lifecycle is active.
