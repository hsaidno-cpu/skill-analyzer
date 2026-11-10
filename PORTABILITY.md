# SKILL ANALYZER — Cross-Platform Distribution

**Release:** 1.0.0  
**Canonical format:** Agent Skills (`SKILL.md`)  
**Canonical source:** `skills/`

SKILL ANALYZER is authored once in a vendor-neutral skill layout. Platform-specific export profiles copy that canonical source into the discovery locations expected by each target. The adapters do not rewrite analytical rules or claim that different hosts execute them identically.

## Supported distribution profiles

| Target | Project-level discovery path | Integration status | Important boundary |
|---|---|---|---|
| OpenAI Codex | `.agents/skills/` | Native Agent Skills | Tool access, MCP, and runtime traces depend on the Codex environment. |
| ChatGPT plugin | `skills/` plus `plugin.json` | Native package profile | Plugin manifest and app integrations are OpenAI-specific. |
| Claude Code | `.claude/skills/` | Native Agent Skills | Subagents, hooks, MCP, and permission controls are host capabilities, not portable skill features. |
| GitHub Copilot | `.github/skills/` | Native Agent Skills | Availability varies by Copilot product surface and IDE/version. |
| Gemini CLI | `skills/` in a Gemini extension with `gemini-extension.json` | Native extension profile | Extension packaging, commands, hooks, and MCP configuration are Gemini-specific. |
| Cursor | `.cursor/skills/` or `.agents/skills/` | Native Agent Skills | Cloud-agent availability can differ from local project skill discovery. |
| VS Code | `.github/skills/`, `.claude/skills/`, or `.agents/skills/` depending on the selected harness | Harness-dependent | Select the directory supported by the active agent integration. |
| Other Agent Skills clients | Their documented skill directory | Conditional | Verify the client’s current specification and runtime limits before claiming support. |

The portable contract is the skill directory (`SKILL.md`, `references/`, optional `scripts/` and `assets/`). It is not a guarantee that every platform exposes the same agents, tools, memory, schedules, browsing, filesystem, or security enforcement.

## Export

Run from the package root:

```bash
python scripts/export_platforms.py --target all --output ./dist
```

Available targets: `codex`, `claude`, `copilot`, `gemini`, `cursor`, `portable`, or `all`.

The exporter copies the complete canonical `skills/` tree, preserving references and schemas. For Gemini CLI it also writes a minimal `gemini-extension.json` and a `GEMINI.md` context entrypoint. It does not install the extension or publish it to a marketplace.

Examples:

```bash
python scripts/export_platforms.py --target codex --output ./dist
python scripts/export_platforms.py --target claude --output ./dist
python scripts/export_platforms.py --target copilot --output ./dist
python scripts/export_platforms.py --target gemini --output ./dist
python scripts/export_platforms.py --target cursor --output ./dist
```

## Validate

```bash
python scripts/validate_portability.py
```

The validator checks manifest parity, preserved default prompts, semantic version parity, skill frontmatter and folder names, local Markdown references, and JSON syntax of schema files. It does not run a model, invoke a platform agent, test host routing, validate every JSON Schema instance, or prove runtime behavior.

## Installation quick map

- **Codex:** copy the exported `.agents/skills/` directory into the repository or user skill location supported by your Codex setup.
- **Claude Code:** copy `.claude/skills/` into the project or your user-level skill location.
- **GitHub Copilot:** copy `.github/skills/` into the repository. Use Copilot's supported product surface and version.
- **Gemini CLI:** install the exported Gemini extension from a Git repository or local extension directory using Gemini CLI's extension workflow.
- **Cursor:** copy `.cursor/skills/` into the project, or use `.agents/skills/` where appropriate.
- **ChatGPT/Codex plugin:** use the package manifest and plugin distribution workflow; do not substitute a Gemini extension manifest or generic skill directory for the plugin package.

## Capability boundary

Before analysis, map required capabilities to the active host: file access, web/search, code execution, schema validation, persistence, subagents, MCP, Git operations, runtime traces, and release controls. Record each required capability using the Capability Readiness statuses already defined by SKILL ANALYZER. Never infer availability from a product name or from a skill being visible.

If a capability is unavailable, use only an independently authorized and functionally adequate fallback. Otherwise mark that branch `BLOCKED` or `UNAVAILABLE`, disclose the limitation, and continue only with separable work.

## Versioning and source of truth

- Edit `skills/` first; generated platform copies are disposable build outputs.
- Keep each skill's `name` equal to its skill-directory name.
- Keep local references relative to the file that contains the link.
- Do not store secrets, access tokens, user data, or credentials in the package.
- Do not add host-specific tool names to the canonical core unless they are clearly marked as examples and mapped through a host adapter.
- When platform-specific behavior changes, update the compatibility matrix and the relevant test cases.
