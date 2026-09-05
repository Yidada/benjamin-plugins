#!/usr/bin/env python3
"""Check non-mutation and fail-closed environment inspection."""
import json
from pathlib import Path
import tempfile
import unittest
from unittest.mock import patch
from preflight import inspect_project


class PreflightTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)

    def test_new_project_is_not_initialized(self):
        with patch("preflight.shutil.which", return_value="/bin/true"):
            result = inspect_project(self.root)
        self.assertEqual(result["registry_state"], "absent")
        self.assertFalse(result["runtime_verified"])
        self.assertFalse(result["driver_verified"])
        self.assertEqual(list(self.root.iterdir()), [])

    def test_existing_registry_is_preserved(self):
        registry = self.root / ".loopx/registry.json"
        registry.parent.mkdir()
        original = json.dumps({"goals": [{"id": "original"}]})
        registry.write_text(original)
        result = inspect_project(self.root)
        self.assertEqual(result["registry_state"], "present_unverified")
        self.assertEqual(registry.read_text(), original)
        self.assertFalse(result["runtime_verified"])

    def test_corruption_is_not_empty(self):
        registry = self.root / ".loopx/registry.json"
        registry.parent.mkdir()
        for value in ("{broken", "[]", "null", "\"text\""):
            registry.write_text(value)
            self.assertIn(inspect_project(self.root)["registry_state"],
                          {"invalid", "invalid_or_unreadable"})
            self.assertEqual(registry.read_text(), value)

    def test_dangling_registry_is_not_absent(self):
        registry = self.root / ".loopx/registry.json"
        registry.parent.mkdir()
        registry.symlink_to(self.root / "missing.json")
        self.assertEqual(inspect_project(self.root)["registry_state"], "invalid_or_unreadable")

    def test_missing_project_is_not_created(self):
        missing = self.root / "missing"
        with self.assertRaises(FileNotFoundError):
            inspect_project(missing)
        self.assertFalse(missing.exists())

    def test_cli_is_not_shell_evaluated(self):
        marker = self.root / "executed"
        with self.assertRaises(ValueError):
            inspect_project(self.root, f"loopx; touch {marker}")
        self.assertFalse(marker.exists())


if __name__ == "__main__":
    unittest.main()
