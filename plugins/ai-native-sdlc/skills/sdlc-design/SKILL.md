---
name: sdlc-design
description: "Design software behavior, architecture, APIs, data contracts and compatibility for a feature or refactor. Use when an implementation needs a concrete design decision."
---

# 软件方案与接口设计

## Scope

- Apply this skill to its named software task. Do not load `$ai-native-sdlc`, bootstrap `.sdlc`, or start other lifecycle stages unless the user explicitly invokes the coordinator.
- If the coordinator is already active, write results into the corresponding change artifacts and obey its current risk decisions. Otherwise return the requested result in the existing project format.
- Read applicable project instructions and preserve user scope and existing authorization. Use plain explanations with observable examples. Do not change global configuration as a side effect.

## Workflow


1. Read the existing call path, public contracts, persisted data and relevant tests. State what evidence is current.
2. Describe inputs, outputs, invariants and failure behavior. Map acceptance examples to the proposed boundaries.
3. Compare alternatives only when they change cost, compatibility, risk or user experience. Select one and explain its tradeoff.
4. For API/data changes, describe old/new compatibility, rollout ordering, migration and rollback limits. For UI changes, describe normal/empty/loading/error states and accessibility where relevant.
5. Define checks at the boundary that may fail. Avoid assuming a framework, cloud or datastore.
6. Make the design concrete enough to review before an irreversible decision. Reuse applicable prior authorization and flag unresolved high-impact choices.

Output: behavior/contracts, affected boundaries, decision rationale and verification plan. Update spec.md and decisions.md when the lifecycle is active.
