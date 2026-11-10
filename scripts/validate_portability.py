#!/usr/bin/env python3
"""Dependency-free static checks for the SKILL ANALYZER portable package."""
from __future__ import annotations

import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
errors: list[str] = []
checks: list[str] = []


def fail(message: str) -> None:
    errors.append(message)


def check(condition: bool, message: str) -> None:
    if condition:
        checks.append(message)
    else:
        fail(message)


def read_json(path: Path):
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except Exception as exc:  # noqa: BLE001 - report malformed package files
        fail(f"Invalid JSON {path.relative_to(ROOT)}: {exc}")
        return None


root_manifest_path = ROOT / "plugin.json"
codex_manifest_path = ROOT / ".codex-plugin" / "plugin.json"
root_manifest = read_json(root_manifest_path)
codex_manifest = read_json(codex_manifest_path)

if root_manifest and codex_manifest:
    check(root_manifest.get("name") == codex_manifest.get("name") == "skill-analyzer", "manifest identity parity")
    check(root_manifest.get("version") == codex_manifest.get("version"), "manifest version parity")
    check(root_manifest.get("description") == codex_manifest.get("description"), "manifest description parity")
    root_interface = root_manifest.get("extensions", {}).get("com.openai", {}).get("interface", {})
    codex_interface = codex_manifest.get("interface", {})
    check(root_interface.get("defaultPrompt") == codex_interface.get("defaultPrompt"), "defaultPrompt value/type/order parity")
    check(root_interface.get("shortDescription") == codex_interface.get("shortDescription"), "presentation parity")
    check(len(root_interface.get("shortDescription", "")) <= 30, "shortDescription <= 30 characters")
    check(root_manifest.get("skills") == "./skills" and codex_manifest.get("skills") == "./skills", "canonical skills path parity")

skills_root = ROOT / "skills"
skill_files = sorted(skills_root.glob("*/SKILL.md"))
check(len(skill_files) >= 12, "master, ten core specialist skills, and platform utility are present")

for skill_path in skill_files:
    content = skill_path.read_text(encoding="utf-8")
    if not content.startswith("---\n"):
        fail(f"Missing YAML frontmatter: {skill_path.relative_to(ROOT)}")
        continue
    end = content.find("\n---", 4)
    if end < 0:
        fail(f"Unclosed YAML frontmatter: {skill_path.relative_to(ROOT)}")
        continue
    front = content[4:end]
    name_match = re.search(r"^name:\s*([a-z0-9-]+)\s*$", front, re.M)
    desc_match = re.search(r"^description:\s*(.+)$", front, re.M)
    folder = skill_path.parent.name
    check(bool(name_match), f"frontmatter name exists: {folder}")
    check(bool(desc_match and desc_match.group(1).strip()), f"frontmatter description exists: {folder}")
    if name_match:
        check(name_match.group(1) == folder, f"skill name matches folder: {folder}")

# Validate relative Markdown links in skill files and portability docs.
markdown_files = [*ROOT.glob("skills/**/*.md"), ROOT / "PORTABILITY.md"]
link_pattern = re.compile(r"\[[^\]]*\]\(([^)]+)\)")
for md_path in markdown_files:
    if not md_path.exists():
        continue
    body = md_path.read_text(encoding="utf-8")
    for destination in link_pattern.findall(body):
        destination = destination.strip()
        if not destination or destination.startswith(("http://", "https://", "#", "mailto:")):
            continue
        target_text = destination.split("#", 1)[0]
        if not target_text:
            continue
        target = (md_path.parent / target_text).resolve()
        try:
            target.relative_to(ROOT.resolve())
        except ValueError:
            fail(f"Relative link escapes package root: {md_path.relative_to(ROOT)} -> {destination}")
            continue
        check(target.exists(), f"local link exists: {md_path.relative_to(ROOT)} -> {destination}")

schema_paths = sorted(ROOT.glob("skills/**/*.schema.json"))
for schema_path in schema_paths:
    parsed = read_json(schema_path)
    if parsed is not None:
        check(isinstance(parsed, dict), f"schema is a JSON object: {schema_path.relative_to(ROOT)}")

# Check that the compatibility reference and exporter are present.
check((ROOT / "skills/skill-analyzer/references/cross-platform-compatibility.md").exists(), "cross-platform compatibility reference exists")
check((ROOT / "scripts/export_platforms.py").exists(), "platform exporter exists")
check((ROOT / "PORTABILITY.md").exists(), "portability guide exists")

summary = {"checks_passed": len(checks), "errors": errors, "status": "PASS" if not errors else "FAIL"}
print(json.dumps(summary, ensure_ascii=False, indent=2))
if errors:
    print("\nFailed checks:\n- " + "\n- ".join(errors), file=sys.stderr)
    raise SystemExit(1)
