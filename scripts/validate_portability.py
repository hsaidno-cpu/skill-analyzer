#!/usr/bin/env python3
"""Dependency-free static checks for manifests, skills, Gateway contracts, and adapters."""
from __future__ import annotations

import json
import re
import sys
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
errors: list[str] = []
checks: list[str] = []

EXPECTED_SKILLS = {
    "skill-analyzer", "analytical-collector", "analyzer", "negative-collector",
    "positive-converter", "evidence-auditor", "strategic-foresight", "evaluator",
    "komparator", "comparative-analytic", "information-authenticator",
    "platform-compatibility", "invocation-gateway",
}

def fail(message: str) -> None:
    errors.append(message)

def check(condition: bool, message: str) -> None:
    if condition:
        checks.append(message)
    else:
        fail(message)

def read_json(path: Path) -> Any:
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except Exception as exc:  # noqa: BLE001 - report malformed package files
        fail(f"Invalid JSON {path.relative_to(ROOT)}: {exc}")
        return None

root_manifest = read_json(ROOT / "plugin.json")
codex_manifest = read_json(ROOT / ".codex-plugin" / "plugin.json")
if isinstance(root_manifest, dict) and isinstance(codex_manifest, dict):
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
skill_names = {path.parent.name for path in skill_files}
check(EXPECTED_SKILLS.issubset(skill_names), "all ten specialists, master orchestrator, and two utility skills are present")
check(len(skill_files) == len(skill_names), "one SKILL.md per skill directory")

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

# Local Markdown links.
markdown_files = [*ROOT.glob("skills/**/*.md"), ROOT / "PORTABILITY.md", ROOT / "GATEWAY.md"]
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

# Validate all committed JSON schema files.
schema_paths = sorted([*ROOT.glob("skills/**/*.schema.json"), *ROOT.glob("gateway/**/*.schema.json")])
for schema_path in schema_paths:
    parsed = read_json(schema_path)
    if parsed is not None:
        check(isinstance(parsed, dict) and parsed.get("type") == "object", f"schema is a JSON object: {schema_path.relative_to(ROOT)}")

registry = read_json(ROOT / "gateway" / "registry.json")
platform_data = read_json(ROOT / "gateway" / "platforms.json")
if isinstance(registry, dict) and isinstance(platform_data, dict):
    commands = registry.get("commands", [])
    profiles = platform_data.get("profiles", {})
    check(registry.get("protocol") == "urn:skill-analyzer:invocation:v1", "Gateway protocol identifier is stable")
    check(isinstance(commands, list) and len(commands) >= 10, "Gateway command registry contains core commands")
    check(isinstance(profiles, dict) and len(profiles) >= 8, "Gateway contains multiple platform profiles")

    command_ids: set[str] = set()
    alias_owners: dict[str, str] = {}
    for item in commands:
        if not isinstance(item, dict):
            fail("Gateway command record must be an object")
            continue
        command_id = item.get("id")
        check(isinstance(command_id, str) and bool(command_id), "Gateway command ID exists")
        if not isinstance(command_id, str):
            continue
        if command_id in command_ids:
            fail(f"Duplicate Gateway command ID: {command_id}")
        command_ids.add(command_id)
        for alias in [command_id, *item.get("aliases", [])]:
            normalized = alias.strip().lower().lstrip("/")
            if normalized.startswith("analyzer:"):
                normalized = normalized.split(":", 1)[1]
            if normalized.startswith("analyzer "):
                normalized = normalized.split(None, 1)[1]
            normalized = normalized.replace("_", "-")
            previous = alias_owners.get(normalized)
            if previous and previous != command_id:
                fail(f"Gateway alias collision: {alias!r} maps to {previous} and {command_id}")
            alias_owners[normalized] = command_id
        for skill in item.get("primary_skills", []) + item.get("supporting_skills", []):
            check(skill in skill_names, f"Gateway route references existing skill: {command_id} -> {skill}")

    # Ensure the Gemini extension has one custom command per canonical command ID.
    gemini_manifest = read_json(ROOT / "gemini-extension.json")
    if isinstance(gemini_manifest, dict) and isinstance(root_manifest, dict):
        check(gemini_manifest.get("name") == "skill-analyzer", "Gemini extension identity")
        check(gemini_manifest.get("version") == root_manifest.get("version"), "Gemini extension version parity")
        context_file = gemini_manifest.get("contextFileName", "GEMINI.md")
        check((ROOT / context_file).is_file(), "Gemini extension context file exists")
    gemini_commands = sorted((ROOT / "commands" / "analyzer").glob("*.toml"))
    command_files = {path.stem: path for path in gemini_commands}
    check(set(command_files) == command_ids, "Gemini custom command set matches canonical registry")
    for command_id, command_path in command_files.items():
        command_text = command_path.read_text(encoding="utf-8")
        check("prompt = \"\"\"" in command_text and "{{args}}" in command_text, f"Gemini prompt command format: {command_id}")
        check(f"Canonical command: {command_id}" in command_text, f"Gemini command maps to canonical ID: {command_id}")

# Required Gateway implementation files.
required_files = [
    "GATEWAY.md", "GEMINI.md", "gemini-extension.json",
    "CLOUD_DEPLOYMENT.md", "CLOUD_ARCHITECTURE.md",
    "gateway/registry.json", "gateway/platforms.json",
    "gateway/schemas/invocation.schema.json", "scripts/invoke.py",
    "tests/test_invocation_gateway.py", "scripts/export_platforms.py",
    "requirements-cloud.txt", "Dockerfile",
    "service/app/__init__.py", "service/app/config.py",
    "service/app/auth.py", "service/app/audit.py", "service/app/limiter.py",
    "service/app/provider.py", "service/app/runtime.py", "service/app/main.py",
    "service/tests/test_cloud_gateway.py",
]
for relative in required_files:
    check((ROOT / relative).is_file(), f"required Gateway file exists: {relative}")

summary = {"checks_passed": len(checks), "errors": errors, "status": "PASS" if not errors else "FAIL"}
print(json.dumps(summary, ensure_ascii=False, indent=2))
if errors:
    print("\nFailed checks:\n- " + "\n- ".join(errors), file=sys.stderr)
    raise SystemExit(1)
