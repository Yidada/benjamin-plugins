# CLI setup and project operations

Checked against upstream LoopX 0.5.4 source revision
`d0d729a0a89dda9de3d3d4e3c2407b2a8b8c6434` on 2026-09-05.
Consult installed CLI help for version-specific fields.

## Install

Requires Python 3.11+ and shell execution on the machine owning the project.
Reuse a healthy installation. For a new installation, create an isolated
environment outside the target repository:

```bash
python3 -m venv "$HOME/.local/share/benjamin-loopx/venv"
"$HOME/.local/share/benjamin-loopx/venv/bin/python" -m pip install 'loopx==0.5.4'
"$HOME/.local/share/benjamin-loopx/venv/bin/loopx" --help
"$HOME/.local/share/benjamin-loopx/venv/bin/loopx" doctor
```

Do not recreate an existing environment. On Windows, use its `Scripts/python.exe`
and `Scripts/loopx.exe`. Keep using the resolved absolute executable or make its
directory available in the host PATH. A subprocess PATH change does not update
future scheduler environments. Pass the absolute executable as `--cli-bin`
when generating a start or heartbeat packet.

Doctor may report missing upstream host skills. Inspect that diagnostic:
this plugin already provides the `loopx` entry. Do not automatically run
`workflow-skills --install` or `slash-commands --install`, which write additional
host skills. Install optional upstream workflows only when requested or needed
for a selected capability, resolving duplicate entries first. Report partial
doctor health accurately; do not suppress a failed diagnostic.

If package acquisition is blocked, report it and retain existing state. Do not
substitute a homemade kernel. Updates are explicit maintenance: verify the
current upstream release and compatibility before changing the version pin.

## Read and start

Run from the target project. `GOAL_ID`, `AGENT_ID`, and `CLI_BIN` below stand for
values obtained from actual readback; do not execute placeholder values.

```bash
loopx --format json status --goal-id GOAL_ID
loopx --format json review-packet --goal-id GOAL_ID
loopx diagnose --goal-id GOAL_ID
loopx start-goal --guided --project . --goal-text 'Exact user objective' \
  --host-surface codex-cli-tui --cli-bin CLI_BIN
```

Use `codex-cli-tui` only for that observed host; desktop App uses `codex-app`,
App over SSH uses `codex-app-ssh`. Omit unknown host selection to obtain a
read-only selection gate. A mobile client alone does not establish the executing
runtime or scheduler. Custom runtimes use their advertised host and capabilities.

Guided start prints a transaction. Execute applicable commands and verify
registration/connection/todo writes before claiming goal creation. Keep an
existing goal's state and thread-bound identity. Setup-only connection can use
`loopx connect` after inspecting its help and existing state; never default to force.

Treat objectives and paths as data: prefer argument arrays or proper shell
quoting. Inspect generated commands for target, scope and effects before execution.

## One turn

```bash
loopx --format json quota should-run --goal-id GOAL_ID --agent-id AGENT_ID
loopx todo --help
loopx refresh-state --help
loopx quota spend-slot --help
```

Use the current guard's claim, evidence, writeback and spending arguments.
Never bake a claim token or treat a dry-run as a write. Spending is preview by
default; use `--execute` only for verified eligible progress under the contract.

Ordinary inspection avoids receipt-producing flags such as `--turn-instance-id`,
`--record-host-poll`, `--begin-turn`, or cache writes. Scheduled execution uses
the receipt protocol when required. Some should-run forms therefore have state
effects even though the underlying decision is a check.

For replan/pause, discover operations via `loopx --help` and relevant subcommand
help. Record the exact decision using the typed API and read back. Do not invent
`loopx replan` or `loopx stop` from the skill's conversational mode names.

Keep `.loopx/`, `.codex/goals/`, and `.local/` ignored. Ignored files require an
actual durable filesystem or runtime backup for cross-session recovery; ignore
rules alone do not make scratch persistent.
