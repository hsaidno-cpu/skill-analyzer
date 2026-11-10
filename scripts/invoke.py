#!/usr/bin/env python3
"""Compile SKILL ANALYZER Gateway commands into portable prompts or JSON envelopes."""
from __future__ import annotations

import argparse
import json
import sys
import uuid
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
REGISTRY_PATH = ROOT / "gateway" / "registry.json"
PLATFORMS_PATH = ROOT / "gateway" / "platforms.json"

CAPABILITY_STATUSES = {
    "READY", "READY_WITH_LIMITATIONS", "BLOCKED", "UNAVAILABLE",
    "ACCESS_DENIED", "NOT_CHECKED", "EXPIRED", "NOT_APPLICABLE",
}
BLOCKING_STATUSES = {"BLOCKED", "UNAVAILABLE", "ACCESS_DENIED", "EXPIRED"}
KNOWN_CAPABILITIES = {
    "web_search", "file_access", "code_execution", "json_validation",
    "mcp", "git_read", "git_write", "subagents", "persistence",
    "runtime_trace", "approval",
}


def read_json(path: Path) -> dict[str, Any]:
    try:
        value = json.loads(path.read_text(encoding="utf-8"))
    except FileNotFoundError as exc:
        raise RuntimeError(f"Required Gateway file is missing: {path}") from exc
    except json.JSONDecodeError as exc:
        raise RuntimeError(f"Invalid JSON in {path}: {exc}") from exc
    if not isinstance(value, dict):
        raise RuntimeError(f"Expected a JSON object in {path}")
    return value


def load_catalog() -> tuple[dict[str, Any], dict[str, Any]]:
    registry = read_json(REGISTRY_PATH)
    platforms = read_json(PLATFORMS_PATH)
    if not isinstance(registry.get("commands"), list):
        raise RuntimeError("Gateway registry must contain a commands array")
    if not isinstance(platforms.get("profiles"), dict):
        raise RuntimeError("Gateway platform file must contain a profiles object")
    return registry, platforms


def normalize_command(value: str) -> str:
    token = value.strip().lower()
    if token.startswith("/"):
        token = token[1:]
    if token.startswith("skill-analyzer "):
        token = token[len("skill-analyzer "):].strip()
    if token.startswith("analyzer:"):
        token = token.split(":", 1)[1].strip()
    elif token.startswith("analyzer "):
        token = token.split(None, 1)[1].strip()
    return token.replace("_", "-")


def resolve_command(value: str, registry: dict[str, Any]) -> dict[str, Any]:
    token = normalize_command(value)
    matches = []
    for item in registry["commands"]:
        accepted = {item["id"], *item.get("aliases", [])}
        normalized = {normalize_command(alias) for alias in accepted}
        if token in normalized:
            matches.append(item)
    if not matches:
        raise ValueError(f"Unknown Gateway command: {value!r}. Run 'python scripts/invoke.py list'.")
    if len(matches) > 1:
        raise ValueError(f"Ambiguous Gateway command alias: {value!r}. Use a canonical command ID.")
    return matches[0]


def parse_capability_declaration(value: str) -> tuple[str, str]:
    if "=" not in value:
        raise ValueError(f"Invalid capability declaration {value!r}; expected name=STATUS")
    name, status = value.split("=", 1)
    name = name.strip().lower()
    status = status.strip().upper()
    if name not in KNOWN_CAPABILITIES:
        raise ValueError(f"Unknown capability name: {name}")
    if status not in CAPABILITY_STATUSES:
        raise ValueError(f"Invalid capability status: {status}")
    return name, status


