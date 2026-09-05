#!/usr/bin/env python3
"""Inspect a project without executing LoopX, creating state, or installing tools."""
import argparse
import json
import os
from pathlib import Path
import shutil
import sys


def inspect_project(project, cli=None):
    root = Path(project).expanduser().resolve(strict=True)
    if not root.is_dir():
        raise ValueError("Project must be a directory")
    executable = shutil.which(cli or "loopx")
    if cli and not executable:
        raise ValueError("Explicit LoopX executable is missing or not executable")
    if not executable:
        candidates = [
            Path.home() / ".local/share/benjamin-loopx/venv/bin/loopx",
            Path.home() / ".local/share/benjamin-loopx/venv/Scripts/loopx.exe",
            Path.home() / ".local/bin/loopx",
        ]
        executable = next((str(p) for p in candidates if p.is_file() and os.access(p, os.X_OK)), None)
    registry = root / ".loopx/registry.json"
    state = "absent"
    if os.path.lexists(registry):
        try:
            data = json.loads(registry.read_text(encoding="utf-8"))
            state = "present_unverified" if isinstance(data, dict) else "invalid"
        except (OSError, ValueError, UnicodeError):
            state = "invalid_or_unreadable"
    return {
        "project": str(root),
        "python_supported": sys.version_info >= (3, 11),
        "loopx_executable": str(Path(executable).resolve()) if executable else None,
        "registry_state": state,
        "runtime_verified": False,
        "driver_verified": False,
    }


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--project", required=True)
    parser.add_argument("--loopx-bin", help="Installed executable, never a shell command")
    args = parser.parse_args()
    try:
        result = inspect_project(args.project, args.loopx_bin)
    except (OSError, ValueError) as exc:
        print(json.dumps({"error": str(exc), "runtime_verified": False}))
        return 2
    print(json.dumps(result, ensure_ascii=False, indent=2))
    invalid = result["registry_state"] in {"invalid", "invalid_or_unreadable"}
    return 2 if invalid or not result["loopx_executable"] or not result["python_supported"] else 0


if __name__ == "__main__":
    raise SystemExit(main())
