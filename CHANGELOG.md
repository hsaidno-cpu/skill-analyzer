# Changelog

## 1.2.0 — 2026-11-10

### Added
- Deployable cloud runtime using FastAPI and MCP Python SDK v2 Streamable HTTP.
- One-origin Remote MCP endpoint at `/mcp` and JSON HTTP API at `/v1/invoke`.
- External OAuth 2.1 / OIDC resource-server token verification with issuer, JWKS, audience, expiry, signature, and scope checks.
- Central command routing from the canonical Gateway registry and skill package.
- OpenAI-compatible model-provider adapter with server-side credentials.
- Redis-backed distributed rate limiting with fail-closed behavior.
- Metadata-only structured audit events with HMAC-pseudonymous actor identifiers.
- Container packaging, cloud deployment guide, architecture document, and cloud export profile.
- Cloud service tests and CI checks for the HTTP/MCP runtime and production container.

### Changed
- Package version bumped from 1.1.0 to 1.2.0.
- Added a remote-gateway platform profile for callers that do not want to install local skills or adapters.
- Development dependency entrypoint now includes the cloud runtime and test dependencies.

### Preserved
- Plugin identity, the ten analytical specialists, five shared engines, and existing default prompts.
- Canonical source trees under `skills/` and `gateway/`.
- Explicit separation between logical specialist routing and actual independent-agent execution.
- Evidence, authentication, governance, failure-control, and fail-closed semantics.

### Important boundaries
- The service package is deployable but is not automatically deployed by a GitHub commit.
- A real public URL requires a cloud deployment, DNS/custom domain, external OIDC issuer, model-provider secret, Redis service, and production environment configuration.
- This release uses one configured OpenAI-compatible model endpoint and one model call per invocation. Separate subagents, web search, filesystem tools, external execution, conversation persistence, provider failover, and tenant billing are not enabled by this service.
- Audit logs are metadata-only; retention, access governance, and tamper-resistant storage are responsibilities of the deployed logging platform.

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
