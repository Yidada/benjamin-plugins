---
name: ai-native-sdlc
description: "Coordinate a risk-scaled software delivery lifecycle with repository artifacts and evidence. Load only on explicit $ai-native-sdlc invocation. Supports bootstrap, start, resume, status, audit, and close."
---

# AI-Native SDLC

Use only after the user explicitly invokes `$ai-native-sdlc`. This skill coordinates delivery across languages and frameworks. The six companion skills can perform individual tasks without activating this lifecycle.

## First decision

1. Steelman the request in plain language: the real problem, observable outcome, constraints, acceptance criteria, and uncertainty that could change the solution. Make reasonable assumptions visible and continue independent work.
2. Resolve the user's target directory, applicable `AGENTS.md`, Git state, existing plans, and current tooling. A repository can have several languages and independently deployed components.
3. Select the highest applicable risk in [risk-and-routing.md](references/risk-and-routing.md). Read-only work creates no files. In actual Plan mode, inspect and plan only; Default collaboration mode permits authorized implementation.
4. Reuse an unambiguously identified change. When several changes fit, list their IDs and ask which one to resume while continuing independent inspection.

## Commands

| Request | Action |
|---|---|
| `bootstrap` | Inspect commands and boundaries, then initialize the requested Git repo. Preserve its instructions. Fill verified commands in `.sdlc/config.json`; unknown commands stay empty. |
| `start <goal>` | Classify risk, create the appropriate artifacts, fill intent and a concrete plan, then carry authorized work forward. If initialization is needed, perform it within the requested development scope. |
| `resume [id]` | Read current state, relevant artifacts and live diff. Continue from the first unmet requirement. |
| `status [id]` | Read-only state and missing evidence. |
| `audit` | Read-only inspection. Report gaps without repairing or writing a report unless requested. |
| `close [id]` | Validate the final evidence and delivery scope, then close. A local change can close without a production deployment. |

For a folder without Git, use the relevant companion skill and deliver in the requested folder. Explain that tracked lifecycle history needs a Git repository; do not initialize or clone a different target silently.

## Load only the current stage

- Risk or authority decision: [risk-and-routing.md](references/risk-and-routing.md).
- State, bootstrap or closure: [artifact-contracts.md](references/artifact-contracts.md).
- Plan or Design: [plan-design.md](references/plan-design.md).
- Build or Test: [build-test.md](references/build-test.md).
- Release or incident: [deploy-maintain.md](references/deploy-maintain.md).
- Choosing checks for an unfamiliar stack: [project-adapters.md](references/project-adapters.md).

The sequence is Plan → Design → Build → Test → Deploy → Maintain. These are checkpoints, not a requirement to perform deployment or install monitoring. R1 omits Design. Write the implementation plan during Plan/Design, before entering Build.

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

`inspect`, `status`, `validate`, and `audit` are read-only. `start --risk R0` requires no bootstrap and makes no writes. The helper validates records and stage prerequisites. It does not execute tests, authenticate a human, authorize deployment, or intercept other tools. Verify every claimed result against actual tool output. Enforced organization-wide controls belong in CI, branch protection and deployment permissions.

For an R3 decision, use `transition --approve-gate <spec|plan|production> --approver <actual-actor> --note <source-and-scope>`. Record only existing explicit authorization covering the concrete artifact and action. Never invent an approver. Renew a decision when its scope or material artifact changes. Do not ask again when current-session authorization already covers that same decision.

## Completion

- Keep `.sdlc` available for version control alongside the code. Commit or push only within the user's authorized scope.
- Preserve unrelated changes and existing tool/provider choices.
- For failed checks, fix in scope or report the exact remaining limitation. Never replace a failure with a passing label.
- Report the behavior delivered, relevant verification, delivery level, and any material unresolved limitation. Do not claim a local build proves a live integration.
