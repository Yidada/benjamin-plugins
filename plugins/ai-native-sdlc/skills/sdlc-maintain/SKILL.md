---
name: sdlc-maintain
description: "Investigate software incidents, operational regressions, dependency drift and maintenance follow-ups; diagnose from a trigger, act only through gated routes, and write findings back as new intent. Use for software health, incident or maintenance tasks."
---

# 故障诊断与持续改进

## Scope

- Apply this skill to its named software task. Do not load `$ai-native-sdlc`, bootstrap `.sdlc`, or start other lifecycle stages unless the user explicitly invokes the coordinator.
- If the coordinator is already active, write results into the corresponding change artifacts and obey its current risk decisions. Otherwise return the requested result in the existing project format.
- Read applicable project instructions and preserve user scope and existing authorization. Use plain explanations with observable examples. Do not change global configuration as a side effect.

## Workflow

This is the Maintain play: a trigger starts the work, the agent diagnoses, acts only through gated routes, and closes the loop by writing a new intent.

1. Establish the trigger (band breach, ticket, channel message, schedule, or the user's request), the affected service or environment, and the symptom timeline. Read current logs, metrics, recent changes and existing runbooks before choosing a cause. Preserve the original evidence.
2. Rank plausible causes by evidence. Use the smallest discriminating diagnostic step and state coverage limits. A clean unit test does not disprove a runtime incident.
3. Respond in tiers: log a small deviation, diagnose read-only a clear anomaly, and act on a severe breach only by opening a PR into the review gate or running a pre-approved runbook such as the rehearsed rollback. Follow read-only scope until a fix is authorized.
4. Write the diagnosis as intent in the Plan format: the anomaly and its evidence, a proposed outcome, affected systems, open questions, and the link to the originating incident or prior change. Separate containment, root-cause correction and regression prevention.
5. Hand the owner a triage decision: fix now, schedule, or dismiss. A dismissal tunes the threshold that fired. After an authorized fix ships, add a regression check or eval so the class of issue stays protected. Record observation windows and baseline sources without inventing metrics or owners.
6. Create scheduled monitoring or notifications only on request. Keep detection deterministic and version-controlled, define target, cadence, meaningful change and stop conditions, and keep unchanged runs quiet. When an incident is handled in a chat channel, the channel is the audit trail; anything larger than a small bounded fix becomes an intent.

Output: evidence-based diagnosis, action taken within scope, verification, and the new intent or owned follow-up. Do not claim continuous monitoring after a one-time inspection.
