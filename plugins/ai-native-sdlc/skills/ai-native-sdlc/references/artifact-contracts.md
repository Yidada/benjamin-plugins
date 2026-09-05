# Artifacts and state

Each tracked change lives in `.sdlc/changes/<change-id>/`. Bootstrap appends one integration section to AGENTS.md and preserves existing content. It never edits CLAUDE.md. The helper requires `.sdlc` to be available to Git, but does not commit anything.

| File | Minimum useful content |
|---|---|
| intent.md | Source problem, outcome, constraints, exclusions, acceptance examples |
| spec.md | Behavior, contracts, failure paths, compatibility, criterion-to-check mapping |
| plan.md | Verified files/commands, ordered changes, validation and existing authorization |
| evidence.md | Exact commands or manual checks, timestamp, environment, actual outcome, gaps |
| review.md | Reviewed scope, findings, resolutions and residual risk |
| decisions.md | Tradeoffs, accepted deviations and risk-level decisions |
| risk.md | Protected assets, impact, controls, stop conditions and responsible role |
| rollback.md | Trigger, prerequisites, steps, verification and recovery limits |
| approvals.md | Append-only recorded decisions with actual actor and source/scope |

R1 requires intent, plan and evidence. R2 adds spec, review and decisions. R3 adds risk, rollback and approvals. Avoid expanding the number of documents beyond the selected contract.

State schema version 1 retains `change_id`, `title`, `risk`, `current_stage`, `status`, `required_artifacts`, `gates`, `created_at`, `updated_at`. New changes also carry `delivery` (`local`, `pr`, `production`). Legacy states without delivery retain the old production-gate interpretation; never silently rewrite them.

Stages: plan, design, build, test, deploy, maintain, closed. R1 skips design. Terminal statuses complete and cancelled cannot be reopened with transition. A follow-up gets a new change linked by parent_change_id or trigger.

Stage checks:

- Enter Design: intent is filled.
- Enter Build: intent and plan are filled; R2/R3 also require spec; R3 requires risk, rollback and approved spec + plan gates.
- Enter Test: no additional completion claim; run checks against the implemented behavior.
- Enter Deploy: all required artifacts are filled, evidence is pass, R2/R3 review is approved. This stage prepares the requested delivery; it does not itself deploy.
- Enter Maintain: production delivery requires its recorded production approval. Record actual delivery result and follow-up conditions.
- Close: all required records, passing evidence, approved review when applicable, and all applicable R3 decisions.

Replace each REQUIRED template marker with facts. Blank files fail validation. `- Outcome: pass` and `- Verdict: approved` are explicit record labels. Their presence is a structural check, not independent proof of test execution or reviewer identity. The agent must inspect the actual outputs and final diff. For stronger controls, wire verified commands and external review requirements into the project's CI.

Writes validate inputs before mutation and replace individual state files atomically. Multi-file operations have no concurrent-writer transaction guarantee. Use one writer per change.
