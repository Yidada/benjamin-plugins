# Deploy and Maintain

## Deploy: review runs both ways, and the agent stops at the production gate

Resolve the requested delivery level: local verified change, PR, staging, or production. The helper represents staging preparation as local unless production is explicitly in scope. Do not promote an artifact beyond the requested level.

### Review passes

Every PR gets the same passes, with findings ranked by severity:

- bugs and logic errors;
- security and vulnerabilities;
- compliance against spec.md, plan.md, and the project's design principles, including whether the final diff still matches plan.md.

Rank Important findings before Nits and cap nits at five per review. Skip generated paths and anything CI already enforces. A finding never approves or blocks a PR on its own: branch protection and code owner approval decide, and the agent that wrote the code cannot approve it. Record the passes and the resolutions in review.md; label a self-review as such. When a review flags the same mistake for the second time, the correction goes into `AGENTS.md` as part of that review.

Review is bidirectional. On its own PR the agent addresses review comments, fixes failing checks, and pushes until the PR waits only on code owner approval. Do not narrate each fix; the diff is the record.

### Hooks as approval gates

Build used hooks to allow or block with no human involved. A hook can also ask, pausing an action until a specific person approves; that is what release gating needs. The surviving human gates (change sign-off, release authorization, edits to protected paths) belong in the repository's hook or CI configuration, and non-negotiable ones in settings the engineer cannot switch off. A block explains itself: the reason and the route to approval appear in the output. Do not install global hooks, change branch protection, or add a hosting provider merely because this plugin exists.

### CI/CD

- Everything the agent writes arrives as a PR through branch protection; there is no direct path to the default branch.
- Agent jobs run sandboxed with short-lived scoped tokens and no standing production credentials. Do not broaden access to solve a tooling limitation.
- Tier autonomy by environment: development is open, staging in between, production requires the release manager's authorization enforced by the platform's gate.
- Before an external action, identify the target, artifact/commit, validation result, rollback limits, and existing authorization. Reuse session authorization covering the action. If a required decision is missing, finish preparation and show the concrete result for approval.
- Observe actual remote status and verify deployed behavior when tools allow. A successful build or created pipeline does not establish a successful deployment. A PR, a build, a successful upload, and a healthy running release are different completion levels.
- Rollback is the most rehearsed path: a single documented command, exercised in staging, because Maintain calls it when a control band is breached. Perform rollback only when authorized or covered by an approved runbook.

Measure Deploy by time to first review, the share of review comments resolved without a human touching the branch, defects and vulnerabilities caught before merge versus escaping to production, time spent waiting on each approval gate, and the share of pipeline failures triaged without paging a human.

## Maintain: close the loop

A trigger, not a person, starts this stage: a control-band breach, a ticket, a channel message, or a schedule. The agent diagnoses, acts only through gated routes, and writes what it found as a new intent.md that re-enters Plan. People triage and review the work; they no longer have to start it.

1. Establish the affected service, environment, and symptom timeline. Read current logs, metrics, recent changes, and existing runbooks before choosing a cause. Preserve the timeline and raw evidence.
2. Rank hypotheses by evidence and take the smallest discriminating diagnostic step. State coverage limits: a clean unit test does not disprove a runtime incident.
3. Respond in tiers. Log-only for small deviations. Read-only diagnosis for clear anomalies. Action for severe breaches, and only by opening a PR into the review gate or triggering a pre-approved runbook such as the rehearsed rollback. Detection stays deterministic; keep thresholds in version-controlled configuration when the user asks for monitoring.
4. Write the diagnosis as intent.md in the Plan format: the anomaly and its evidence, a proposed outcome, affected systems, open questions. Start it as a new change linked by `--parent-change-id` or `--trigger`; never reopen a terminal change.
5. The service owner triages the queue: fix now, schedule, or dismiss. Dismissals tune the thresholds and reduce noise. Separate containment, root-cause correction, and regression prevention.
6. When a fix ships, add an eval or regression check for the incident so the class of issue is protected going forward.

Chat is a channel too. When an incident is handled in a channel, the channel is the audit trail: request, diagnosis, authorization, and fix stay where the incident was handled, and anything larger than a small bounded fix becomes an intent.md.

Maintain can also be a small handoff describing relevant signals, owner, rollback trigger, and a follow-up condition. It does not require starting a service or scheduler. Set up monitors, periodic jobs, or notifications only when the user requests them and the needed scope is available; keep unchanged, non-actionable runs quiet, and never describe a one-time inspection as continuous monitoring.

Close local delivery after the requested local work and evidence are complete. Use a production gate only for production-scoped R3 changes. Name unresolved external validation, avoid invented owners or baselines, and keep historical records intact.

Measure Maintain by time from trigger to an intent.md in the triage queue, the share of findings that become merged fixes, and repeat incidents of the same class.
