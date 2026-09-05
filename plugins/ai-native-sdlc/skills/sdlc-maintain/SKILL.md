---
name: sdlc-maintain
description: "Investigate software incidents, operational regressions, dependency drift and maintenance follow-ups. Use for software health, incident or maintenance tasks."
---

# 故障诊断与持续改进

## Scope

- Apply this skill to its named software task. Do not load `$ai-native-sdlc`, bootstrap `.sdlc`, or start other lifecycle stages unless the user explicitly invokes the coordinator.
- If the coordinator is already active, write results into the corresponding change artifacts and obey its current risk decisions. Otherwise return the requested result in the existing project format.
- Read applicable project instructions and preserve user scope and existing authorization. Use plain explanations with observable examples. Do not change global configuration as a side effect.

## Workflow


1. Establish affected service/device/environment and symptom timeline. Read current logs, metrics, recent changes and existing runbooks before choosing a cause.
2. Rank plausible causes by evidence. Use the smallest discriminating diagnostic step and state coverage limits. A clean unit test does not disprove a runtime incident.
3. Separate containment, root-cause correction and regression prevention. Follow read-only scope until a fix is authorized. Preserve original evidence.
4. Turn actionable findings into scoped work with a trigger, acceptance criterion and source link. Link a new change to its originating incident or prior change when the lifecycle is active.
5. Add a useful regression check after an authorized fix. Record observation windows, baseline sources and unresolved uncertainty without inventing metrics or owners.
6. Create scheduled monitoring/notifications only on request. Define target, cadence, meaningful change and stop conditions; keep unchanged runs quiet.

Output: evidence-based diagnosis, action taken within scope, verification and the next owned follow-up. Do not claim continuous monitoring after a one-time inspection.
