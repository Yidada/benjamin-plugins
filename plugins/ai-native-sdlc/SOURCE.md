# Source and implementation boundary

Conceptual reference: [The AI-Native SDLC playbook](https://claude.com/blog/the-ai-native-sdlc-playbook), Louis Claxton, Anthropic, published August 21, 2026; consulted September 5, 2026 and re-aligned September 19, 2026.

The plugin follows the playbook's overall logic:

- Six non-linear stages that form a loop: Plan → Design → Build → Test → Deploy → Maintain, where Maintain writes a new intent that re-enters Plan.
- Every stage ends by committing an artifact the next stage reads: intent.md, spec.md, plan.md, the diff and its tests, evidence and review findings, the incident record. The commit chain is the audit trail.
- Human judgment sits at the gates: intent accepted, spec approved, plan accepted, PR merged by a code owner, release authorized. The agent goes to the production gate and never crosses it.
- Two layers of guardrails: skills and instructions are advisory; hooks, CI, branch protection and deployment permissions are deterministic.
- Plan mode before any code, a self-verifying feedback loop, continuous evals for the agent's configuration, severity-ranked review passes, a rehearsed rollback, and tiered incident response.
- Per-stage leading and lagging measures read from Git and CI history, never invented.

This plugin is an independent implementation for Benjamin's Codex environment. Its risk tiers (R0–R3), seven-skill packaging, CLI behavior, delivery scopes and validation rules are local design choices that scale how many artifacts and recorded decisions a change carries. Framework names are mapped to Codex: AGENTS.md is the repository memory, and hooks or CI on the actual platform are the deterministic layer.

The plugin has no official affiliation with Anthropic. It includes no copied article body, external MCP service, automatic deployment, global shell hook or continuous monitoring daemon. The recorded gates are local workflow records; enforce production authorization through the actual platform's controls.
