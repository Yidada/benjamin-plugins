---
name: ai-native-sdlc
description: "Coordinate the AI-native SDLC loop (Plan → Design → Build → Test → Deploy → Maintain) with committed artifacts, human gates and evidence, scaled by risk. Load only on explicit $ai-native-sdlc invocation. Supports bootstrap, start, resume, status, audit, and close."
---

# AI-Native SDLC

Use only after the user explicitly invokes `$ai-native-sdlc`. This skill coordinates delivery across languages and frameworks. The six companion skills run single plays without activating this lifecycle.

## The loop

The lifecycle is a loop, not a pipeline. Every stage ends by committing an artifact that the next stage reads. The commit chain is the audit trail: who asked for what, what the agent produced, and who approved it.

| Stage | Reads | Commits | Gate that fires the next stage |
|---|---|---|---|
| Plan | the originator's problem, issue, or incident | intent.md | owner accepts the intent |
| Design | intent.md, project instructions, policy skills | spec.md | owner approves the spec; technical lead consulted for higher risk |
| Build | intent.md, spec.md | plan.md from plan mode, then the diff and its tests | engineer accepts the plan; nothing is implemented without an accepted plan |
| Test | the diff, plan.md, eval cases | evidence.md | feedback-loop checks pass |
| Deploy | the PR, spec.md, plan.md | review.md findings, release record | code owner merges; release manager authorizes production |
| Maintain | production signals, incidents | incident record and a new intent.md | owner triages: fix now, schedule, or dismiss |

Rules that hold at every stage:

- The agent goes all the way to the production gate and never crosses it. Humans hold the judgment positions; the agent generates, executes, and mechanically verifies.
- Skills and project instructions are advisory controls. Hooks, CI, branch protection, and deployment permissions are the deterministic controls. A policy that must always hold needs a deterministic control behind the skill.
- Risk decides how many artifacts exist and which decisions are recorded explicitly. Low-blast-radius work with passing checks moves through the gates on the user's request. R3 records every gate decision. R1 omits Design. See [risk-and-routing.md](references/risk-and-routing.md).
- Maintain closes the loop: a diagnosis becomes a new linked change whose intent.md re-enters Plan.

## First decision

1. Steelman the request in the originator's own words: the real problem, who is affected, what better looks like, constraints, out of scope, and the uncertainty that could change the solution. Make assumptions visible and continue independent work.
2. Resolve the target directory, applicable `AGENTS.md`, Git state, existing changes, and current tooling. A repository can have several languages and independently deployed components.
3. Select the highest applicable risk in [risk-and-routing.md](references/risk-and-routing.md). Read-only work creates no files. In actual Plan mode, inspect and plan only; Default collaboration mode permits authorized implementation.
4. Reuse an unambiguously identified change. When several changes fit, list their IDs and ask which one to resume while continuing independent inspection.

## Commands

| Request | Action |
|---|---|
| `bootstrap` | Inspect commands and boundaries, then initialize the requested Git repo. Preserve its instructions. Fill verified commands in `.sdlc/config.json`; unknown commands stay empty. |
| `start <goal>` | Classify risk, create the artifacts, capture intent.md, then carry authorized work through the loop. If initialization is needed, perform it within the requested development scope. |
| `resume [id]` | Read current state, the artifacts the current stage reads, and the live diff. Continue from the first unmet requirement. |
| `status [id]` | Read-only state, missing evidence, and the next gate. |
| `audit` | Read-only inspection. Report gaps without repairing or writing a report unless requested. |
| `close [id]` | Validate the final evidence and delivery scope, then close. A local change can close without a production deployment. |

For a folder without Git, use the relevant companion skill and deliver in the requested folder. Explain that tracked lifecycle history needs a Git repository; do not initialize or clone a different target silently.

## Load only the current stage

- Risk or authority decision: [risk-and-routing.md](references/risk-and-routing.md).
- State, bootstrap, or closure: [artifact-contracts.md](references/artifact-contracts.md).
- Plan or Design: [plan-design.md](references/plan-design.md).
- Build or Test: [build-test.md](references/build-test.md).
- Deploy or Maintain: [deploy-maintain.md](references/deploy-maintain.md).
- Choosing checks for an unfamiliar stack: [project-adapters.md](references/project-adapters.md).
- Reporting stage metrics for status, audit, or close: [measures.md](references/measures.md).

Stages are checkpoints, not an obligation to deploy or to install monitoring. Plan mode runs before `transition --stage build`: entering Build records that plan.md is accepted and implementation may begin.

## Helper

Resolve this skill's installed directory and use its absolute script path. Do not assume the working directory is the plugin directory.

```text
python3 <skill-dir>/scripts/sdlc.py --repo <repo> inspect
python3 <skill-dir>/scripts/sdlc.py --repo <repo> bootstrap
python3 <skill-dir>/scripts/sdlc.py --repo <repo> start --title "<goal>" --risk R2 --delivery local
python3 <skill-dir>/scripts/sdlc.py --repo <repo> transition --change-id <id> --stage design
python3 <skill-dir>/scripts/sdlc.py --repo <repo> validate --change-id <id> --for-close
python3 <skill-dir>/scripts/sdlc.py --repo <repo> close --change-id <id>
```

`inspect`, `status`, `validate`, and `audit` are read-only. `start --risk R0` requires no bootstrap and makes no writes. The helper validates records and stage prerequisites. It does not execute tests, authenticate a human, authorize deployment, or intercept other tools. Verify every claimed result against actual tool output. Enforced organization-wide controls belong in CI, branch protection, hooks, and deployment permissions.

For an R3 decision, use `transition --approve-gate <spec|plan|production> --approver <actual-actor> --note <source-and-scope>`. Record only existing explicit authorization covering the concrete artifact and action. Never invent an approver. Renew a decision when its scope or material artifact changes. Do not ask again when current-session authorization already covers that same decision.

## Completion

- Keep `.sdlc` available for version control alongside the code. Commit or push only within the user's authorized scope.
- Preserve unrelated changes and existing tool/provider choices.
- For failed checks, fix in scope or report the exact remaining limitation. Never replace a failure with a passing label.
- When the same mistake appears twice, add the correction to the repository's `AGENTS.md` within scope, so the next session starts with it.
- Report the behavior delivered, relevant verification, delivery level, and any material unresolved limitation. Do not claim a local build proves a live integration.
