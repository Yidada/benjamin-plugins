# Plan and Design

Plan starts with source evidence from the request, issue or incident. Steelman the problem before selecting an implementation. Separate facts from assumptions, list acceptance examples and identify the smallest useful scope.

Inspect the actual entry point, callers, tests and data boundaries. Reuse existing plans or issue links as sources of truth. Record external issue IDs in local artifacts without duplicating every tracker field.

For R2/R3, write a spec with normal behavior, rejected/empty/error behavior, interface and persistence compatibility, and recovery conditions. Map each acceptance criterion to a proposed check. Use a small diagram or prototype only when it resolves uncertainty. Record consequential alternatives and the chosen tradeoff.

Write plan.md during these stages, before implementation. Name relevant files, available verification commands, dependencies and existing approvals. Unknown details need a small investigation, not an invented answer.

For R3, present the concrete spec, plan and risk/rollback records together. Record any existing decisions and ask only for missing decisions. No implementation begins until spec and plan decisions cover the current design.

Use time to reviewable intent and later rework to evaluate planning quality. Never manufacture baseline metrics.
