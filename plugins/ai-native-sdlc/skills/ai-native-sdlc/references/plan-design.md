# Plan and Design

## Plan: capture intent as intent.md

Intent is captured once, in the originator's own words, as a version-controlled artifact the next stage can act on. It must be readable by the owner without engineering knowledge and structured enough for the agent to act on directly.

1. Start from the source: the request, issue, incident record, or band breach. The originator describes what cannot be done today, who is affected, what better looks like, and what is out of scope. No formal language required.
2. Brainstorm until the idea is concrete. Ask the questions an analyst would ask: scope, users, constraints, what success looks like. Separate facts from assumptions. Inspect the affected product or code path only as far as needed to challenge the proposed solution; do not treat the first suggested implementation as a fixed requirement.
3. Write intent.md with the template fields: source, problem, proposed outcome, affected users and systems, constraints, out of scope, success criteria as observable examples, open questions. Reference external issue IDs without duplicating tracker fields.
4. The originator corrects anything misunderstood. Then commit intent.md with the code. Author and timestamp join the record.
5. The owner's acceptance sends the intent into Design. For R2/R3 note that acceptance in decisions.md. Ask only for missing choices that change scope or correctness.

Measure planning by time from first conversation to a committed intent.md, and by intent.md edits made after the first spec.md commit. Read both from Git history; never manufacture baselines.

## Design: requirements and design in one session

Requirements and design are compressed into one working session, guided by the organization's standards, and versioned in Git. Policy is applied while the spec is written, not discovered in a review weeks later.

1. Read intent.md, the existing call path, public contracts, persisted data, relevant tests, and every applicable standard: project `AGENTS.md`, brand, security, compliance, UX, and API conventions encoded as skills. State what evidence is current.
2. Produce spec.md: user-visible behavior, interfaces and data contracts, system boundaries, failure and edge cases, non-functional requirements, and acceptance examples that map each criterion to a proposed check. For API or data changes describe old/new compatibility, rollout ordering, migration, and rollback limits. For UI changes describe normal, empty, loading, and error states, and accessibility where relevant.
3. Flag concerns explicitly, especially where two policies contradict or a standard cannot be satisfied. Route each concern to its policy owner instead of resolving it silently.
4. Compare alternatives only when they change cost, compatibility, risk, or user experience. Select one and record the tradeoff in decisions.md. Use a small diagram or prototype only when it resolves uncertainty.
5. Review the spec against the intent: does it solve the stated problem? Are the open questions answered or carried forward? Commit spec.md beside intent.md; the pair records what was asked for and what was decided.
6. A human decides whether spec and intent progress to Build, consulting a technical lead for anything classed as higher risk. For R3, present spec, plan, risk, and rollback together, record existing decisions, and ask only for the missing ones. No implementation begins until spec and plan decisions cover the current design.

Measure design by elapsed time between the intent.md commit and the spec.md commit, and by spec.md commits dated after the first plan.md commit for the same change.

## Hand-off to Build

Build starts in plan mode. plan.md is written from intent.md and spec.md before any code and is accepted before `transition --stage build`; see [build-test.md](build-test.md). Unknown details need a small investigation, not an invented answer.
