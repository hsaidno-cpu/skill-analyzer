# SKILL ANALYZER — Universal AI Invocation Gateway

**Gateway contract:** urn:skill-analyzer:invocation:v1  
**Introduced in package:** 1.1.0  
**Canonical registry:** gateway/registry.json

The Universal AI Invocation Gateway (UAIG) gives different AI runtimes one shared command vocabulary and routing contract. It separates the user's intent from each host's syntax for loading skills.

## 1. What the Gateway does

The Gateway normalizes aliases into canonical command IDs; routes commands to primary skills, optional supporting skills, and shared engines; maps platform-specific discovery paths and invocation strategies; records conditional capability readiness without guessing; produces a portable prompt or structured JSON envelope; and labels prepared work separately from work actually executed by an AI host.

The Gateway does **not** make every platform expose the same native command, grant tools, spawn agents, persist history, or provide a hosted API/MCP endpoint. The local CLI is a request compiler, not an AI execution runtime.

## 2. Four access modes

| Mode | Example | Portability |
|---|---|---|
| Natural language | "Use the skill-analyzer skill and run audit on this system..." | Highest; works wherever the skill instructions can be loaded |
| Native skill invocation | /skill-analyzer or a host skill picker | Depends on host and product surface |
| Platform custom command | Gemini CLI /analyzer:audit | Native only in the configured host |
| Structured envelope | JSON matching gateway/schemas/invocation.schema.json | Suitable for API, MCP, or agent integrations that implement the contract |

/analyzer <command> is a human-friendly convention, not a universal built-in command. Use the platform adapter rather than assuming the text will trigger a command everywhere.

## 3. Canonical command catalogue

| Command | Purpose | Main route |
|---|---|---|
| analyze | Adaptive root-cause and system analysis | skill-analyzer |
| audit | Critical audit and stress test | analyzer, negative-collector, evidence-auditor, information-authenticator |
| compare | Balanced multi-object comparison | komparator, comparative-analytic |
| methods | Method and framework selection | analytical-collector |
| authenticate | Claim and evidence verification | information-authenticator, evidence-auditor |
| forecast | Foresight and scenario analysis | strategic-foresight |
| evaluate | Program, outcome, and control evaluation | evaluator |
| reconstruct | Failure reconstruction and controlled correction | skill-analyzer plus relevant FIRE procedures |
| solution | Mitigation and implementation engineering | positive-converter, negative-collector, evaluator |
| decision | Decision intelligence and trade-off analysis | skill-analyzer plus Decision Intelligence Engine |
| platform | Compatibility, adapter, and invocation audit | invocation-gateway, platform-compatibility |

Aliases and engine routing are maintained only in gateway/registry.json.

## 4. Local CLI

Python 3.10+ is sufficient; no third-party dependency is required.

~~~~bash
# List canonical commands
python scripts/invoke.py list

# List target platform profiles
python scripts/invoke.py platforms

# Build a copy-paste prompt
python scripts/invoke.py resolve audit --target "SKILL ANALYZER repository" --objective "Audit the routing and invocation architecture" --platform claude-code --depth deep --format prompt

# Build a machine-readable request envelope
python scripts/invoke.py resolve compare --target "Option A versus Option B" --platform openai-api --format json

# Record an explicitly observed capability. Unspecified capabilities remain NOT_CHECKED.
python scripts/invoke.py resolve audit --target "Deployment workflow" --capability file_access=READY --capability web_search=UNAVAILABLE --format json
~~~~

The CLI accepts canonical IDs, aliases, and the shorthand /analyzer:audit. It does not connect to a model or verify user-declared capability status. Do not label its output as executed analysis.

## 5. Platform-specific invocation

### OpenAI Codex

Install or export the skills into .agents/skills/. Then ask:

~~~~text
Use the skill-analyzer skill. Execute the Gateway command "audit" against the following target: [target]. Read GATEWAY.md and gateway/registry.json if available. Use sequential routing unless native delegation is verified.
~~~~

Codex selects skills from their metadata and explicit skill naming; /analyzer is not assumed to be a built-in Codex command.

### Claude Code

Install .claude/skills/ or the user-level skill directory. Invoke the master skill:

~~~~text
/skill-analyzer Audit [target]. Resolve the request using Gateway command audit.
~~~~

Claude Code can expose a skill by its name as a slash command. The subcommand audit remains a Gateway vocabulary item, not a separately installed Claude command.

### GitHub Copilot

For Copilot CLI, install the project skills under .github/skills/ or a documented personal skill directory, then use:

~~~~text
Use the /skill-analyzer skill to audit [target]. Follow Gateway command audit.
~~~~

For VS Code, select the skill from the slash picker when it is surfaced. If it is not visible, explicitly name it in the prompt and verify discovery with the host's skill-management command. Copilot app, CLI, and VS Code capabilities are not interchangeable.

