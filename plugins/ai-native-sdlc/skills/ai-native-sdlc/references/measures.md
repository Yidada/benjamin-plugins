# Measures

Report a measure only when its source exists: Git history, CI logs, the PR history, the incident tracker, or the metrics store. Never manufacture a baseline, an owner, or a target. When a source is missing, name it as the gap.

| Stage | Leading (read early) | Lagging (read later) |
|---|---|---|
| Plan | Time from first conversation to a committed intent.md | Share of intents accepted into Design; intent.md edits after the first spec.md commit |
| Design | Time between the intent.md commit and the spec.md commit | spec.md commits dated after the first plan.md commit for the same change |
| Build | First-pass CI success for agent-written changes | Review time per PR; change failure rate; rework cycles; merged diff still matching plan.md |
| Test | Eval pass rate over time; time for an incident to become a permanent eval | Regressions caught in CI versus found in production |
| Deploy | Time to first review; share of review comments resolved without a human touching the branch; time waiting on each gate; pipeline failures triaged without paging | Defects and vulnerabilities caught before merge versus escaping; DORA measures from CI and deployment tooling |
| Maintain | Time from trigger to an intent.md in the triage queue | Share of findings that become merged fixes; repeat incidents of the same class |

Use these during `status`, `audit`, and `close` to describe where work stops moving. Items collecting right after a PR opens mean review is the bottleneck, not coding.
