# Build and Test

Use the repository's package manager, lockfile, toolchain, build targets and ownership boundaries. Verify available commands from project instructions, manifests and CI. Read project-adapters.md when the stack is unfamiliar. A manifest script is a candidate command; inspect its effects before executing it.

Implement the smallest coherent slice in the approved plan. Preserve unrelated changes. For a bug, reproduce the externally observable failure when feasible, then verify the fix at the same boundary. For user interface work, exercise the actual changed flow when tools permit. Avoid broad refactors or dependency upgrades unrelated to the task.

Run checks that can falsify the success claim. Choose unit, integration, contract, end-to-end, visual, performance or device checks according to the changed boundary. Low-impact wording or formatting edits usually need a direct check rather than a new test suite. Run all checks mandated by the repository.

Record command, cwd, environment, exit code, observed behavior and coverage gap. Preserve failed results and link the later successful rerun. Fixture success, simulator success and production success are different evidence levels. If a final material code change invalidates prior checks, rerun the affected checks.

Review final diff and modified expectations. For R2/R3 fill review.md with concrete findings and resolutions. A self-review must be identified as such. Use subagents only when delegation is authorized; never claim independence from a second pass by the same agent.

For model, prompt, skill or tool-policy changes, run representative behavioral eval cases. Include negative authorization cases and preserve the original expected behavior when repairing a regression. The plugin's evals/scenarios.json contains reusable cases; it is a test specification, not an automatically scheduled model evaluator.
