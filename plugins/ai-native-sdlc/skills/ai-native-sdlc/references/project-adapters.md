# Discover checks from the project

These are clues, not default commands. Prefer current AGENTS.md, checked-in wrappers, manifests and CI. In a monorepo target the changed package and its consumers. `sdlc.py inspect` lists manifest candidates without executing their content.

| Project | Look for | Relevant boundary checks |
|---|---|---|
| JS/TS and web | package.json, packageManager, workspace files, one matching lockfile | Existing lint/typecheck/test/build; changed browser flow and responsive layout |
| Python | pyproject.toml, uv.lock, requirements files, tox/nox | Existing test/lint targets; import/package checks and API integration |
| Go | go.mod, go.work, Makefile, CI | Package tests, affected consumers, concurrency checks when relevant |
| Rust | Cargo.toml, toolchain file, workspace | Existing cargo targets; feature combinations and FFI boundaries when changed |
| JVM / Android | Gradle/Maven wrappers, settings files | Module tests, API contracts, emulator/device behavior when applicable |
| iOS / macOS | xcodeproj, xcworkspace, Package.swift | Existing scheme build/tests, simulator or device evidence, accessibility |
| .NET | sln, csproj, global.json, Directory.Build.* | Existing solution/module build and tests, API or UI interaction |
| C/C++ / embedded | CMakePresets, CMakeLists, Makefile, board configuration | Host tests and cross-build; actual target/device observations remain separate |
| Infrastructure | Terraform/OpenTofu, Kubernetes, Docker, pipeline files | Validate/plan/render in the requested environment; production changes need scoped authority |

Do not assume internet, a package manager, credentials, Docker or device access. Report a missing capability precisely and finish checks that are possible. Generated files and existing dependency versions follow repository rules.
