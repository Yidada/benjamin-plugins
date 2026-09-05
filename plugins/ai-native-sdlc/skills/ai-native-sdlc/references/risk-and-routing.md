# Risk and authority

Classify by impact and reversibility, not line count. Explain the selected level in one sentence.

| Risk | Trigger | Records |
|---|---|---|
| R0 | Explanation, inspection, diagnosis, review, audit | No persistent artifacts |
| R1 | Bounded reversible change without a public contract, dependency or stored-data change | intent, plan, evidence |
| R2 | User behavior, public interface, dependency, configuration, schema or module boundary changes | R1 + spec, review, decisions |
| R3 | Authentication, authorization, payment, sensitive data, destructive migration, production or broad infrastructure impact | R2 + risk, rollback, approvals |

- Use the highest matching level. The user may raise it. An approved downgrade must include its rationale in decisions.md; never reclassify merely to avoid a pending gate.
- For ordinary implementation, the request authorizes the reversible work needed to complete it. Existing explicit authorization continues across turns.
- For R3, prepare the specification, implementation plan, risk assessment and rollback plan before requesting missing decisions. Both spec and plan decisions are required before entering Build. Approval may already be present in the conversation if it covers those concrete artifacts.
- Production execution requires authorization for the exact environment and artifact. A change with `delivery=local` or `delivery=pr` has no production gate. Set production delivery only when production is part of the user's scope.
- Check existing authorization immediately before a consequential action. If missing, finish independent preparation and ask one focused question. Do not insert blanket confirmation gates for reversible local actions or authorized PR creation.
- A read-only request authorizes inspection only. Never bootstrap a repo during an audit.
- In actual Plan mode do not mutate. The label “Default collaboration mode” does not mean Plan mode.
- Resolve technical conventions from applicable project instructions. Respect a project's stricter mandated lifecycle controls; surface genuine conflicts with the requested scope.
- Skills guide decisions. The CLI checks local records. Neither establishes a tamper-resistant approval boundary.
