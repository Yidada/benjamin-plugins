#!/usr/bin/env python3
"""Deterministic repository state helper for the AI-Native SDLC skill."""

from __future__ import annotations

import argparse
import hashlib
import json
import os
import re
import subprocess
import sys
import tempfile
import unicodedata
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


SCHEMA_VERSION = 1
RISKS = ("R0", "R1", "R2", "R3")
STAGES = ("plan", "design", "build", "test", "deploy", "maintain", "closed")
STATUSES = ("draft", "active", "blocked", "complete", "cancelled")
GATE_STATES = ("not_required", "pending", "approved", "rejected")
ACTIVE_STATUSES = {"draft", "active", "blocked"}
ARTIFACTS = {
    "R0": (),
    "R1": ("intent.md", "plan.md", "evidence.md"),
    "R2": (
        "intent.md",
        "spec.md",
        "plan.md",
        "evidence.md",
        "review.md",
        "decisions.md",
    ),
    "R3": (
        "intent.md",
        "spec.md",
        "plan.md",
        "evidence.md",
        "review.md",
        "decisions.md",
        "risk.md",
        "rollback.md",
        "approvals.md",
    ),
}
REQUIRED_MARKER = "<!-- REQUIRED:"
INTEGRATION_HEADING = "## AI-Native SDLC Integration"
INTEGRATION_BLOCK = """## AI-Native SDLC Integration

- Load `$ai-native-sdlc` only when the user explicitly invokes it.
- Keep lifecycle artifacts in `.sdlc/changes/<change-id>/` and commit them with the related code.
- Read `.sdlc/config.json` and the active change's `state.json` before advancing the workflow.
- Repository and closer `AGENTS.md` instructions own architecture, commands, style, and technical constraints. The plugin owns lifecycle stages, risk, gates, artifacts, and evidence.
"""


class SdlcError(RuntimeError):
    """Expected validation or usage error."""


def now_iso() -> str:
    return datetime.now(timezone.utc).isoformat(timespec="seconds").replace("+00:00", "Z")


def print_json(value: Any) -> None:
    print(json.dumps(value, ensure_ascii=False, indent=2))


def run_git(repo: Path, *args: str) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        ["git", "-C", str(repo), *args],
        check=False,
        capture_output=True,
        text=True,
    )


def resolve_repo(raw: str) -> Path:
    candidate = Path(raw).expanduser().resolve()
    if not candidate.is_dir():
        raise SdlcError(f"Repository path is not a directory: {candidate}")
    result = run_git(candidate, "rev-parse", "--show-toplevel")
    if result.returncode != 0:
        raise SdlcError(f"A Git repository is required: {candidate}")
    return Path(result.stdout.strip()).resolve()


def sdlc_is_ignored(repo: Path) -> bool:
    result = run_git(repo, "check-ignore", "--no-index", ".sdlc/config.json", ".sdlc/changes/probe/state.json", ".sdlc/changes/probe/intent.md")
    if result.returncode not in {0, 1}:
        raise SdlcError("Could not verify Git ignore rules for .sdlc.")
    return result.returncode == 0


def load_json(path: Path) -> dict[str, Any]:
    try:
        value = json.loads(path.read_text(encoding="utf-8"))
    except FileNotFoundError as exc:
        raise SdlcError(f"Missing file: {path}") from exc
    except json.JSONDecodeError as exc:
        raise SdlcError(f"Invalid JSON in {path}: {exc}") from exc
    if not isinstance(value, dict):
        raise SdlcError(f"Expected a JSON object in {path}")
    return value