def build_envelope(
    command_value: str,
    target: str,
    registry: dict[str, Any],
    platforms: dict[str, Any],
    platform_id: str = "generic",
    objective: str | None = None,
    scope: str | None = None,
    mode: str | None = None,
    depth: str = "deep",
    context: str = "",
    constraints: list[str] | None = None,
    desired_output: str | None = None,
    capability_declarations: list[str] | None = None,
) -> dict[str, Any]:
    command = resolve_command(command_value, registry)
    profiles = platforms["profiles"]
    if platform_id not in profiles:
        available = ", ".join(sorted(profiles))
        raise ValueError(f"Unknown platform {platform_id!r}. Available platforms: {available}")
    if not target.strip():
        raise ValueError("Target must not be empty")
    if depth not in {"standard", "deep", "forensic"}:
        raise ValueError("Depth must be one of: standard, deep, forensic")

    platform = profiles[platform_id]
    declarations: dict[str, str] = {}
    for item in capability_declarations or []:
        name, status = parse_capability_declaration(item)
        declarations[name] = status

    conditional = list(command.get("conditional_capabilities", []))
    irrelevant = sorted(set(declarations) - set(conditional))
    if irrelevant:
        raise ValueError(
            "Capability declarations not relevant to this command: " + ", ".join(irrelevant)
        )
    statuses = {name: declarations.get(name, "NOT_CHECKED") for name in conditional}
    blocked = [name for name, status in statuses.items() if status in BLOCKING_STATUSES]
    normalized_mode = mode or command.get("default_mode", "adaptive")

    request = {
        "request_id": uuid.uuid4().hex[:12],
        "command": command["id"],
        "original_command": command_value,
        "target": target.strip(),
        "objective": objective or command["description"],
        "scope": scope or "Not specified; do not invent scope boundaries.",
        "mode": normalized_mode,
        "depth": depth,
        "context": context,
        "constraints": constraints or [],
        "desired_output": desired_output or "Structured findings, evidence limits, residual unknowns, and actionable next steps appropriate to the command."
    }

    envelope = {
        "protocol": registry.get("protocol", "urn:skill-analyzer:invocation:v1"),
        "request": request,
        "routing": {
            "primary_skills": command.get("primary_skills", []),
            "supporting_skills": command.get("supporting_skills", []),
            "engines": command.get("engines", []),
            "delegation_policy": "host_native_if_verified_otherwise_sequential"
        },
        "platform": {
            "id": platform_id,
            "label": platform["label"],
            "project_skill_paths": platform.get("project_skill_paths", []),
            "invocation_type": platform["invocation_type"],
            "explicit_invocation": platform["explicit_invocation"],
            "native_slash_command": platform["native_slash_command"],
            "notes": platform.get("notes", "")
        },
        "capability_readiness": {
            "conditional_capabilities": conditional,
            "statuses": statuses,
            "blocked_branches": blocked,
            "source": "user_declared" if declarations else "not_checked"
        },
        "execution": {
            "status": "PREPARED_NOT_EXECUTED",
            "mode": "host_native_if_verified_otherwise_sequential",
            "host_controls_execution": True,
            "warning": "This CLI compiles an invocation request. It does not call an AI model, run host tools, verify declared capabilities, or persist execution traces."
        }
    }
    envelope["prompt"] = render_prompt(envelope)
    return envelope


def render_prompt(envelope: dict[str, Any]) -> str:
    req = envelope["request"]
    routing = envelope["routing"]
    platform = envelope["platform"]
    caps = envelope["capability_readiness"]["statuses"]
    lines = [
        "# SKILL ANALYZER — UNIVERSAL INVOCATION",
        "",
        f"Protocol: {envelope['protocol']}",
        f"Request ID: {req['request_id']}",
        f"Canonical command: {req['command']}",
        f"Target: {req['target']}",
        f"Objective: {req['objective']}",
        f"Platform: {platform['label']} ({platform['id']})",
        f"Invocation strategy: {platform['invocation_type']}",
        f"Mode / depth: {req['mode']} / {req['depth']}",
        "",
        "## Routing",
        "Primary skills: " + ", ".join(routing["primary_skills"]),
        "Supporting skills (conditional): " + (", ".join(routing["supporting_skills"]) or "none"),
        "Shared engines (activate when relevant): " + (", ".join(routing["engines"]) or "none"),
        "Delegation: host-native only if verified; otherwise sequential.",
        "",
        "## Capability readiness",
        "The following are declarations or runtime observations, not facts verified by this CLI:"
    ]
    for name, status in caps.items():
        lines.append(f"- {name}: {status}")
    if envelope["capability_readiness"]["blocked_branches"]:
        lines.extend([
            "",
            "Blocked dependent branches: " + ", ".join(envelope["capability_readiness"]["blocked_branches"]),
            "Do not simulate those operations or silently replace their status with PASS."
        ])
    lines.extend([
        "",
        "## Execution instructions",
        "1. Confirm that the routed skills are actually discoverable in this host. Load their SKILL.md files and only the references they require.",
        "2. Follow the canonical Gateway registry. Preserve evidence, authentication, governance, and fail-closed rules.",
        "3. Check each tool, permission, and data source at the point of use. Any unlisted capability remains NOT_CHECKED.",
        "4. Use native delegation only if this runtime demonstrably supports it; otherwise run a sequential workflow and label it as such.",
        "5. Distinguish evidence, assumption, inference, hypothesis, prediction, and recommendation. Do not invent source checks or test results.",
        "6. Report the canonical command, selected skills, capability gaps, limitations, and what was actually executed.",
        "",
        f"Scope: {req['scope']}",
        f"Context: {req['context'] or 'Not supplied'}",
        "Constraints: " + ("; ".join(req["constraints"]) if req["constraints"] else "None supplied"),
        f"Desired output: {req['desired_output']}",
        "",
        "Execution status at compile time: PREPARED_NOT_EXECUTED. Change this only after the host has actually performed the work.",
        "",
        "Platform adapter instruction: " + platform["explicit_invocation"],
        "Platform notes: " + platform["notes"]
    ])
    return "\n".join(lines)


