---
name: loopx
description: Start, resume, inspect, and replan durable long-running agent goals with the official LoopX CLI. Use for LoopX requests and multi-session engineering or research tasks that need persistent state, evidence, quotas, and controlled continuation.
---

# LoopX

Use the official LoopX kernel for goal state and transitions. This plugin supplies
the operating workflow; the installed CLI supplies validation and persistence.
Use the user's selected project and existing session authorization throughout.

## Route the request

| Request | Action |
| --- | --- |
| `start <objective>` or a new concrete long-running objective | Preview guided start, create the authorized goal and ordered todos, execute one permitted bounded turn. |
| `connect` / setup | Connect and verify the environment; stop after setup. |
| `status` / `report` / `review` | Read status or a review packet without initializing or modifying a goal. |
| `resume` / continue | Recover the existing goal and session identity, obtain a fresh guard, and continue permitted work. |
| `replan <change>` | Record the requested change through the current CLI's typed transition; preserve prior evidence and lineage. |
| `pause` / `stop` | Change only the selected goal's verified driver using its supported lifecycle operation; report any running turn separately. |

These are conversational modes, not additional CLI subcommands. Read
[operations.md](references/operations.md) for command shapes and
[continuation.md](references/continuation.md) when executing or scheduling.

## Establish the environment

Resolve the target project from the request or current project workspace. Never
initialize the plugin checkout or temporary workspace as the user's target by
accident. If multiple projects remain plausible, resolve the target before writing.

Run `scripts/preflight.py --project <absolute-project>` from this skill directory.
It reads registry metadata and locates the executable without executing or
installing LoopX. It does not establish runtime health. Follow with the actual
`loopx doctor` for setup/diagnosis. Distinguish missing CLI, invalid state, and
unavailable project access. For pure status, an absent registry means no local
goal to inspect; do not fall through to connect or search all other projects.

For requested setup with no CLI, follow the scoped installation path in
operations.md. Do not register duplicate global `loopx` skills over this plugin.
Keep the plugin version separate from the kernel version. Follow current help
and generated packets when the installed version differs from the reference.

## Start or reconnect

1. Preserve the exact objective and extract testable acceptance conditions,
   scope, known authorization boundaries, and intended continuation. Reuse
   decisions already provided; ask only for a material unresolved choice.
2. Inspect existing state. Run `start-goal --guided` with the exact host and
   project. Its output is a **preview**, not a created goal.
3. Follow returned setup/registration commands within scope. Resolve goal and
   agent IDs from readback or a verified thread binding. Never take over an agent
   because it is the only registered agent. Unknown host or identity gates need
   actual evidence. Declare only capabilities that the host really exposes.
4. Write a minimal ordered todo plan through the CLI. Record scope, acceptance
   conditions, and quota using the installed contract. Never overwrite a
   registry, force bootstrap to edit a plan, or manufacture approval records.
   Preserve ignore rules and ignore private runtime directories before creation.
5. Read back status, obtain a fresh interaction contract, and complete a
   permitted bounded turn for a delivery request. Setup-only ends with verified
   setup and the next action.

## Continue with evidence

At each eligible turn, use the latest `quota should-run` interaction contract.
Validate goal, identity, scope, and selected todo before acting. Interpret the
structured contract; the article's five explanatory labels are not a guaranteed
one-to-one mapping to raw CLI enums.

| Decision | Behavior |
| --- | --- |
| Run | Claim the authorized slice, implement, validate, submit evidence. |
| Ask | Surface the concrete unresolved question; an independent lane may continue only when the current guard expressly permits it. |
| Wait | Preserve waiting state and follow the next observation time. |
| Repair | Repair the supported inconsistency within the returned boundary, then recheck. |
| Quiet | End without delivery work or quota spending. |

Use the CLI's validated todo/refresh/receipt protocol. A preview or zero process
exit alone is insufficient: inspect `ok`, `written`, validation errors and state
as applicable. Spend once only after accepted validated progress. Slots are
logical accounting; provider token charges can still accrue for checks or failures.

After interruption, inspect the receipt, claim/lease and evidence before retrying.
Reuse the same identity for retries of the same turn. Preserve failures; do not
declare an unclosed turn successful or replay an external effect before checking
its actual result.

## Completion and changes

Trust the kernel's current validated goal-closure result. Check acceptance gaps,
blocked/deferred successors, due monitors, CI/review obligations, and pending
replanning. Missing lists/evidence must not be interpreted as zero. Todo
completion alone cannot establish goal completion.

Record changed direction through installed replan/configuration commands. Keep
prior records, supersession and lineage. A goal change does not grant external
permissions. If AI-Native SDLC is also used, reference its acceptance/evidence
artifacts while keeping LoopX as the continuation state authority; avoid
divergent copies of approval or status records.

Report in the user's language: objective, verified progress/evidence, blocker
or concrete question, next action, and driver state. Distinguish **prepared**,
**connected**, **driver active**, **waiting**, and **validated complete** by
readback. Never claim that the plugin alone keeps working after chat ends or
that it provides a Multica connection.
