# Build and Test

## Build: nothing is implemented without an accepted plan

### Plan mode first

1. Read intent.md and spec.md, the repository's package manager, lockfile, toolchain, build targets, and ownership boundaries. Verify available commands from project instructions, manifests, and CI; read [project-adapters.md](project-adapters.md) when the stack is unfamiliar. A manifest script is a candidate command; inspect its effects before executing it.
2. Write plan.md without editing code: the files that change, the order of work, the risks, and the proof. Interrogate it: what could this break, which step is most risky, what options were rejected? Iterate until an engineer who has never seen the conversation could implement the change from the plan alone.
3. The plan is accepted by the engineer (the user, or the recorded R3 plan gate). Then `transition --stage build`. When implementation departs from the plan, update plan.md in the same commit; the review pass later checks the diff against it.

### Repository memory and institutional knowledge

- `AGENTS.md` is the repository memory: conventions, commands with healthy output, architecture, and the mistakes seen most often. Keep it under a page; the agent reads all of it at session start. When the agent makes the same mistake twice, the correction goes into `AGENTS.md`.
- Knowledge that must be applied consistently (security standards, API conventions, brand rules) belongs in a skill, not in a prompt. A skill is advisory; a policy that must always hold needs a hook or CI check behind it.
- Build-time hooks run on file edits and shell commands: block edits to protected paths, run the formatter and linter after an edit, keep credentials out of the diff. Keep them fast and scoped to the changed file. Hooks that ask a human belong with the Deploy gates, not in Build.

### Implement

- Implement the smallest coherent slice in the accepted plan. Preserve unrelated changes. Avoid broad refactors or dependency upgrades unrelated to the task.
- For a bug, write the failing test first: reproduce the externally observable failure, run it, confirm it fails for the expected reason, then make it pass without editing the test.
- For UI work, close the loop against the approved mock: implement, screenshot or exercise the flow, compare, adjust. Two or three rounds is normal.
- Split independent file sets across parallel sessions only when the user authorizes it; each session takes its own worktree, and two or three sessions is a sensible start. Delegate recurring jobs to subagents named for their function (verifier, researcher, code simplifier), state why each was dispatched, and require an evidence-based report: what it ran, what it saw, what it did not check. Never claim independence from a second pass by the same agent.

### The feedback loop

Always give the agent a way to verify its own work before a person sees it.

- Prefer one command per check that exits non-zero on failure; list it in `AGENTS.md` with an example of healthy output.
- Make the target quantifiable: "all tests in test_status.py pass", "the endpoint returns 200 with the new field", "the screenshot matches the mock".
- Run checks that can falsify the success claim: unit, integration, contract, end-to-end, visual, performance, or device checks according to the changed boundary. Low-impact wording or formatting edits usually need a direct check rather than a new suite. Run all checks mandated by the repository.
- Record command, cwd, environment, exit code, observed behavior, and coverage gap in evidence.md. Preserve failed results and link the later successful rerun. Fixture success, simulator success, and production success are different evidence levels. If a final material change invalidates prior checks, rerun the affected checks.
- Verification is part of "done". Paste the output as evidence rather than asserting a result.

Measure Build by first-pass CI success for agent-written changes, review time per PR, change failure rate, rework cycles per change, and how often the merged diff still matches the committed plan.md.

## Test: continuous evals

QA is woven through implementation rather than a gate at a stage boundary. Two suites matter.

1. The product's own checks, run through the feedback loop above, with failures diagnosed from actual logs. Separate environment failures, flaky tests, and product defects with evidence. Never weaken assertions, skip failures, or edit tests during a fix task to obtain green output.
2. Evals for the agent's configuration. A change to `AGENTS.md`, a skill, a hook, a prompt, or the model steers the agent and deserves the regression testing that code gets. Build the suite from real tasks with expected outcomes (start with the ten most recent, grow toward twenty to fifty), run it on any configuration change and on a schedule when CI can run the agent non-interactively, gate the configuration change on the pass rate, and add an eval for every production incident. Include negative cases for scope, permissions, uncertainty, and failure handling. Human acceptance criteria remain final; do not over-rely on a model judge. A format validator alone cannot prove behavior.

The plugin's evals/scenarios.json is a reusable test specification for this plugin's own configuration, not an automatically scheduled evaluator.

For R2/R3 fill review.md with concrete findings and resolutions using the review passes in [deploy-maintain.md](deploy-maintain.md). A self-review must be identified as such.

Measure Test by eval pass rate over time, by how long a production incident takes to become a permanent eval, and by regressions caught in CI versus regressions found in production.
