---
name: sdlc-release
description: "Prepare or execute a requested software PR, release, deployment or rollback with bidirectional review, target-specific verification and a hard stop at the production gate. Use for software delivery requests."
---

# 发布与交付验证

## Scope

- Apply this skill to its named software task. Do not load `$ai-native-sdlc`, bootstrap `.sdlc`, or start other lifecycle stages unless the user explicitly invokes the coordinator.
- If the coordinator is already active, write results into the corresponding change artifacts and obey its current risk decisions. Otherwise return the requested result in the existing project format.
- Read applicable project instructions and preserve user scope and existing authorization. Use plain explanations with observable examples. Do not change global configuration as a side effect.

## Workflow

This is the Deploy play: review runs both ways, governance is enforced by the platform's gates, and the agent stops at the production gate.

1. Resolve the requested destination: local handoff, PR, staging or production. Confirm the repo, branch, artifact or commit, environment and provider from current evidence. Everything the agent writes reaches the default branch through a PR and branch protection; there is no direct path.
2. Inspect the final diff, required checks, release notes, configuration and migration impact, and rollback limits. Check the diff against the plan and spec, and run the review passes (bugs, security, compliance) before asking a human to look. Use the repository's current delivery mechanism.
3. Review is bidirectional. On the agent's own PR, address review comments and failing checks and push until the PR waits only on code owner approval. Never approve the code you wrote; the code owner decides the merge.
4. Reuse explicit session authorization. If the concrete external action or environment is outside its scope, finish preparation and request the missing decision immediately before execution. Autonomy is tiered by environment: development open, staging in between, production only with the release manager's authorization enforced by the platform's gate or hook.
5. Execute only the requested delivery, sandboxed with scoped short-lived credentials. Observe actual remote status and verify the deployed behavior when tools allow. Record URLs or IDs and any material unverified step.
6. For a failed release, diagnose within scope. Rollback is the rehearsed path: perform it only when authorized or covered by an approved runbook, and do not broaden access to solve a tooling limitation.
7. Report exactly what reached which destination. A PR, a build, a successful upload and a healthy running release are different completion levels.

Output: delivery target, artifact or commit, review and verification results, rollback readiness and remaining blocker. Creating a release plan alone does not prove release.
