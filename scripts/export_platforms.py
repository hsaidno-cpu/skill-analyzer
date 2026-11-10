#!/usr/bin/env python3
"""Export canonical SKILL ANALYZER skills to documented host discovery paths."""
from __future__ import annotations

import argparse
import json
import shutil
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SKILLS = ROOT / "skills"
PROFILES = {
    "codex": (".agents/skills", "Codex / Agent Skills"),
    "claude": (".claude/skills", "Claude Code / Agent Skills"),
    "copilot": (".github/skills", "GitHub Copilot / Agent Skills"),
    "cursor": (".cursor/skills", "Cursor / Agent Skills"),
    "portable": ("skills", "Generic Agent Skills package"),
    "gemini": ("skills", "Gemini CLI extension"),
}

ENTRYPOINTS = {
    "codex": """# AGENTS.md — SKILL ANALYZER\n\nThis repository includes portable Agent Skills under `.agents/skills/`. Select the relevant skill by its frontmatter description. For full-cycle analysis, start with `skill-analyzer`; load specialist references progressively. Do not claim unavailable tools, subagents, persistence, or host traces.\n""",
    "claude": """# CLAUDE.md — SKILL ANALYZER\n\nReusable Agent Skills are packaged under `.claude/skills/`. Use their `SKILL.md` descriptions for task routing. Skills are instructions, not permissions or tools. Spawn subagents only when the active Claude Code runtime actually supports and performs that operation.\n""",
    "copilot": """# GitHub Copilot repository instructions\n\nReusable Agent Skills are packaged under `.github/skills/`. Load the relevant `SKILL.md` when its description matches the task. Keep static package validation, host behavior, and runtime traces as separate evidence layers. Tool availability depends on the active Copilot surface.\n""",
    "gemini": """# GEMINI.md — SKILL ANALYZER\n\nThis Gemini CLI extension includes Agent Skills under `skills/`. Select the relevant skill from its frontmatter description and load referenced resources only when needed. Do not assume MCP, shell, sub-agents, persistence, or Git permissions are available; check the actual extension/runtime configuration.\n""",
}


def copy_skills(target: Path) -> None:
    if not SKILLS.is_dir():
        raise FileNotFoundError(f"Canonical skills directory not found: {SKILLS}")
    shutil.copytree(SKILLS, target, dirs_exist_ok=True)


def export_one(name: str, output: Path, version: str, description: str) -> list[str]:
    relative, label = PROFILES[name]
    profile_root = output / name
    profile_root.mkdir(parents=True, exist_ok=True)
    copy_skills(profile_root / relative)
    written = [str((profile_root / relative).relative_to(output))]

    if name in ENTRYPOINTS:
        entry_name = {"codex": "AGENTS.md", "claude": "CLAUDE.md", "copilot": ".github/copilot-instructions.md", "gemini": "GEMINI.md"}[name]
        entry_path = profile_root / entry_name
        entry_path.parent.mkdir(parents=True, exist_ok=True)
        entry_path.write_text(ENTRYPOINTS[name], encoding="utf-8")
        written.append(str(entry_path.relative_to(output)))

    if name == "gemini":
        manifest = {
            "name": "skill-analyzer",
            "version": version,
            "description": description,
            "contextFileName": "GEMINI.md",
        }
        manifest_path = profile_root / "gemini-extension.json"
        manifest_path.write_text(json.dumps(manifest, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
        written.append(str(manifest_path.relative_to(output)))

    (profile_root / "PROFILE.txt").write_text(
        f"Target: {label}\nCanonical version: {version}\nGenerated from: {SKILLS.relative_to(ROOT)}\n",
        encoding="utf-8",
    )
    written.append(str((profile_root / "PROFILE.txt").relative_to(output)))
    return written


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--target", choices=["all", *PROFILES.keys()], default="all")
    parser.add_argument("--output", type=Path, required=True, help="Directory where platform profiles will be written")
    args = parser.parse_args()

    manifest_path = ROOT / "plugin.json"
    manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    version = manifest.get("version", "unknown")
    description = manifest.get("description", "SKILL ANALYZER portable Agent Skills package")
    targets = list(PROFILES) if args.target == "all" else [args.target]
    output = args.output.resolve()
    output.mkdir(parents=True, exist_ok=True)

    generated: list[str] = []
    for target in targets:
        generated.extend(export_one(target, output, version, description))

    report = {"package": "skill-analyzer", "version": version, "targets": targets, "files_written": generated}
    (output / "export-report.json").write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(report, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
