# Risk and authority

Classify by impact and reversibility, not line count. Explain the selected level in one sentence.

| Risk | Trigger | Records |
|---|---|---|
| R0 | Explanation, inspection, diagnosis, review, audit | No persistent artifacts |
| R1 | Bounded reversible change without a public contract, dependency or stored-data change | intent, plan, evidence |
| R2 | User behavior, public interface, dependency, configuration, schema or module boundary changes | R1 + spec, review, decisions |
| R3 | Authentication, authorization, payment, sensitive data, destructive migration, production or broad infrastructure impact | R2 + risk, rollback, approvals |

## Gates by risk

The loop has five human judgment points: intent accepted, spec approved, plan accepted, PR merged by a code owner, release authorized. Risk decides how each one is recorded.

| Gate | R1 | R2 | R3 |
|---|---|---|---|
| Intent accepted | the user's request plus a filled intent.md | same, and the acceptance noted in decisions.md | same |
| Spec approved | no spec | approval noted in decisions.md before Build | `transition --approve-gate spec` with the actual approver |
| Plan accepted | plan.md filled before `transition --stage build` | same | `transition --approve-gate plan` after spec, risk and rollback are filled |
| PR merged | branch protection and code owner review of the actual repository | same | same |
| Release authorized | not applicable for `delivery=local` or `pr` | same | `transition --approve-gate production` in the deploy stage for the exact artifact |

- Use the highest matching level. The user may raise it. An approved downgrade must include its rationale in decisions.md; never reclassify merely to avoid a pending gate.
- Low-blast-radius work with passing checks moves through its gates on the strength of the user's request: this is the playbook's auto-accept path, and it applies only when the surrounding controls exist (project instructions, verified commands, tests the agent can run). Regulated, high-risk and core architectural logic keeps explicit human approval.
- For ordinary implementation, the request authorizes the reversible work needed to complete it. Existing explicit authorization continues across turns.
- For R3, prepare the specification, implementation plan, risk assessment and rollback plan before requesting missing decisions. Both spec and plan decisions are required before entering Build. Approval may already be present in the conversation if it covers those concrete artifacts.
- Production execution requires authorization for the exact environment and artifact. A change with `delivery=local` or `delivery=pr` has no production gate. Set production delivery only when production is part of the user's scope. The agent prepares the release and stops at the production gate.
- Check existing authorization immediately before a consequential action. If missing, finish independent preparation and ask one focused question. Do not insert blanket confirmation gates for reversible local actions or authorized PR creation; an approval prompt during Build puts a person on the critical path of every parallel session.
- A read-only request authorizes inspection only. Never bootstrap a repo during an audit.
- In actual Plan mode do not mutate. The label “Default collaboration mode” does not mean Plan mode.

## Two layers of guardrails

- Advisory controls make compliant behavior likely: `AGENTS.md`, skills, templates, and this plugin's guidance.
- Deterministic controls make violations close to impossible: hooks, CI checks, branch protection, sandboxing, scoped credentials, deployment permissions.
- A policy that must always hold needs a deterministic control behind the skill. The helper checks local records; it is not that control. Enforce production authorization through the actual platform.
- Resolve technical conventions from applicable project instructions. Respect a project's stricter mandated lifecycle controls; surface genuine conflicts with the requested scope.

## Existing tools stay

Jira, GitHub, Figma, Slack and similar systems stay. For every artifact name one source of truth: repository markdown, or the legacy record. Keep cross-references in both directions at minimum: the artifact carries the record ID, the record carries the commit SHA. Do not duplicate every tracker field into local artifacts.
