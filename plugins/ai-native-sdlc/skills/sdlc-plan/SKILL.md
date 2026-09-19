---
name: sdlc-plan
description: "Capture a software request as intent in the originator's own words: problem, outcome, affected users and systems, constraints, out of scope, success examples, open questions. Use for software planning or ambiguous development requests."
---

# 需求意图与规划

## Scope

- Apply this skill to its named software task. Do not load `$ai-native-sdlc`, bootstrap `.sdlc`, or start other lifecycle stages unless the user explicitly invokes the coordinator.
- If the coordinator is already active, write results into the corresponding change artifacts and obey its current risk decisions. Otherwise return the requested result in the existing project format.
- Read applicable project instructions and preserve user scope and existing authorization. Use plain explanations with observable examples. Do not change global configuration as a side effect.

## Workflow

This is the Plan play: intent is captured once, in the originator's own words, as an artifact the next stage can act on.

1. Start from the source: the request, issue, incident, or metric. Keep the originator's words for what cannot be done today, who is affected, what better looks like, and what is out of scope. Distinguish evidence from assumptions.
2. Brainstorm until the idea is concrete. Ask the questions an analyst would ask: scope, users, constraints, what success looks like. Inspect the affected product or code path only far enough to challenge the proposed solution, and explain a material conflict with the user's goal. Do not treat the first suggested implementation as a fixed requirement unless the user makes it one.
3. Write the intent: source, problem, proposed outcome, affected users and systems, constraints, out of scope, success criteria as observable examples, open questions. Carry over existing decisions and issue references without duplicating the tracker.
4. Let the originator correct anything misunderstood. Ask only for missing choices that change scope or correctness, and continue independent investigation meanwhile.
5. When the user asks for an implementation plan, run plan mode without editing code: files that change, order of work, risks, proof. A request for a plan yields a plan; an implementation request continues into authorized work through `$sdlc-build`.

Output: a concise intent readable without engineering knowledge, plus unresolved questions. Use the existing intent.md (and plan.md when a plan was requested) when the lifecycle is active.
