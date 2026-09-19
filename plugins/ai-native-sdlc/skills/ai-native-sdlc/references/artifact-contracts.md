# Artifacts and state

Each tracked change lives in `.sdlc/changes/<change-id>/`. Bootstrap appends one integration section to AGENTS.md and preserves existing content. It never edits CLAUDE.md. The helper requires `.sdlc` to be available to Git, but does not commit anything.

Every artifact is committed evidence that the next stage reads. Keep the chain readable in both directions: intent.md → spec.md → plan.md → the diff and its tests → evidence.md → review.md and the PR → the incident record → the next intent.md.

| File | Written in | Read by | Minimum useful content |
|---|---|---|---|
| intent.md | Plan | Design (Build for R1) | Source, problem, proposed outcome, affected users and systems, constraints, out of scope, success criteria, open questions |
| spec.md | Design | Build, Deploy review | Behavior, contracts, boundaries, failure paths, non-functional requirements, acceptance examples, concerns and policy conflicts, intent check |
| plan.md | Plan mode, before Build | Build, Deploy review | Repository facts, files that change, order of work, risks, proof, gates and authorization |
| evidence.md | Build and Test | Deploy, close | Exact commands or manual checks, timestamp, environment, actual outcome, gaps |
| review.md | Deploy | Close, Maintain | Reviewed scope, findings per pass, plan sync, residual risk, repeated mistakes moved to AGENTS.md |
| decisions.md | Any stage | Every later stage | Gate acceptances, tradeoffs, accepted deviations, risk-level decisions |
| risk.md | Design | Plan gate, Deploy | Protected assets, blast radius, controls, stop conditions, responsible role |
| rollback.md | Design | Deploy, Maintain | Trigger, prerequisites, rehearsed steps, verification, recovery limits |
| approvals.md | R3 gates | Audit | Append-only recorded decisions with actual actor and source/scope |

R1 requires intent, plan and evidence. R2 adds spec, review and decisions. R3 adds risk, rollback and approvals. Avoid expanding the number of documents beyond the selected contract.

State schema version 1 retains `change_id`, `title`, `risk`, `current_stage`, `status`, `required_artifacts`, `gates`, `created_at`, `updated_at`. New changes also carry `delivery` (`local`, `pr`, `production`). Legacy states without delivery retain the old production-gate interpretation; never silently rewrite them.

Stages: plan, design, build, test, deploy, maintain, closed. R1 skips design. Terminal statuses complete and cancelled cannot be reopened with transition. A follow-up, including an incident diagnosis from Maintain, gets a new change linked by `parent_change_id` or `trigger`.

Stage checks:

- Enter Design: intent is filled and accepted.
- Enter Build: intent and plan are filled; the plan is accepted; R2/R3 also require spec; R3 requires risk, rollback and approved spec + plan gates. Plan mode happens before this transition.
- Enter Test: no additional completion claim; run checks against the implemented behavior.
- Enter Deploy: all required artifacts are filled, evidence is pass, R2/R3 review is approved. This stage prepares the requested delivery; it does not itself deploy.
- Enter Maintain: production delivery requires its recorded production approval. Record actual delivery result and follow-up conditions.
- Close: all required records, passing evidence, approved review when applicable, and all applicable R3 decisions.

Replace each REQUIRED template marker with facts. Blank files fail validation. `- Outcome: pass` and `- Verdict: approved` are explicit record labels. Their presence is a structural check, not independent proof of test execution or reviewer identity. The agent must inspect the actual outputs and final diff. For stronger controls, wire verified commands and external review requirements into the project's CI and branch protection.

Writes validate inputs before mutation and replace individual state files atomically. Multi-file operations have no concurrent-writer transaction guarantee. Use one writer per change.
