#!/usr/bin/env python3
"""End-to-end tests for sdlc.py using isolated temporary Git repositories."""

from __future__ import annotations

import hashlib
import json
import subprocess
import tempfile
import unittest
from pathlib import Path


SCRIPT = Path(__file__).resolve().with_name("sdlc.py")
ARTIFACTS = {
    "R1": {"intent.md", "plan.md", "evidence.md"},
    "R2": {"intent.md", "spec.md", "plan.md", "evidence.md", "review.md", "decisions.md"},
    "R3": {
        "intent.md",
        "spec.md",
        "plan.md",
        "evidence.md",
        "review.md",
        "decisions.md",
        "risk.md",
        "rollback.md",
        "approvals.md",
    },
}


class SdlcCliTests(unittest.TestCase):
    def setUp(self) -> None:
        self.temp = tempfile.TemporaryDirectory()
        self.repo = Path(self.temp.name) / "repo"
        self.repo.mkdir()
        self.git("init", "-q", "-b", "main")
        self.git("config", "user.name", "SDLC Test")
        self.git("config", "user.email", "sdlc-test@example.invalid")

    def tearDown(self) -> None:
        self.temp.cleanup()

    def git(self, *args: str) -> subprocess.CompletedProcess[str]:
        return subprocess.run(
            ["git", "-C", str(self.repo), *args],
            check=True,
            capture_output=True,
            text=True,
        )

    def run_cli(self, *args: str, expected: int = 0) -> subprocess.CompletedProcess[str]:
        result = subprocess.run(
            ["python3", str(SCRIPT), "--repo", str(self.repo), *args],
            check=False,
            capture_output=True,
            text=True,
        )
        self.assertEqual(
            expected,
            result.returncode,
            msg=f"stdout:\n{result.stdout}\nstderr:\n{result.stderr}",
        )
        return result

    def bootstrap(self) -> None:
        self.run_cli("bootstrap")

    def start(self, risk: str, title: str = "Add Raycast command", delivery: str = "local") -> str:
        result = self.run_cli("start", "--title", title, "--risk", risk, "--delivery", delivery)
        return str(json.loads(result.stdout)["change_id"])

    def state(self, change_id: str) -> dict[str, object]:
        return json.loads((self.repo / ".sdlc" / "changes" / change_id / "state.json").read_text())

    def complete_artifacts(self, change_id: str, evidence: str = "pass", review: str = "approved") -> None:
        change_dir = self.repo / ".sdlc" / "changes" / change_id
        state = self.state(change_id)
        for name in state["required_artifacts"]:
            path = change_dir / str(name)
            lines = path.read_text().splitlines()
            lines = [
                "Verified repository-specific content."
                if line.strip().startswith("<!-- REQUIRED:")
                else line
                for line in lines
            ]
            content = "\n".join(lines) + "\n"
            if name == "evidence.md":
                content = content.replace("- Outcome: pending", f"- Outcome: {evidence}")
            if name == "review.md":
                content = content.replace("- Verdict: pending", f"- Verdict: {review}")
            path.write_text(content)

    def advance_r1_to_maintain(self, change_id: str) -> None:
        for stage in ("build", "test", "deploy", "maintain"):
            self.run_cli("transition", "--change-id", change_id, "--stage", stage)

    def advance_r2_to_maintain(self, change_id: str) -> None:
        for stage in ("design", "build", "test", "deploy", "maintain"):
            self.run_cli("transition", "--change-id", change_id, "--stage", stage)

    def snapshot(self) -> dict[str, str]:
        snapshot: dict[str, str] = {}
        for path in sorted(self.repo.rglob("*")):
            if path.is_file() and ".git" not in path.parts:
                digest = hashlib.sha256(path.read_bytes()).hexdigest()
                snapshot[str(path.relative_to(self.repo))] = digest
        return snapshot

    def test_bootstrap_is_idempotent_and_preserves_existing_instructions(self) -> None:
        original_agents = "# Existing instructions\n\nKeep this text.\n"
        original_claude = "# Claude instructions\nDo not touch.\n"
        (self.repo / "AGENTS.md").write_text(original_agents)
        (self.repo / "CLAUDE.md").write_text(original_claude)

        first = self.run_cli("bootstrap")
        after_first = (self.repo / "AGENTS.md").read_text()
        second = self.run_cli("bootstrap")

        self.assertIn(".sdlc/config.json", json.loads(first.stdout)["changed"])
        self.assertEqual(after_first, (self.repo / "AGENTS.md").read_text())
        self.assertEqual(1, after_first.count("## AI-Native SDLC Integration"))
        self.assertIn(original_agents.rstrip(), after_first)
        self.assertEqual(original_claude, (self.repo / "CLAUDE.md").read_text())
        self.assertTrue(json.loads(second.stdout)["idempotent"])

    def test_bootstrap_refuses_ignored_sdlc(self) -> None:
        (self.repo / ".gitignore").write_text(".sdlc/\n")
        result = self.run_cli("bootstrap", expected=2)
        self.assertIn("excluded by .gitignore", result.stderr)
        self.assertFalse((self.repo / ".sdlc").exists())

    def test_r0_creates_no_change(self) -> None:
        self.bootstrap()
        result = self.run_cli("start", "--title", "Inspect repository", "--risk", "R0")
        self.assertFalse(json.loads(result.stdout)["persistent_change_created"])
        self.assertEqual([], list((self.repo / ".sdlc" / "changes").iterdir()))

    def test_each_risk_creates_exact_artifact_set(self) -> None:
        self.bootstrap()
        for risk in ("R1", "R2", "R3"):
            change_id = self.start(risk, f"Change {risk}")
            files = {
                path.name
                for path in (self.repo / ".sdlc" / "changes" / change_id).iterdir()
                if path.name != "state.json"
            }
            self.assertEqual(ARTIFACTS[risk], files)
            self.assertEqual(sorted(ARTIFACTS[risk]), sorted(self.state(change_id)["required_artifacts"]))

    def test_change_id_collision_uses_numeric_suffix(self) -> None:
        self.bootstrap()
        first = self.start("R1", "Same title")
        second = self.start("R1", "Same title")
        self.assertTrue(second.endswith("-02"))
        self.assertNotEqual(first, second)

    def test_multiple_active_changes_require_explicit_selection(self) -> None:
        self.bootstrap()
        self.start("R1", "First")
        self.start("R1", "Second")
        result = self.run_cli("status", expected=2)
        self.assertIn("Multiple active changes", result.stderr)

    def test_status_and_audit_are_read_only(self) -> None:
        self.bootstrap()
        change_id = self.start("R1")
        before = self.snapshot()
        self.run_cli("status", "--change-id", change_id)
        self.run_cli("audit", expected=1)
        self.assertEqual(before, self.snapshot())

    def test_close_requires_passing_evidence(self) -> None:
        self.bootstrap()
        change_id = self.start("R1")
        self.complete_artifacts(change_id)
        self.advance_r1_to_maintain(change_id)
        evidence_path = self.repo / ".sdlc/changes" / change_id / "evidence.md"
        evidence_path.write_text(evidence_path.read_text().replace("- Outcome: pass", "- Outcome: fail"))
        result = self.run_cli("close", "--change-id", change_id, expected=1)
        self.assertIn("evidence.md must contain", result.stdout)
        self.assertEqual("active", self.state(change_id)["status"])
        self.assertEqual("maintain", self.state(change_id)["current_stage"])

    def test_r2_closes_after_artifacts_review_and_evidence(self) -> None:
        self.bootstrap()
        change_id = self.start("R2")
        self.complete_artifacts(change_id)
        self.advance_r2_to_maintain(change_id)
        self.run_cli("close", "--change-id", change_id)
        state = self.state(change_id)
        self.assertEqual("complete", state["status"])
        self.assertEqual("closed", state["current_stage"])

    def test_r3_enforces_and_records_all_gates(self) -> None:
        self.bootstrap()
        change_id = self.start("R3", "Rotate production credentials", delivery="production")
        self.complete_artifacts(change_id)
        self.run_cli("transition", "--change-id", change_id, "--stage", "design")
        blocked = self.run_cli(
            "transition", "--change-id", change_id, "--stage", "build", expected=2
        )
        self.assertIn("requires approved spec gate", blocked.stderr)
        self.run_cli(
            "transition", "--change-id", change_id, "--approve-gate", "spec", "--approver", "Test owner", "--note", "Approved spec"
        )
        blocked = self.run_cli("transition", "--change-id", change_id, "--stage", "build", expected=2)
        self.assertIn("requires approved plan gate", blocked.stderr)
        self.run_cli(
            "transition", "--change-id", change_id, "--approve-gate", "plan", "--approver", "Test owner", "--note", "Approved plan"
        )
        self.run_cli("transition", "--change-id", change_id, "--stage", "build")
        self.run_cli("transition", "--change-id", change_id, "--stage", "test")
        self.run_cli("transition", "--change-id", change_id, "--stage", "deploy")
        blocked = self.run_cli(
            "transition", "--change-id", change_id, "--stage", "maintain", expected=2
        )
        self.assertIn("requires approved production gate", blocked.stderr)
        self.run_cli(
            "transition",
            "--change-id",
            change_id,
            "--approve-gate",
            "production",
            "--approver",
            "Test owner",
            "--note",
            "Approved production release",
        )
        self.run_cli("transition", "--change-id", change_id, "--stage", "maintain")
        self.run_cli("close", "--change-id", change_id)

        state = self.state(change_id)
        self.assertEqual(
            {"spec": "approved", "plan": "approved", "production": "approved"}, state["gates"]
        )
        approvals = (self.repo / ".sdlc" / "changes" / change_id / "approvals.md").read_text()
        self.assertIn("| spec | approved |", approvals)
        self.assertIn("| plan | approved |", approvals)
        self.assertIn("| production | approved |", approvals)

    def approve(self, change_id: str, gate: str) -> None:
        self.run_cli("transition", "--change-id", change_id, "--approve-gate", gate,
                     "--approver", "Test owner", "--note", "Fixture-only explicit decision")

    def test_r0_without_bootstrap_makes_no_writes(self) -> None:
        before = self.snapshot()
        self.run_cli("start", "--title", "Inspect", "--risk", "R0")
        self.run_cli("audit", expected=1)
        self.assertEqual(before, self.snapshot())

    def test_local_r3_closes_without_production_approval(self) -> None:
        self.bootstrap()
        change_id = self.start("R3", "Fix tenant boundary locally")
        self.complete_artifacts(change_id)
        self.run_cli("transition", "--change-id", change_id, "--stage", "design")
        self.approve(change_id, "spec")
        self.approve(change_id, "plan")
        for stage in ("build", "test", "deploy", "maintain"):
            self.run_cli("transition", "--change-id", change_id, "--stage", stage)
        self.run_cli("close", "--change-id", change_id)
        self.assertEqual("not_required", self.state(change_id)["gates"]["production"])

    def test_gate_has_no_default_human_approval(self) -> None:
        self.bootstrap()
        change_id = self.start("R3")
        self.complete_artifacts(change_id)
        before = self.snapshot()
        result = self.run_cli("transition", "--change-id", change_id, "--approve-gate", "spec", expected=2)
        self.assertIn("--approver and --note", result.stderr)
        self.assertEqual(before, self.snapshot())

    def test_invalid_combined_transition_does_not_append_approval(self) -> None:
        self.bootstrap()
        change_id = self.start("R3")
        self.complete_artifacts(change_id)
        before = self.snapshot()
        self.run_cli("transition", "--change-id", change_id, "--approve-gate", "spec",
                     "--approver", "Test owner", "--note", "Fixture decision", "--stage", "maintain", expected=2)
        self.assertEqual(before, self.snapshot())

    def test_changed_plan_invalidates_approval_before_build(self) -> None:
        self.bootstrap()
        change_id = self.start("R3")
        self.complete_artifacts(change_id)
        self.run_cli("transition", "--change-id", change_id, "--stage", "design")
        self.approve(change_id, "spec")
        self.approve(change_id, "plan")
        path = self.repo / ".sdlc/changes" / change_id / "plan.md"
        path.write_text(path.read_text() + "\nNew destructive operation.\n")
        before = self.snapshot()
        result = self.run_cli("transition", "--change-id", change_id, "--stage", "build", expected=2)
        self.assertIn("stale: plan", result.stderr)
        self.assertEqual(before, self.snapshot())

    def test_incomplete_plan_cannot_enter_build(self) -> None:
        self.bootstrap()
        change_id = self.start("R1")
        before = self.snapshot()
        self.run_cli("transition", "--change-id", change_id, "--stage", "build", expected=2)
        self.assertEqual(before, self.snapshot())

    def test_failing_checks_cannot_enter_delivery(self) -> None:
        self.bootstrap()
        change_id = self.start("R2")
        self.complete_artifacts(change_id, evidence="fail")
        for stage in ("design", "build", "test"):
            self.run_cli("transition", "--change-id", change_id, "--stage", stage)
        result = self.run_cli("transition", "--change-id", change_id, "--stage", "deploy", expected=2)
        self.assertIn("Outcome: pass", result.stderr)
        self.assertEqual("test", self.state(change_id)["current_stage"])

    def test_cancelled_change_cannot_be_reopened(self) -> None:
        self.bootstrap()
        change_id = self.start("R1")
        self.run_cli("transition", "--change-id", change_id, "--status", "cancelled")
        before = self.snapshot()
        self.run_cli("transition", "--change-id", change_id, "--status", "active", expected=2)
        self.assertEqual(before, self.snapshot())

    def test_path_traversal_is_rejected(self) -> None:
        self.bootstrap()
        before = self.snapshot()
        self.run_cli("status", "--change-id", "../../outside", expected=2)
        self.assertEqual(before, self.snapshot())

    def test_symlinked_sdlc_is_rejected(self) -> None:
        outside = Path(self.temp.name) / "outside"
        outside.mkdir()
        (self.repo / ".sdlc").symlink_to(outside, target_is_directory=True)
        self.run_cli("bootstrap", expected=2)
        self.assertEqual([], list(outside.iterdir()))

    def test_malformed_state_reports_issue_without_crash(self) -> None:
        self.bootstrap()
        change_id = self.start("R1")
        path = self.repo / ".sdlc/changes" / change_id / "state.json"
        state = self.state(change_id)
        state["required_artifacts"] = None
        state["gates"] = []
        path.write_text(json.dumps(state))
        result = self.run_cli("validate", "--change-id", change_id, expected=1)
        self.assertFalse(json.loads(result.stdout)["valid"])

    def test_duplicate_integration_fails_before_any_write(self) -> None:
        (self.repo / "AGENTS.md").write_text("## AI-Native SDLC Integration\n## AI-Native SDLC Integration\n")
        before = self.snapshot()
        self.run_cli("bootstrap", expected=2)
        self.assertEqual(before, self.snapshot())

    def test_project_inspection_is_read_only_and_finds_nested_stacks(self) -> None:
        (self.repo / "package.json").write_text('{"scripts":{"test":"DO NOT EXECUTE"}}')
        mobile = self.repo / "apps/mobile"
        mobile.mkdir(parents=True)
        (mobile / "build.gradle.kts").write_text("// fixture")
        before = self.snapshot()
        result = self.run_cli("inspect")
        payload = json.loads(result.stdout)
        self.assertIn("apps/mobile/build.gradle.kts", payload["candidates"])
        self.assertIn("package.json", payload["candidates"])
        self.assertFalse(payload["commands_executed_from_project"])
        self.assertEqual(before, self.snapshot())

    def test_production_delivery_cannot_use_low_risk(self) -> None:
        self.bootstrap()
        before = self.snapshot()
        self.run_cli("start", "--title", "Ship", "--risk", "R1", "--delivery", "production", expected=2)
        self.assertEqual(before, self.snapshot())

    def test_changed_release_source_invalidates_production_decision(self) -> None:
        self.bootstrap()
        (self.repo / "service.py").write_text("version = 1\n")
        change_id = self.start("R3", delivery="production")
        self.complete_artifacts(change_id)
        self.run_cli("transition", "--change-id", change_id, "--stage", "design")
        self.approve(change_id, "spec")
        self.approve(change_id, "plan")
        for stage in ("build", "test", "deploy"):
            self.run_cli("transition", "--change-id", change_id, "--stage", stage)
        self.approve(change_id, "production")
        (self.repo / "service.py").write_text("version = 2\n")
        before = self.snapshot()
        result = self.run_cli("transition", "--change-id", change_id, "--stage", "maintain", expected=2)
        self.assertIn("stale: production", result.stderr)
        self.assertEqual(before, self.snapshot())

    def test_change_artifacts_ignored_separately_block_bootstrap(self) -> None:
        (self.repo / ".gitignore").write_text(".sdlc/changes/\n")
        before = self.snapshot()
        self.run_cli("bootstrap", expected=2)
        self.assertEqual(before, self.snapshot())

    def test_legacy_completed_r2_state_remains_readable(self) -> None:
        self.bootstrap()
        change_id = self.start("R2")
        self.complete_artifacts(change_id)
        self.advance_r2_to_maintain(change_id)
        self.run_cli("close", "--change-id", change_id)
        path = self.repo / ".sdlc/changes" / change_id / "state.json"
        state = self.state(change_id)
        state.pop("delivery")
        state.pop("approval_records")
        path.write_text(json.dumps(state))
        before = self.snapshot()
        self.run_cli("validate", "--change-id", change_id, "--for-close")
        self.run_cli("status", "--change-id", change_id)
        self.assertEqual(before, self.snapshot())

    def test_dirty_worktree_content_is_preserved(self) -> None:
        tracked = self.repo / "tracked.txt"
        tracked.write_text("original\n")
        self.git("add", "tracked.txt")
        self.git("commit", "-q", "-m", "initial")
        tracked.write_text("user change\n")

        self.bootstrap()
        self.start("R1")

        self.assertEqual("user change\n", tracked.read_text())
        status = self.git("status", "--short").stdout
        self.assertIn(" M tracked.txt", status)


if __name__ == "__main__":
    unittest.main(verbosity=2)
