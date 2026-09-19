---
name: sdlc-design
description: "Turn an intent into a requirements and design spec in one session, applying project and policy standards while writing and flagging conflicts. Use when an implementation needs behavior, architecture, API, data contract or compatibility decisions."
---

# 软件方案与接口设计

## Scope

- Apply this skill to its named software task. Do not load `$ai-native-sdlc`, bootstrap `.sdlc`, or start other lifecycle stages unless the user explicitly invokes the coordinator.
- If the coordinator is already active, write results into the corresponding change artifacts and obey its current risk decisions. Otherwise return the requested result in the existing project format.
- Read applicable project instructions and preserve user scope and existing authorization. Use plain explanations with observable examples. Do not change global configuration as a side effect.

## Workflow

This is the Design play: requirements and design compressed into one session, with policy applied while the spec is written.

1. Read the intent, the existing call path, public contracts, persisted data, relevant tests, and every applicable standard: project `AGENTS.md`, security, compliance, UX, API and brand conventions available as skills. State what evidence is current.
2. Describe user-visible behavior, interfaces and data, system boundaries, failure and edge cases, and non-functional requirements. Map each success criterion in the intent to a concrete check. For API or data changes describe old/new compatibility, rollout ordering, migration and rollback limits. For UI changes describe normal, empty, loading and error states, and accessibility where relevant.
3. Flag concerns as you write, especially standards that cannot be satisfied or policies that contradict each other. Name the owner who must decide instead of resolving the conflict silently.
4. Compare alternatives only when they change cost, compatibility, risk or user experience. Select one and explain its tradeoff. Avoid assuming a framework, cloud or datastore.
5. Check the spec against the intent: does it solve the stated problem, and are the open questions answered or carried forward?
6. Make the design concrete enough for a human to decide whether it progresses to Build, consulting a technical lead for higher-risk changes. Reuse applicable prior authorization and flag unresolved high-impact choices.

Output: behavior and contracts, affected boundaries, decision rationale, concerns, and a verification plan. Update spec.md and decisions.md when the lifecycle is active.