### Gemini CLI

This repository contains an extension manifest, a context file, bundled skills, and custom prompt commands. Install the repository as an extension:

~~~~bash
gemini extensions install https://github.com/hsaidno-cpu/skill-analyzer
~~~~

Then restart or reload the extension and use:

~~~~text
/analyzer:audit [target]
/analyzer:compare [target A] versus [target B]
/analyzer:forecast [question or strategic topic]
~~~~

Use /extensions list to verify extension installation and /skills list to inspect skill discovery. These commands are specific to Gemini CLI.

### Cursor

Install .cursor/skills/ or .agents/skills/. Invoke through the skill picker:

~~~~text
/skill-analyzer
~~~~

Then provide the Gateway command and target. Cursor also supports attaching a skill through the @ picker. Cloud Agent access to local skills depends on skill sync and project scope.

### Visual Studio Code

VS Code is a host shell. Choose the discovery path supported by the active agent integration. When its slash picker exposes Agent Skills, select skill-analyzer; otherwise explicitly mention the skill. Do not infer the active harness from the editor name alone.

### OpenAI Responses API / Agents SDK

Expose the skill bundle using the host's supported skill-bundle or capability-directory configuration. Then instruct the model explicitly:

~~~~text
Use the skill-analyzer skill. Execute Gateway command audit for the supplied target. Follow the canonical routing registry and return the invocation status and capability limitations.
~~~~

The application must configure tools, sandbox access, authentication, and function/MCP wiring separately. The JSON envelope is an integration contract; the Gateway CLI does not submit an API request.

### ChatGPT app/plugin package

Select or open the SKILL ANALYZER app/plugin, then state the command and target in the message. The OpenAI plugin manifest and its app distribution mechanism remain separate from the generic Agent Skills package.

## 6. Invocation envelope

An integration can send a JSON object with the following conceptual structure:

~~~~json
{
  "protocol": "urn:skill-analyzer:invocation:v1",
  "request": {
    "request_id": "example-0001",
    "command": "audit",
    "target": "Example system",
    "objective": "Identify material risks and testable improvements",
    "mode": "verification",
    "depth": "deep",
    "constraints": []
  },
  "platform": {
    "id": "generic",
    "label": "Generic Agent Skills client",
    "invocation_type": "natural_language",
    "native_slash_command": false
  }
}
~~~~

For a complete validated structure, use the schema file. Capability statuses must come from user declaration or runtime observation, never from platform assumptions.

## 7. Orchestration and trust boundaries

- The host decides whether a skill is automatically selected, explicitly invoked, or loaded by an adapter.
- Run specialists sequentially unless actual subagent/delegation capability is verified.
- A READY capability claim must be backed by an actual observation or explicit user declaration.
- BLOCKED, UNAVAILABLE, and ACCESS_DENIED block the dependent branch; do not silently downgrade them to success.
- Gateway output starts at PREPARED_NOT_EXECUTED. Only the target runtime can establish that execution took place.
- Prompt instructions are not a security boundary. Use host permissions, sandbox policy, MCP authorization, or external middleware for enforceable controls.

## 8. Extending the Gateway

To add a command:
1. Add one canonical record to gateway/registry.json.
2. Add aliases that cannot collide with existing aliases.
3. Map to existing skills and engine identifiers; do not duplicate analytical instructions.
4. Add platform-native commands only where supported, mapping back to the canonical command ID.
5. Add positive, negative, alias, and unknown-command tests.
6. Update this guide and the compatibility reference.

To add a platform:
1. Verify official discovery and invocation documentation.
2. Add a profile to gateway/platforms.json.
3. Add an exporter profile only when required.
4. Keep unsupported capabilities as NOT_CHECKED or UNAVAILABLE.
5. Test the exact host version and product surface before marking it verified.

## 9. Official platform references

- [OpenAI API skills](https://developers.openai.com/api/docs/guides/tools-skills)
- [OpenAI API tools](https://developers.openai.com/api/docs/guides/tools)
- [Claude Code skills and extensions](https://code.claude.com/docs/en/features-overview)
- [GitHub Copilot CLI agent skills](https://docs.github.com/en/copilot/how-tos/copilot-cli/customize-copilot/add-skills)
- [GitHub Copilot app slash commands](https://docs.github.com/en/copilot/reference/github-copilot-app-reference/slash-commands)
- [Gemini CLI extensions](https://geminicli.com/docs/extensions/)
- [Gemini CLI extension authoring](https://github.com/google-gemini/gemini-cli/blob/main/docs/extensions/writing-extensions.md)
- [Gemini CLI Agent Skills](https://github.com/google-gemini/gemini-cli/blob/main/docs/cli/using-agent-skills.md)
- [Cursor Agent Skills](https://cursor.com/help/customization/skills)
- [VS Code Agent Skills](https://code.visualstudio.com/docs/agent-customization/agent-skills)
