# SKILL ANALYZER — Gemini CLI Extension

Use the bundled Agent Skills under skills/. The Universal AI Invocation Gateway contract is defined in GATEWAY.md, with command routes in gateway/registry.json and this extension's platform profile in gateway/platforms.json.

The extension adds custom prompt commands under commands/analyzer/. Each command maps to one canonical command ID in the registry:
- /analyzer:analyze
- /analyzer:audit
- /analyzer:compare
- /analyzer:methods
- /analyzer:authenticate
- /analyzer:forecast
- /analyzer:evaluate
- /analyzer:reconstruct
- /analyzer:solution
- /analyzer:decision
- /analyzer:platform

Treat the command files as prompt shortcuts, not as independent analytical implementations. Load the selected canonical skill instructions and supporting references from skills/.

Do not assume an MCP server, web access, shell, Git write access, persistence, or separate subagents are available. Check the actual Gemini CLI configuration before a tool-dependent operation. Keep execution status separate from command preparation, and never claim that a command ran unless the model actually performs the work.
