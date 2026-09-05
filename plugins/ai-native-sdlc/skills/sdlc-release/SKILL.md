---
name: sdlc-release
description: "Prepare or execute a requested software PR, release, deployment or rollback with target-specific verification. Use for software delivery requests."
---

# 发布与交付验证

## Scope

- Apply this skill to its named software task. Do not load `$ai-native-sdlc`, bootstrap `.sdlc`, or start other lifecycle stages unless the user explicitly invokes the coordinator.
- If the coordinator is already active, write results into the corresponding change artifacts and obey its current risk decisions. Otherwise return the requested result in the existing project format.
- Read applicable project instructions and preserve user scope and existing authorization. Use plain explanations with observable examples. Do not change global configuration as a side effect.

## Workflow


1. Resolve the requested destination: local handoff, PR, staging or production. Confirm the repo, branch, artifact/commit, environment and provider from current evidence.
2. Inspect final diff, required checks, release notes, configuration/migration impact and rollback limits. Use the repository's current delivery mechanism.
3. Reuse explicit session authorization. If the concrete external action or environment is outside its scope, finish preparation and request the missing decision immediately before execution.
4. Execute only the requested delivery. Observe actual remote status and verify the deployed behavior when tools allow. Record URLs/IDs and any material unverified step.
5. For a failed release, diagnose within scope. Perform rollback only when authorized or covered by an existing approved runbook. Do not broaden access to solve a tooling limitation.
6. Report exactly what reached which destination. A PR, build, successful upload and healthy running release are different completion levels.

Output: delivery target, artifact/commit, verification, rollback readiness and remaining blocker. Creating a release plan alone does not prove release.
