# Hosted Gateway Architecture

## Logical components

- **Edge / TLS:** HTTPS termination and public hostname, supplied by the cloud platform.
- **ASGI service:** one FastAPI application with a mounted MCP Streamable HTTP sub-application.
- **HTTP interface:** JSON command invocation and command discovery.
- **MCP interface:** Remote MCP tools over Streamable HTTP.
- **Identity provider:** external OAuth 2.1 / OIDC issuer. The Gateway validates access tokens; it is not an authorization server.
- **Model adapter:** one configured OpenAI-compatible Chat Completions endpoint.
- **Command router:** canonical registry and skill files loaded from this repository image.
- **Rate limiter:** Redis fixed-window quota shared across replicas.
- **Audit channel:** structured metadata-only stdout events collected by the cloud logging service.
- **Secrets:** cloud secret manager supplies model key, Redis URL, and HMAC audit salt at runtime.

## Public path contract

One base URL is used for both protocols:

- \`/mcp\`: Streamable HTTP transport.
- \`/v1/invoke\`: synchronous JSON analysis request.
- \`/v1/commands\`: canonical command catalog.
- \`/healthz\`: liveness.
- \`/readyz\`: provider readiness.
- \`/.well-known/oauth-protected-resource/mcp\`: MCP authorization discovery metadata from the SDK.

## Trust boundaries

1. **Untrusted callers:** authenticate every MCP and API request. Validate JWT signature, issuer, audience/resource, expiry, and required scope.
2. **Untrusted request content:** treat user text as data. It cannot modify system prompts, routing policy, or tool permissions.
3. **Trusted package source:** canonical skills and registry are versioned in this repository. Container build provenance and branch protection remain repository/cloud responsibilities.
4. **External model provider:** send only necessary request content. API keys are server-side secrets. Do not log provider headers or raw request/response bodies.
5. **Audit sink:** logs carry pseudonymous identity and execution metadata only. Retention and log-reader access are cloud governance controls.

## Execution semantics

One Gateway request resolves one canonical command, loads one master orchestrator plus the configured specialist skill files, and performs one model-provider request. Specialist names describe logical responsibilities; no parallel or independent agents are created by this service.

No search, file, shell, repository-write, or external tool capability is granted to the model by this service. Tool execution status is returned as \`NOT_CONFIGURED\` until separately governed tool adapters are added.