def write_json(path: Path, value: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    content = json.dumps(value, ensure_ascii=False, indent=2) + "\n"
    with tempfile.NamedTemporaryFile(mode="w", encoding="utf-8", dir=path.parent, delete=False) as handle:
        temp_path = Path(handle.name)
        try:
            handle.write(content)
            handle.flush()
            os.fsync(handle.fileno())
        except BaseException:
            temp_path.unlink(missing_ok=True)
            raise
    try:
        os.replace(temp_path, path)
    finally:
        temp_path.unlink(missing_ok=True)


def config_template_path() -> Path:
    return Path(__file__).resolve().parent.parent / "assets" / "templates" / "config.json"


def load_config_template() -> dict[str, Any]:
    return load_json(config_template_path())


def config_path(repo: Path) -> Path:
    return safe_path(repo, ".sdlc/config.json")


def changes_path(repo: Path) -> Path:
    return safe_path(repo, ".sdlc/changes")


def safe_path(repo: Path, relative: str) -> Path:
    path = repo / relative
    try:
        path.resolve().relative_to(repo.resolve())
    except ValueError as exc:
        raise SdlcError(f"Path escapes the repository: {relative}") from exc
    current = path
    while current != repo:
        if current.is_symlink():
            raise SdlcError(f"SDLC paths must not be symlinks: {relative}")
        current = current.parent
    return path


def check_id(change_id: str) -> None:
    if not isinstance(change_id, str) or not re.fullmatch(r"[\w-]{1,100}", change_id, flags=re.UNICODE):
        raise SdlcError("Invalid change ID: use a single directory name with letters, digits or hyphens.")


def require_bootstrap(repo: Path) -> dict[str, Any]:
    path = config_path(repo)
    if not path.exists():
        raise SdlcError("Repository is not bootstrapped. Run `bootstrap` first.")
    config = load_json(path)
    if config.get("schema_version") != SCHEMA_VERSION:
        raise SdlcError(f"Unsupported config schema in {path}")
    return config


def slugify(title: str) -> str:
    value = unicodedata.normalize("NFKC", title).strip().lower()
    value = re.sub(r"[^\w]+", "-", value, flags=re.UNICODE)
    value = value.replace("_", "-").strip("-")
    value = re.sub(r"-{2,}", "-", value)
    return (value or "change")[:60].rstrip("-")


def new_change_id(repo: Path, title: str) -> str:
    prefix = datetime.now().astimezone().strftime("%Y%m%d")
    base = f"{prefix}-{slugify(title)}"
    candidate = base
    suffix = 2
    while (changes_path(repo) / candidate).exists():
        candidate = f"{base}-{suffix:02d}"
        suffix += 1
    return candidate


def render_template(name: str, values: dict[str, str]) -> str:
    path = Path(__file__).resolve().parent.parent / "assets" / "templates" / name
    if not path.exists():
        raise SdlcError(f"Plugin template is missing: {path}")
    content = path.read_text(encoding="utf-8")
    for key, value in values.items():
        content = content.replace("{{" + key + "}}", value)
    return content


def state_path(repo: Path, change_id: str) -> Path:
    check_id(change_id)
    return safe_path(repo, f".sdlc/changes/{change_id}/state.json")


def load_state(repo: Path, change_id: str) -> dict[str, Any]:
    state = load_json(state_path(repo, change_id))
    if state.get("change_id") != change_id:
        raise SdlcError(f"State change_id does not match directory: {change_id}")
    return state


def save_state(repo: Path, state: dict[str, Any]) -> None:
    state["updated_at"] = now_iso()
    write_json(state_path(repo, str(state["change_id"])), state)


def list_states(repo: Path) -> list[dict[str, Any]]:
    root = changes_path(repo)
    if not root.exists():
        return []
    states: list[dict[str, Any]] = []
    for path in sorted(root.glob("*/state.json")):
        try:
            states.append(load_state(repo, path.parent.name))
        except SdlcError as exc:
            states.append({"change_id": path.parent.name, "load_error": str(exc)})
    return states


def resolve_change(repo: Path, requested: str | None) -> dict[str, Any]:
    if requested:
        return load_state(repo, requested)
    active = [state for state in list_states(repo) if state.get("status") in ACTIVE_STATUSES]
    if not active:
        raise SdlcError("No active change. Pass --change-id to inspect a completed change.")
    if len(active) > 1:
        ids = ", ".join(str(state.get("change_id")) for state in active)
        raise SdlcError(f"Multiple active changes require an explicit --change-id: {ids}")
    return active[0]


def validate_state_shape(state: dict[str, Any]) -> list[str]:
    issues: list[str] = []
    try:
        check_id(state.get("change_id"))
    except SdlcError as exc:
        issues.append(str(exc))
    required_keys = {
        "schema_version",
        "change_id",
        "title",
        "risk",
        "current_stage",
        "status",
        "required_artifacts",
        "gates",
        "created_at",
        "updated_at",
    }
    for key in sorted(required_keys - state.keys()):
        issues.append(f"state.json missing field: {key}")
    if state.get("schema_version") != SCHEMA_VERSION:
        issues.append(f"state.json schema_version must be {SCHEMA_VERSION}")
    risk = state.get("risk")
    if risk not in RISKS:
        issues.append(f"state.json risk must be one of {', '.join(RISKS)}")
    if state.get("current_stage") not in STAGES:
        issues.append(f"state.json current_stage must be one of {', '.join(STAGES)}")
    if state.get("status") not in STATUSES:
        issues.append(f"state.json status must be one of {', '.join(STATUSES)}")
    if state.get("delivery", "production") not in ("local", "pr", "production"):
        issues.append("delivery must be local, pr or production")
    if (state.get("status") == "complete") != (state.get("current_stage") == "closed"):
        issues.append("complete status and closed stage must occur together")
    if "approval_records" in state and not isinstance(state["approval_records"], dict):
        issues.append("approval_records must be an object")
    artifacts = state.get("required_artifacts")
    expected = list(ARTIFACTS.get(str(risk), ()))
    if artifacts != expected:
        issues.append(f"required_artifacts must equal the {risk} contract: {expected}")
    gates = state.get("gates")
    if not isinstance(gates, dict):
        issues.append("state.json gates must be an object")
    else:
        if set(gates) != {"spec", "plan", "production"}:
            issues.append("gates must contain exactly: spec, plan, production")
        for gate, value in gates.items():
            if value not in GATE_STATES:
                issues.append(f"gate {gate} has invalid state: {value}")
        expected_default = "pending" if risk == "R3" else "not_required"
        if risk != "R3" and any(value != expected_default for value in gates.values()):
            issues.append("R0-R2 gates must remain not_required")
        if risk == "R3":
            required = ("spec", "plan", "production") if state.get("delivery", "production") == "production" else ("spec", "plan")
            for gate in required:
                if gates.get(gate) == "not_required":
                    issues.append(f"R3 {gate} gate cannot be not_required")
            if "production" not in required and gates.get("production") != "not_required":
                issues.append("Non-production delivery requires production gate not_required")
    return issues


def artifact_issues(repo: Path, state: dict[str, Any], for_close: bool) -> list[str]:
    issues: list[str] = []
    change_dir = changes_path(repo) / str(state.get("change_id"))
    for name in state.get("required_artifacts", []):
        path = safe_path(repo, f".sdlc/changes/{state['change_id']}/{name}")
        if run_git(repo, "check-ignore", "--no-index", "-q", str(path.relative_to(repo))).returncode == 0:
            issues.append(f"artifact is excluded by Git ignore rules: {name}")
        if not path.is_file():
            issues.append(f"missing artifact: {name}")
            continue
        content = path.read_text(encoding="utf-8")
        if not content.strip():
            issues.append(f"empty artifact: {name}")
        if REQUIRED_MARKER in content:
            issues.append(f"incomplete artifact: {name} contains REQUIRED markers")
    if for_close:
        evidence = change_dir / "evidence.md"
        if evidence.is_file():
            content = evidence.read_text(encoding="utf-8")
            if not re.search(r"(?im)^- Outcome:\s*pass\s*$", content):
                issues.append("evidence.md must contain `- Outcome: pass`")
        if state.get("risk") in {"R2", "R3"}:
            review = change_dir / "review.md"
            if review.is_file():
                content = review.read_text(encoding="utf-8")
                if not re.search(r"(?im)^- Verdict:\s*approved\s*$", content):
                    issues.append("review.md must contain `- Verdict: approved`")
        if state.get("risk") == "R3":
            gates = state.get("gates", {})
            for gate in ("spec", "plan", "production"):
                if gate == "production" and state.get("delivery", "production") != "production":
                    continue
                if gates.get(gate) != "approved":
                    issues.append(f"R3 gate is not approved: {gate}")
    return issues


def validate_change(repo: Path, state: dict[str, Any], for_close: bool = False) -> list[str]:
    shape = validate_state_shape(state)
    if shape:
        return shape
    issues = artifact_issues(repo, state, for_close)
    if state.get("risk") == "R3" and "approval_records" in state:
        for gate, decision in state["gates"].items():
            if decision != "approved":
                continue
            record = state["approval_records"].get(gate)
            if not isinstance(record, dict) or record.get("fingerprint") != gate_fingerprint(repo, state, gate):
                issues.append(f"R3 approval is missing or stale: {gate}")
    return issues


def next_action(state: dict[str, Any], issues: list[str]) -> str:
    if state.get("status") in {"complete", "cancelled"}:
        return "Read historical evidence; start a linked follow-up for new work."
    stage = str(state.get("current_stage"))
    relevant = {"plan": ("intent.md", "plan.md"), "design": ("spec.md", "plan.md", "risk.md", "rollback.md"), "build": ("plan.md",), "test": ("evidence.md", "review.md", "decisions.md"), "deploy": (), "maintain": ()}.get(stage, ())
    for issue in issues:
        if not issue.startswith(("incomplete artifact:", "missing artifact:", "empty artifact:")) or any(name in issue for name in relevant) or stage in {"deploy", "maintain"}:
            return f"Resolve: {issue}"
    if state.get("risk") == "R3":
        gates = state.get("gates", {})
        stage = state.get("current_stage")
        if stage == "design" and gates.get("spec") == "pending":
            return "Complete spec.md and request explicit spec gate approval."
        if stage == "design" and gates.get("plan") == "pending":
            return "Complete plan.md and request explicit plan gate approval before implementation."
        if stage == "deploy" and gates.get("production") == "pending":
            return "Request explicit production gate approval before release."
    stage = str(state.get("current_stage"))
    if stage == "maintain":
        return "Run close validation, then close the change."
    return f"Advance the {stage} stage using its reference and record evidence."


def command_bootstrap(args: argparse.Namespace) -> int:
    repo = resolve_repo(args.repo)
    if sdlc_is_ignored(repo):
        raise SdlcError(".sdlc is excluded by .gitignore. Remove that rule before bootstrap.")
    changed: list[str] = []
    agents = safe_path(repo, "AGENTS.md")
    existing_agents = agents.read_text(encoding="utf-8") if agents.exists() else ""
    count = existing_agents.count(INTEGRATION_HEADING)
    if count > 1:
        raise SdlcError("AGENTS.md contains duplicate AI-Native SDLC Integration sections.")
    changes_path(repo)
    config = config_path(repo)
    if config.exists():
        existing = load_json(config)
        if existing.get("schema_version") != SCHEMA_VERSION:
            raise SdlcError(f"Unsupported existing config schema in {config}")
    else:
        write_json(config, load_config_template())
        changed.append(str(config.relative_to(repo)))
    changes_path(repo).mkdir(parents=True, exist_ok=True)

    if count == 0:
        prefix = existing_agents.rstrip()
        updated = f"{prefix}\n\n{INTEGRATION_BLOCK}" if prefix else INTEGRATION_BLOCK
        agents.write_text(updated, encoding="utf-8")
        changed.append("AGENTS.md")
    print_json(
        {
            "repository": str(repo),
            "status": "bootstrapped",
            "changed": changed,
            "idempotent": not changed,
            "claude_md_modified": False,
        }
    )
    return 0


def command_start(args: argparse.Namespace) -> int:
    repo = resolve_repo(args.repo)
    if args.risk == "R0":
        print_json(
            {
                "repository": str(repo),
                "title": args.title,
                "risk": "R0",
                "persistent_change_created": False,
                "next_action": "Complete the requested read-only explanation, inspection, research, or audit.",
            }
        )
        return 0

    require_bootstrap(repo)
    if sdlc_is_ignored(repo):
        raise SdlcError(".sdlc is excluded by .gitignore.")
    if not args.title.strip():
        raise SdlcError("Title must not be blank.")
    if args.delivery == "production" and args.risk != "R3":
        raise SdlcError("Production delivery requires R3 risk.")
    if args.parent_change_id:
        load_state(repo, args.parent_change_id)

    change_id = new_change_id(repo, args.title)
    created_at = now_iso()
    required = list(ARTIFACTS[args.risk])
    ignored = run_git(repo, "check-ignore", "--no-index", *[f".sdlc/changes/{change_id}/{name}" for name in ("state.json", *required)])
    if ignored.returncode == 0:
        raise SdlcError("Change artifacts are excluded by Git ignore rules.")
    if ignored.returncode != 1:
        raise SdlcError("Could not verify Git ignore rules for this change.")
    gates = {
        "spec": "pending" if args.risk == "R3" else "not_required",
        "plan": "pending" if args.risk == "R3" else "not_required",
        "production": "pending" if args.risk == "R3" and args.delivery == "production" else "not_required",
    }
    state: dict[str, Any] = {
        "schema_version": SCHEMA_VERSION,
        "change_id": change_id,
        "title": args.title,
        "risk": args.risk,
        "current_stage": "plan",
        "status": "active",
        "required_artifacts": required,
        "gates": gates,
        "created_at": created_at,
        "updated_at": created_at,
        "delivery": args.delivery,
        "approval_records": {},
    }
    if args.risk_justification:
        state["risk_justification"] = args.risk_justification
    if args.parent_change_id:
        state["parent_change_id"] = args.parent_change_id
    if args.trigger:
        state["trigger"] = args.trigger

    change_dir = changes_path(repo) / change_id
    change_dir.mkdir(parents=True)
    write_json(change_dir / "state.json", state)
    values = {
        "CHANGE_ID": change_id,
        "TITLE": args.title,
        "RISK": args.risk,
        "CREATED_AT": created_at,
    }
    for name in required:
        (change_dir / name).write_text(render_template(name, values), encoding="utf-8")
    print_json(
        {
            "repository": str(repo),
            "change_id": change_id,
            "risk": args.risk,
            "current_stage": "plan",
            "created": ["state.json", *required],
            "next_action": "Fill intent.md with the steelmanned goal and verified repository context.",
        }
    )
    return 0


def command_inspect(args: argparse.Namespace) -> int:
    repo = resolve_repo(args.repo)
    result = run_git(repo, "ls-files", "--cached", "--others", "--exclude-standard", "-z")
    if result.returncode:
        raise SdlcError("Could not enumerate repository files.")
    exact = {"AGENTS.md", "package.json", "pnpm-lock.yaml", "pnpm-workspace.yaml", "yarn.lock", "package-lock.json", "bun.lock", "bun.lockb", "pyproject.toml", "uv.lock", "go.mod", "go.work", "Cargo.toml", "Cargo.lock", "Package.swift", "Podfile", "build.gradle", "build.gradle.kts", "settings.gradle", "settings.gradle.kts", "pom.xml", "gradlew", "mvnw", "Makefile", "justfile", "CMakeLists.txt", "CMakePresets.json", "global.json", "Dockerfile", "compose.yaml"}
    suffixes = (".csproj", ".sln", ".tf", ".xcodeproj/project.pbxproj", ".xcworkspace/contents.xcworkspacedata")
    found = []
    for filename in sorted(set(result.stdout.split("\0")) - {""}):
        if len(found) == 500:
            break
        parts = Path(filename).parts
        if any(part in {"node_modules", "vendor", ".venv", "target", "build", ".git", ".sdlc"} for part in parts):
            continue
        if Path(filename).name in exact or filename.endswith(suffixes) or filename.startswith(".github/workflows/"):
            found.append(filename)
    status = run_git(repo, "status", "--short").stdout
    print_json({"repository": str(repo), "read_only": True, "candidates": found, "candidate_limit": 500, "git_status": status, "commands_executed_from_project": False, "next_action": "Read relevant instructions, manifests and CI; select commands for the changed package. Candidate files do not authorize execution."})
    return 0


def status_payload(repo: Path, state: dict[str, Any]) -> dict[str, Any]:
    issues = validate_change(repo, state, for_close=False)
    return {
        "repository": str(repo),
        "change_id": state.get("change_id"),
        "title": state.get("title"),
        "risk": state.get("risk"),
        "current_stage": state.get("current_stage"),
        "status": state.get("status"),
        "gates": state.get("gates"),
        "issues": issues,
        "next_action": next_action(state, issues),
    }


def command_status(args: argparse.Namespace) -> int:
    repo = resolve_repo(args.repo)
    require_bootstrap(repo)
    state = resolve_change(repo, args.change_id)
    print_json(status_payload(repo, state))
    return 0


def command_validate(args: argparse.Namespace) -> int:
    repo = resolve_repo(args.repo)
    require_bootstrap(repo)
    state = resolve_change(repo, args.change_id)
    issues = validate_change(repo, state, for_close=args.for_close)
    print_json(
        {
            "repository": str(repo),
            "change_id": state.get("change_id"),
            "valid": not issues,
            "for_close": args.for_close,
            "issues": issues,
        }
    )
    return 0 if not issues else 1


def append_approval(repo: Path, state: dict[str, Any], gate: str, gate_status: str, approver: str, note: str) -> None:
    path = changes_path(repo) / str(state["change_id"]) / "approvals.md"
    if not path.exists():
        raise SdlcError("approvals.md is required before recording an R3 approval.")
    safe_note = note.replace("|", "\\|").replace("\n", " ").strip()
    safe_approver = approver.replace("|", "\\|").replace("\n", " ").strip()
    line = f"| {gate} | {gate_status} | {safe_approver} | {now_iso()} | {safe_note} |\n"
    with path.open("a", encoding="utf-8") as handle:
        handle.write(line)


def allowed_next_stage(risk: str, current: str) -> str | None:
    route = (
        ("plan", "build", "test", "deploy", "maintain", "closed")
        if risk == "R1"
        else ("plan", "design", "build", "test", "deploy", "maintain", "closed")
    )
    if current not in route:
        return None
    index = route.index(current)
    return route[index + 1] if index + 1 < len(route) else None


def enforce_transition_gate(state: dict[str, Any], target: str) -> None:
    if state.get("risk") != "R3":
        return
    gates = state.get("gates", {})
    required_gates = ("spec", "plan") if target in {"build", "test", "deploy", "maintain"} else ()
    if target == "maintain" and state.get("delivery", "production") == "production":
        required_gates += ("production",)
    for gate in required_gates:
        if gates.get(gate) != "approved":
            raise SdlcError(f"R3 transition to {target} requires approved {gate} gate.")


def gate_fingerprint(repo: Path, state: dict[str, Any], gate: str) -> str:
    names = {"spec": ("spec.md",), "plan": ("spec.md", "plan.md", "risk.md", "rollback.md"), "production": ("spec.md", "plan.md", "risk.md", "rollback.md", "evidence.md", "review.md")}[gate]
    digest = hashlib.sha256()
    digest.update(str(state.get("delivery", "production")).encode())
    for name in names:
        path = safe_path(repo, f".sdlc/changes/{state['change_id']}/{name}")
        digest.update(name.encode())
        digest.update(path.read_bytes() if path.is_file() else b"<missing>")
    if gate == "production":
        digest.update(run_git(repo, "rev-parse", "HEAD").stdout.encode())
        result = run_git(repo, "ls-files", "--cached", "--others", "--exclude-standard", "-z")
        if result.returncode:
            raise SdlcError("Could not fingerprint the release worktree.")
        for filename in sorted(set(result.stdout.split("\0")) - {""}):
            if filename.startswith(".sdlc/"):
                continue
            path = repo / filename
            digest.update(filename.encode())
            if path.is_symlink():
                digest.update(os.readlink(path).encode())
            elif path.is_file():
                with path.open("rb") as handle:
                    for chunk in iter(lambda: handle.read(1024 * 1024), b""):
                        digest.update(chunk)
            else:
                digest.update(b"<missing-or-submodule>")
    return digest.hexdigest()


def require_filled(repo: Path, state: dict[str, Any], names: tuple[str, ...]) -> None:
    for name in names:
        path = safe_path(repo, f".sdlc/changes/{state['change_id']}/{name}")
        if not path.is_file():
            raise SdlcError(f"missing artifact: {name}")
        content = path.read_text(encoding="utf-8")
        if not content.strip() or REQUIRED_MARKER in content:
            raise SdlcError(f"incomplete artifact: {name}")


def enforce_stage_artifacts(repo: Path, state: dict[str, Any], target: str) -> None:
    if target == "design":
        require_filled(repo, state, ("intent.md",))
    if target == "build":
        names = ("intent.md", "plan.md")
        if state["risk"] in {"R2", "R3"}:
            names += ("spec.md",)
        if state["risk"] == "R3":
            names += ("risk.md", "rollback.md")
        require_filled(repo, state, names)
    if target == "deploy":
        issues = artifact_issues(repo, state, for_close=True)
        issues = [issue for issue in issues if issue != "R3 gate is not approved: production"]
        if issues:
            raise SdlcError(issues[0])
    if target in {"build", "test", "deploy", "maintain"} and state["risk"] == "R3" and "approval_records" in state:
        for gate, record in state["approval_records"].items():
            if state["gates"].get(gate) != "approved":
                continue
            if not isinstance(record, dict) or record.get("fingerprint") != gate_fingerprint(repo, state, gate):
                raise SdlcError(f"R3 approval is missing or stale: {gate}")
        for gate in ("spec", "plan"):
            if state["gates"].get(gate) == "approved" and gate not in state["approval_records"]:
                raise SdlcError(f"R3 approval is missing or stale: {gate}")
        if target == "maintain" and state.get("delivery") == "production" and "production" not in state["approval_records"]:
            raise SdlcError("R3 approval is missing or stale: production")


def command_transition(args: argparse.Namespace) -> int:
    repo = resolve_repo(args.repo)
    require_bootstrap(repo)
    state = resolve_change(repo, args.change_id)
    issues = validate_state_shape(state)
    if issues:
        raise SdlcError(issues[0])
    if state["status"] in {"complete", "cancelled"}:
        raise SdlcError("Terminal changes cannot be reopened; start a linked follow-up change.")
    changed: list[str] = []
    approval = None

    if args.approve_gate:
        if state.get("risk") != "R3":
            raise SdlcError("Only R3 changes use approval gates.")
        gates = state.get("gates", {})
        if gates.get(args.approve_gate) == "not_required":
            raise SdlcError("This gate is not applicable to the selected delivery scope.")
        if not args.approver or not args.approver.strip() or not args.note or not args.note.strip():
            raise SdlcError("Recording a gate requires --approver and --note with actual authorization source and scope.")
        if args.approve_gate == "production" and state["current_stage"] != "deploy":
            raise SdlcError("Record production approval in the deploy stage for the prepared release.")
        if args.gate_status == "approved":
            names = {"spec": ("spec.md",), "plan": ("spec.md", "plan.md", "risk.md", "rollback.md"), "production": tuple(state["required_artifacts"])}[args.approve_gate]
            require_filled(repo, state, names)
        gates[args.approve_gate] = args.gate_status
        state["gates"] = gates
        state.setdefault("approval_records", {})[args.approve_gate] = {
            "actor": args.approver, "note": args.note, "recorded_at": now_iso(),
            "fingerprint": gate_fingerprint(repo, state, args.approve_gate),
        }
        approval = (args.approve_gate, args.gate_status, args.approver, args.note)
        state["status"] = "blocked" if args.gate_status == "rejected" else "active"
        changed.append(f"gate:{args.approve_gate}={args.gate_status}")

    if args.stage:
        if args.stage == "closed":
            raise SdlcError("Use the `close` command to enter the closed stage.")
        current = str(state.get("current_stage"))
        if args.stage != current:
            if state["status"] == "blocked":
                raise SdlcError("Resolve the blocker and explicitly set --status active before advancing.")
            expected = allowed_next_stage(str(state.get("risk")), current)
            if args.stage != expected:
                raise SdlcError(f"Invalid stage transition {current} -> {args.stage}; expected {expected}")
            enforce_transition_gate(state, args.stage)
            enforce_stage_artifacts(repo, state, args.stage)
            state["current_stage"] = args.stage
            changed.append(f"stage:{current}->{args.stage}")

    if args.status:
        state["status"] = args.status
        changed.append(f"status:{args.status}")
    if not changed:
        raise SdlcError("transition requires --stage, --approve-gate, or --status.")
    if approval:
        safe_path(repo, f".sdlc/changes/{state['change_id']}/approvals.md")
        append_approval(repo, state, *approval)
    save_state(repo, state)
    print_json({**status_payload(repo, state), "changed": changed})
    return 0


def command_close(args: argparse.Namespace) -> int:
    repo = resolve_repo(args.repo)
    require_bootstrap(repo)
    state = resolve_change(repo, args.change_id)
    if state.get("status") not in {"active", "draft"}:
        raise SdlcError("Only an active change can close; resolve any blocker first.")
    if state.get("current_stage") != "maintain":
        raise SdlcError("A change can close only from the maintain stage.")
    issues = validate_change(repo, state, for_close=True)
    if issues:
        print_json(
            {
                "repository": str(repo),
                "change_id": state.get("change_id"),
                "closed": False,
                "issues": issues,
            }
        )
        return 1
    state["current_stage"] = "closed"
    state["status"] = "complete"
    state["closed_at"] = now_iso()
    save_state(repo, state)
    print_json(
        {
            "repository": str(repo),
            "change_id": state.get("change_id"),
            "closed": True,
            "current_stage": "closed",
            "status": "complete",
        }
    )
    return 0


def command_audit(args: argparse.Namespace) -> int:
    repo = resolve_repo(args.repo)
    issues: list[str] = []
    if sdlc_is_ignored(repo):
        issues.append(".sdlc is excluded by .gitignore")
    config = config_path(repo)
    if not config.exists():
        issues.append("missing .sdlc/config.json")
    else:
        try:
            value = load_json(config)
            if value.get("schema_version") != SCHEMA_VERSION:
                issues.append("unsupported .sdlc/config.json schema_version")
        except SdlcError as exc:
            issues.append(str(exc))
    agents = safe_path(repo, "AGENTS.md")
    if not agents.exists():
        issues.append("missing root AGENTS.md")
    else:
        count = agents.read_text(encoding="utf-8").count(INTEGRATION_HEADING)
        if count != 1:
            issues.append(f"expected one AI-Native SDLC Integration section; found {count}")
    changes: list[dict[str, Any]] = []
    for state in list_states(repo):
        if state.get("load_error"):
            state_issues = [str(state["load_error"])]
        else:
            state_issues = validate_change(repo, state, for_close=state.get("status") == "complete")
        changes.append(
            {
                "change_id": state.get("change_id"),
                "status": state.get("status"),
                "issues": state_issues,
            }
        )
        issues.extend(f"{state.get('change_id')}: {issue}" for issue in state_issues)
    print_json(
        {
            "repository": str(repo),
            "read_only": True,
            "valid": not issues,
            "issues": issues,
            "changes": changes,
        }
    )
    return 0 if not issues else 1


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--repo", default=".", help="Path inside the target Git repository")
    subparsers = parser.add_subparsers(dest="command", required=True)

    inspect = subparsers.add_parser("inspect", help="Read-only project manifest and instruction discovery")
    inspect.set_defaults(func=command_inspect)

    bootstrap = subparsers.add_parser("bootstrap", help="Initialize .sdlc and root AGENTS.md integration")
    bootstrap.set_defaults(func=command_bootstrap)

    start = subparsers.add_parser("start", help="Create a risk-tiered change")
    start.add_argument("--title", required=True, help="Steelmanned change goal or title")
    start.add_argument("--risk", required=True, choices=RISKS)
    start.add_argument("--delivery", choices=("local", "pr", "production"), default="local")
    start.add_argument("--risk-justification")
    start.add_argument("--parent-change-id")
    start.add_argument("--trigger")
    start.set_defaults(func=command_start)

    status = subparsers.add_parser("status", help="Read current change state")
    status.add_argument("--change-id")
    status.set_defaults(func=command_status)

    validate = subparsers.add_parser("validate", help="Validate state and required artifacts")
    validate.add_argument("--change-id")
    validate.add_argument("--for-close", action="store_true")
    validate.set_defaults(func=command_validate)

    transition = subparsers.add_parser("transition", help="Advance one stage or record an R3 gate decision")
    transition.add_argument("--change-id")
    transition.add_argument("--stage", choices=STAGES)
    transition.add_argument("--status", choices=("active", "blocked", "cancelled"))
    transition.add_argument("--approve-gate", choices=("spec", "plan", "production"))
    transition.add_argument("--gate-status", choices=("approved", "rejected"), default="approved")
    transition.add_argument("--approver")
    transition.add_argument("--note")
    transition.set_defaults(func=command_transition)

    close = subparsers.add_parser("close", help="Validate and mark a maintain-stage change complete")
    close.add_argument("--change-id")
    close.set_defaults(func=command_close)

    audit = subparsers.add_parser("audit", help="Read-only repository SDLC audit")
    audit.set_defaults(func=command_audit)
    return parser


def main(argv: list[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)
    try:
        return int(args.func(args))
    except (SdlcError, OSError, UnicodeError) as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
