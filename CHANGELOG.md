# Changelog

## 1.1.0 — 2026-11-10

### Added
- Universal AI Invocation Gateway with a canonical command registry, aliases, routing rules, platform profiles, and a versioned JSON invocation envelope.
- Dependency-free local CLI for command resolution and portable prompt/JSON generation.
- Dedicated invocation-gateway utility skill.
- Gemini CLI extension packaging at repository root, with native custom prompt commands for all eleven Gateway commands.
- Gateway-aware platform exporter and expanded portability validator.
- Unit tests for command resolution, platform profiles, capability readiness, and execution-state honesty.

### Changed
- Package version bumped from 1.0.0 to 1.1.0.
- README and portability documentation now describe platform-specific access and the Gateway contract.
- Platform exports now include the Gateway registry, profile data, documentation, and invocation compiler.

### Preserved
- Plugin identity and existing audience/scope.
- Ten analytical specialist responsibilities and five cross-skill engines.
- Existing three default prompts, including their order and string values.
- Existing analytical schemas, evidence gates, and failure-control semantics.
- Single canonical skill source under skills/; platform adapters remain thin mappings.

### Important boundary
- The local CLI prepares invocation payloads; it does not invoke a model, provide tools, launch subagents, or persist runtime traces.
- Gemini CLI custom commands are bundled as native prompt shortcuts. Other platforms retain their documented native invocation behavior.
- Cross-platform static packaging is not equivalent to host-level runtime verification.
