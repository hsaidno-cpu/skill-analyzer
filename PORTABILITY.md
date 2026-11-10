# SKILL ANALYZER — Cross-Platform Distribution

**Release:** 1.1.0  
**Canonical format:** Agent Skills (SKILL.md)  
**Canonical skill source:** skills/  
**Invocation contract:** urn:skill-analyzer:invocation:v1

SKILL ANALYZER is authored once in a vendor-neutral skill layout. The Universal AI Invocation Gateway adds a canonical command vocabulary and maps it to host-specific invocation behavior. The Gateway does not force different runtimes to behave identically.

## Supported distribution profiles

| Target | Project-level discovery path | Invocation strategy | Integration boundary |
|---|---|---|---|
| OpenAI Codex | .agents/skills/ | Natural language or explicit skill name | Do not assume /analyzer is a native Codex command. |
| ChatGPT app/plugin | skills/ plus plugin.json | Select the app/plugin, then provide a Gateway command | OpenAI manifest and app distribution remain host-specific. |
| Claude Code | .claude/skills/ | Invoke /skill-analyzer, then provide the command | Slash skill invocation is native; Gateway subcommands are a shared vocabulary. |
| GitHub Copilot CLI | .github/skills/ or .agents/skills/ | Explicit skill name, natural language, or supported skill syntax | Verify the current CLI version and skill discovery. |
| GitHub Copilot in VS Code | .github/skills/ or .agents/skills/ | Skill picker/slash invocation when surfaced; otherwise explicit prompt | IDE version, workspace discovery, and policy affect availability. |
| GitHub Copilot app | Host-managed skill source | Surface-dependent prompt/skill selection | Do not assume custom repository skills are available in every app session. |
| Gemini CLI | Extension root with gemini-extension.json, GEMINI.md, skills/, commands/ | Native custom commands such as /analyzer:audit | Extension commands and Agent Skills are Gemini-specific adapters. |
| Cursor | .cursor/skills/ or .agents/skills/ | Skill slash picker or @ attachment | Cloud Agent sync and project scope differ from local discovery. |
| VS Code | Path supported by active harness | Harness-dependent skill picker or explicit skill name | VS Code is a host shell, not one uniform agent runtime. |
| Other Agent Skills clients | Client-documented skill directory | Natural language or client-native selection | Conditional; verify the client specification and runtime. |

The portable contract includes SKILL.md, references, scripts, and assets. It does not guarantee uniform tools, memory, schedules, browsing, filesystem access, agent delegation, or enforcement.

## Universal AI Invocation Gateway

Read [GATEWAY.md](GATEWAY.md) for the full contract. Its canonical sources are:

- gateway/registry.json: commands, aliases, skill routing, engine routing, and conditional capability declarations.
- gateway/platforms.json: platform-specific paths and invocation behavior.
- gateway/schemas/invocation.schema.json: versioned invocation envelope.
- skills/invocation-gateway/SKILL.md: runtime routing and safety instructions.
- scripts/invoke.py: local command resolver and prompt/JSON compiler.

The command registry uses stable IDs: analyze, audit, compare, methods, authenticate, forecast, evaluate, reconstruct, solution, decision, and platform. Platform-specific commands must map back to these IDs; they must not fork the analytical logic.

## Export

Run from the package root:

~~~~bash
python scripts/export_platforms.py --target all --output ./dist
~~~~

Available targets: codex, claude, copilot, gemini, cursor, portable, or all.

Each export contains the canonical skills, Gateway registry and profiles, GATEWAY.md, and the local invocation compiler. The Gemini profile also includes its extension manifest, context file, and custom command shortcuts. Exporting does not install the package or publish it to a marketplace.

Examples:

~~~~bash
python scripts/export_platforms.py --target codex --output ./dist
python scripts/export_platforms.py --target claude --output ./dist
python scripts/export_platforms.py --target copilot --output ./dist
python scripts/export_platforms.py --target gemini --output ./dist
python scripts/export_platforms.py --target cursor --output ./dist
~~~~

## Validate and test

~~~~bash
python scripts/validate_portability.py
python -m unittest discover -s tests -v
python scripts/invoke.py list
python scripts/invoke.py platforms
~~~~

Static validation checks manifest parity, skill frontmatter, local references, JSON schemas, Gateway command IDs and aliases, skill routing, platform profiles, and Gemini command parity. Unit tests exercise alias resolution, capability handling, and execution-status boundaries.

These tests do not run a model or prove real host skill discovery, model selection, tool access, agent delegation, persistence, or runtime traces. Host behavior requires separate tests using the exact platform, version, product surface, and evidence.

## Gemini CLI direct installation

The repository root is packaged as a Gemini CLI extension:

~~~~bash
gemini extensions install https://github.com/hsaidno-cpu/skill-analyzer
~~~~

After install, reload/restart the extension as required by the CLI version. Verify extension and skill discovery with /extensions list and /skills list. Custom commands are provided as prompt-only TOML files under commands/analyzer/. They do not execute shell commands or call external services.

## Capability boundary

Before a tool-dependent branch, check the exact operation, access, permission, and scope. Use the readiness statuses READY, READY_WITH_LIMITATIONS, BLOCKED, UNAVAILABLE, ACCESS_DENIED, NOT_CHECKED, EXPIRED, and NOT_APPLICABLE.

A platform name, skill file, manifest, or successful export does not prove that browsing, shell, file access, MCP, Git, subagents, persistence, or runtime traces are enabled. If a required capability is unavailable, block that branch or use an independently authorized and functionally adequate fallback. Never simulate a successful operation.

## Versioning and source of truth

- Edit skills/ and gateway/ as canonical sources.
- Keep platform adapter commands thin; map them to canonical command IDs.
- Keep each skill name equal to its directory name.
- Keep relative resource paths relative to the file that contains the link.
- Do not store secrets, access tokens, user data, or credentials in the package.
- Do not add host-specific tool names to the portable core unless clearly marked and mapped through an adapter.
- Re-check official platform documentation before major releases.
- Mark a platform VERIFIED only for tested behavior on a recorded host/version/surface; otherwise use NOT_TESTED or NOT_CHECKED.
