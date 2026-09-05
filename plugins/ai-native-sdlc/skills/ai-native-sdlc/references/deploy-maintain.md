# Delivery and maintenance

Resolve the requested delivery level: local verified change, PR, staging, or production. The helper represents staging preparation as local unless production is explicitly in scope. Do not promote an artifact beyond the requested level.

Before an external action, identify the target, artifact/commit, validation result, rollback limits and existing authorization. Reuse session authorization covering the action. If a required decision is missing, finish preparation and show the concrete result for approval.

For production, enforce the organization's deployment permissions and review controls. Record actual CI, release and runtime observations. A successful build or created pipeline does not establish a successful deployment. Do not install global hooks, change branch protection or add a hosting provider merely because the plugin exists.

Maintain can mean a small handoff describing relevant signals, owner/role, rollback trigger and a follow-up condition. It does not require starting a service or scheduler. Set up monitors, periodic jobs or notifications only when the user requests them and the needed scope is available. Keep unchanged, non-actionable runs quiet.

For an incident, preserve the timeline and raw evidence, rank hypotheses, define the smallest diagnostic step, and separate containment from the final correction. In read-only mode produce a diagnosis. When a fix is authorized, create a new linked change and add a regression check when useful.

Close local delivery after the requested local work and evidence are complete. Use a production gate only for production-scoped R3 changes. Name unresolved external validation, avoid invented owners or baselines, and keep historical records intact.
