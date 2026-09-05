#!/usr/bin/env python3
"""Validate this marketplace's portable files without changing its contents."""

import ast
import json
from pathlib import Path
import re
import sys
from urllib.parse import unquote, urlsplit

import yaml


ROOT = Path(__file__).resolve().parents[1]


def require(condition, message):
    if not condition:
        raise ValueError(message)


def read_json(path):
    return json.loads(path.read_text(encoding="utf-8"))


def contained_path(base, relative):
    require(isinstance(relative, str) and relative, "Missing relative path")
    require(not Path(relative).is_absolute(), f"Absolute path: {relative}")
    path = (base / relative).resolve()
    require(path.is_relative_to(base), f"Path escapes its root: {relative}")
    require(path.exists(), f"Missing path: {relative}")
    return path


def validate():
    market = read_json(ROOT / ".agents/plugins/marketplace.json")
    require(re.fullmatch(r"[A-Za-z0-9_-]+", market["name"]), "Invalid marketplace name")
    require(market["plugins"], "Marketplace has no plugins")
    names = set()
    skill_count = 0
    case_count = 0
    for entry in market["plugins"]:
        name = entry["name"]
        require(name not in names, f"Duplicate plugin: {name}")
        names.add(name)
        require(entry["source"]["source"] == "local", f"Expected local source: {name}")
        require(entry["source"]["path"] == f"./plugins/{name}", f"Unexpected source path: {name}")
        plugin = contained_path(ROOT, entry["source"]["path"])
        manifest = read_json(plugin / ".codex-plugin/plugin.json")
        require(manifest["name"] == name == plugin.name, f"Plugin name mismatch: {name}")
        require(re.fullmatch(r"[A-Za-z0-9_-]+(?:\.[A-Za-z0-9_-]+)*", name), "Invalid plugin name")
        require(re.fullmatch(r"\d+\.\d+\.\d+(?:-[0-9A-Za-z.-]+)?(?:\+[0-9A-Za-z.-]+)?", manifest["version"]), f"Invalid version: {name}")
        require(manifest.get("description", "").strip(), f"Missing description: {name}")
        require("[TODO:" not in json.dumps(manifest), f"Manifest placeholder: {name}")
        require(entry["policy"]["installation"] in {"AVAILABLE", "NOT_AVAILABLE", "INSTALLED_BY_DEFAULT"}, "Invalid installation policy")
        require(entry["policy"]["authentication"] in {"ON_INSTALL", "ON_USE"}, "Invalid authentication policy")
        require(entry.get("category"), f"Missing category: {name}")
        skills = contained_path(plugin, manifest["skills"])
        skill_files = sorted(skills.glob("*/SKILL.md"))
        require(skill_files, f"No skills: {name}")
        for skill_file in skill_files:
            body = skill_file.read_text(encoding="utf-8")
            frontmatter = re.match(r"\A---\n(.*?)\n---(?:\n|$)", body, re.S)
            require(frontmatter, f"Missing frontmatter: {skill_file}")
            metadata = yaml.safe_load(frontmatter[1])
            skill_name = skill_file.parent.name
            require(metadata["name"] == skill_name, f"Skill name mismatch: {skill_name}")
            require(metadata.get("description", "").strip(), f"Missing skill description: {skill_name}")
            config = yaml.safe_load((skill_file.parent / "agents/openai.yaml").read_text(encoding="utf-8"))
            implicit = config["policy"]["allow_implicit_invocation"]
            require(type(implicit) is bool, f"Invocation policy must be boolean: {skill_name}")
            if skill_name == "ai-native-sdlc":
                require(implicit is False, "Coordinator must require explicit invocation")
            skill_count += 1
        cases = read_json(plugin / "evals/scenarios.json")["scenarios"]
        require(cases, f"Missing behavior scenarios: {name}")
        case_ids = set()
        for case in cases:
            require(case["id"] not in case_ids, f"Duplicate scenario: {case['id']}")
            require(case["prompt"].strip() and case["checks"], f"Empty scenario: {case['id']}")
            require(all(isinstance(check, str) and check.strip() for check in case["checks"]), "Invalid scenario check")
            case_ids.add(case["id"])
        case_count += len(cases)

    for file in ROOT.rglob("*"):
        relative = file.relative_to(ROOT)
        if any(part in {".git", ".venv", "__pycache__"} for part in relative.parts):
            continue
        if not file.is_file():
            continue
        if file.suffix == ".py":
            ast.parse(file.read_text(encoding="utf-8"), filename=str(relative))
        elif file.suffix in {".yaml", ".yml"}:
            yaml.safe_load(file.read_text(encoding="utf-8"))
        elif file.suffix == ".md":
            for target in re.findall(r"\]\(([^\s)]+)\)", file.read_text(encoding="utf-8")):
                link = urlsplit(target)
                if link.scheme or not link.path:
                    continue
                destination = (file.parent / unquote(link.path)).resolve()
                require(destination.is_relative_to(ROOT) and destination.exists(), f"Broken relative link in {relative}: {target}")
    print(f"PASS: {len(names)} plugin(s), {skill_count} skills, {case_count} behavior scenario definitions")


if __name__ == "__main__":
    try:
        validate()
    except (KeyError, TypeError, ValueError, OSError, SyntaxError, yaml.YAMLError) as error:
        print(f"FAIL: {error}", file=sys.stderr)
        sys.exit(1)