def command_list(registry: dict[str, Any]) -> None:
    for item in registry["commands"]:
        aliases = ", ".join(item.get("aliases", []))
        print(f"{item['id']:<14} {item['description']}")
        if aliases:
            print(f"  aliases: {aliases}")


def platform_list(platforms: dict[str, Any]) -> None:
    for key, item in platforms["profiles"].items():
        print(f"{key:<24} {item['label']}")
        print(f"  paths: {', '.join(item.get('project_skill_paths', []))}")
        print(f"  invocation: {item['invocation_type']}; native slash: {item['native_slash_command']}")


def make_parser(platform_ids: list[str]) -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__)
    sub = parser.add_subparsers(dest="action", required=True)
    sub.add_parser("list", help="List canonical Gateway commands")
    sub.add_parser("platforms", help="List platform invocation profiles")

    resolve = sub.add_parser("resolve", help="Resolve a command and emit a prompt or JSON envelope")
    resolve.add_argument("command", help="Canonical command ID or alias, e.g. audit or /analyzer:audit")
    resolve.add_argument("--target", required=True, help="The system, topic, document, decision, or objects to analyze")
    resolve.add_argument("--objective", help="Specific outcome expected from the command")
    resolve.add_argument("--scope", help="Scope boundary; do not invent one when omitted")
    resolve.add_argument("--mode", help="Override the command's default mode")
    resolve.add_argument("--depth", choices=["standard", "deep", "forensic"], default="deep")
    resolve.add_argument("--context", default="", help="Optional context or background")
    resolve.add_argument("--constraint", action="append", default=[], help="Constraint; repeat for multiple constraints")
    resolve.add_argument("--desired-output", help="Desired output shape")
    resolve.add_argument("--platform", choices=platform_ids, default="generic")
    resolve.add_argument("--capability", action="append", default=[], metavar="NAME=STATUS",
                         help="Explicit capability declaration; repeat as needed. Unspecified capabilities stay NOT_CHECKED.")
    resolve.add_argument("--format", choices=["prompt", "json"], default="prompt")
    return parser


def main(argv: list[str] | None = None) -> int:
    try:
        registry, platforms = load_catalog()
        parser = make_parser(sorted(platforms["profiles"]))
        args = parser.parse_args(argv)
        if args.action == "list":
            command_list(registry)
            return 0
        if args.action == "platforms":
            platform_list(platforms)
            return 0

        envelope = build_envelope(
            command_value=args.command,
            target=args.target,
            registry=registry,
            platforms=platforms,
            platform_id=args.platform,
            objective=args.objective,
            scope=args.scope,
            mode=args.mode,
            depth=args.depth,
            context=args.context,
            constraints=args.constraint,
            desired_output=args.desired_output,
            capability_declarations=args.capability,
        )
        if args.format == "json":
            print(json.dumps(envelope, ensure_ascii=False, indent=2))
        else:
            print(envelope["prompt"])
        return 0
    except (ValueError, RuntimeError) as exc:
        print(f"Gateway error: {exc}", file=sys.stderr)
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
