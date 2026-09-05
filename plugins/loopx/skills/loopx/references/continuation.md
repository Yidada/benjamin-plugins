# Driver, receipts, and recovery

LoopX determines eligible work and scheduling hints. The host provides wake-ups.
After verified goal registration, generate its packet:

```bash
loopx heartbeat-prompt --thin --goal-id GOAL_ID --agent-id AGENT_ID \
  --agent-scope 'The authorized scope' --cli-bin CLI_BIN
```

Use the observed host's runtime profile from help or the guided-start packet.
Read the full lifecycle contract when the thin packet delegates receipt or
recovery details. Preserve goal, agent, executable, project, registry route and
capability declarations in the driver.

## Activation

| Observed host | Continuation |
| --- | --- |
| Codex App with automation tools and persistent project access | Install/update one matched heartbeat using its generated prompt and a supported schedule; read back the saved task. |
| Codex CLI or App over SSH with visible Goal support | Use the returned visible `/goal` handoff. Verify activation through the host; otherwise provide the exact activation text and report it pending. |
| Custom runner | Use its verified scheduler/LoopX bridge and inspect execution receipts. |
| Shell-only or temporary chat workspace | Complete bounded work now, preserve a handoff on durable project storage, and report automatic continuation unavailable. |

Creating a plugin does not create or authorize a background job. A request to
run a goal over time authorizes relevant scheduling. Match goal, project and
agent before reusing a task. Verify the scheduler can access project, CLI and
state after this session ends; otherwise leave activation pending.

Do not fabricate a three-minute cadence if the scheduler cannot support it.
Keep next-due checks in the execution guard, use a supported host cadence, and
explain the effective delay when material. A text-only reminder is not a driver.

## Each wake

1. Obtain a fresh guard for the same goal and agent. Use the host turn ID when
   receipts require it; reuse it only for retries of that same turn.
2. Follow permitted delivery/question/wait/repair/quiet behavior. Notification
   suppression alone does not prohibit work. A denied delivery guard does.
   Independent work needs its own permitted lane and boundary.
3. Claim and perform bounded work, submit actual validation and effect readback,
   preserve evidence identity and successors, then spend once after acceptance.
   Retain failed attempts and use the recovery protocol for interrupted writes.
4. Apply scheduler hints only to the matched driver, at most once per hint per
   turn. ACK only after host readback matches. On failure, record the returned
   failure hint once; do not ACK or retry in a tight loop.
5. Keep waiting monitors alive with backoff. Stop/pause when the user requests it
   or the validated terminal/no-progress contract requires it. One denied wake
   alone does not justify stopping a waiting goal.

## Evidence and closure

Kernel validation determines accepted transitions. Tie evidence to the actual
revision and checks; distinguish local tests, external CI, review and merge.
Preserve unresolved acceptance gaps, monitors, dependencies, blocked/deferred
successors and replan obligations until validated resolution. Never patch state
JSON to generate a terminal marker.

Report provider charges only when available. LoopX slots do not establish zero
token cost for waits, questions or failed turns.
