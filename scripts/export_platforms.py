#!/usr/bin/env python3
"""Export canonical SKILL ANALYZER skills, Gateway contracts, and host adapters."""
from __future__ import annotations

import argparse
import json
import shutil
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SKILLS = ROOT / "skills"
GATEWAY = ROOT / "gateway"
COMMANDS = ROOT / "commands"
PROFILES = {
    "codex": (".agents/skills", "Codex / Agent Skills"),
    "claude": (".claude/skills", "Claude Code / Agent Skills"),
    "copilot": (".github/skills", "GitHub Copilot / Agent Skills"),
    "cursor": (".cursor/skills", "Cursor / Agent Skills"),
    "portable": ("skills", "Generic Agent Skills package"),
    "gemini": ("skills", "Gemini CLI extension"),
    "cloud": ("skills", "Universal Cloud Gateway service"),
}

ENTRYPOINTS = {
    "codex": """# AGENTS.md — SKILL ANALYZER

This profile includes canonical Agent Skills plus the Universal AI Invocation Gateway. Read GATEWAY.md and gateway/registry.json for command routing. Explicitly name the skill-analyzer skill in prompts. Do not assume /analyzer is a native Codex command. Use native delegation only when actually available and verified.
""",
    "claude": """# CLAUDE.md — SKILL ANALYZER

Reusable Agent Skills are packaged under .claude/skills/. Invoke the master workflow with /skill-analyzer, then provide a canonical Gateway command such as audit or compare. Read GATEWAY.md and gateway/registry.json for routing. Skills are instructions, not permissions or tools.
""",
    "copilot": """# GitHub Copilot repository instructions

Reusable Agent Skills are packaged under .github/skills/. Select /skill-analyzer from the skill picker when available, or explicitly name it in the prompt. Use GATEWAY.md and gateway/registry.json for canonical commands. Tool availability and slash-command behavior depend on the active Copilot surface.
""",
}

def copy_tree(source: Path, target: Path) -> None:
    if not source.is_dir():
        raise FileNotFoundError(f"Required source directory not found: {source}")
    shutil.copytree(source, target, dirs_exist_ok=True)

def copy_file(source: Path, target: Path) -> None:
    if not source.is_file():
        raise FileNotFoundError(f"Required source file not found: {source}")
    target.parent.mkdir(parents=True, exist_ok=True)
    shutil.copy2(source, target)

def export_one(name: str, output: Path, version: str, description: str) -> list[str]:
    relative, label = PROFILES[name]
    profile_root = output / name
    profile_root.mkdir(parents=True, exist_ok=True)

    copy_tree(SKILLS, profile_root / relative)
    copy_tree(GATEWAY, profile_root / "gateway")
    copy_file(ROOT / "GATEWAY.md", profile_root / "GATEWAY.md")
    copy_file(ROOT / "scripts" / "invoke.py", profile_root / "scripts" / "invoke.py")

    written = [
        str((profile_root / relative).relative_to(output)),
        str((profile_root / "gateway").relative_to(output)),
        str((profile_root / "GATEWAY.md").relative_to(output)),
        str((profile_root / "scripts" / "invoke.py").relative_to(output)),
    ]

    if name in ENTRYPOINTS:
        entry_name = {"codex": "AGENTS.md", "claude": "CLAUDE.md", "copilot": ".github/copilot-instructions.md"}[name]
        entry_path = profile_root / entry_name
        entry_path.parent.mkdir(parents=True, exist_ok=True)
        entry_path.write_text(ENTRYPOINTS[name], encoding="utf-8")
        written.append(str(entry_path.relative_to(output)))

    if name == "gemini":
        copy_file(ROOT / "GEMINI.md", profile_root / "GEMINI.md")
        copy_tree(COMMANDS, profile_root / "commands")
        manifest = {
            "name": "skill-analyzer",
            "version": version,
            "contextFileName": "GEMINI.md",
            "description": description,
        }
        manifest_path = profile_root / "gemini-extension.json"
        manifest_path.write_text(json.dumps(manifest, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
        written.extend([
            str((profile_root / "GEMINI.md").relative_to(output)),
            str((profile_root / "commands").relative_to(output)),
            str(manifest_path.relative_to(output)),
        ])

    if name == "cloud":
        copy_tree(ROOT / "service", profile_root / "service")
        for filename in ("Dockerfile", "CLOUD_DEPLOYMENT.md", "CLOUD_ARCHITECTURE.md",
                         "requirements-cloud.txt", ".env.example", ".dockerignore"):
            copy_file(ROOT / filename, profile_root / filename)
        written.extend([
            str((profile_root / "service").relative_to(output)),
            str((profile_root / "Dockerfile").relative_to(output)),
            str((profile_root / "CLOUD_DEPLOYMENT.md").relative_to(output)),
            str((profile_root / "CLOUD_ARCHITECTURE.md").relative_to(output)),
            str((profile_root / "requirements-cloud.txt").relative_to(output)),
            str((profile_root / ".env.example").relative_to(output)),
            str((profile_root / ".dockerignore").relative_to(output)),
        ])

    profile_text = (
        f"Target: {label}\n"
        f"Canonical version: {version}\n"
        f"Generated from: skills/ + gateway/\n"
        f"Invocation protocol: urn:skill-analyzer:invocation:v1\n"
    )
    (profile_root / "PROFILE.txt").write_text(profile_text, encoding="utf-8")
    written.append(str((profile_root / "PROFILE.txt").relative_to(output)))
    return written

def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--target", choices=["all", *PROFILES.keys()], default="all")
    parser.add_argument("--output", type=Path, required=True, help="Directory where platform profiles will be written")
    args = parser.parse_args()

    manifest = json.loads((ROOT / "plugin.json").read_text(encoding="utf-8"))
    version = manifest.get("version", "unknown")
    description = manifest.get("description", "SKILL ANALYZER portable Agent Skills package")
    targets = list(PROFILES) if args.target == "all" else [args.target]
    output = args.output.resolve()
    output.mkdir(parents=True, exist_ok=True)

    generated: list[str] = []
    for target in targets:
        generated.extend(export_one(target, output, version, description))

    report = {
        "package": "skill-analyzer",
        "version": version,
        "invocation_protocol": "urn:skill-analyzer:invocation:v1",
        "targets": targets,
        "files_written": generated,
    }
    (output / "export-report.json").write_text(
        json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
    )
    print(json.dumps(report, ensure_ascii=False, indent=2))
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
