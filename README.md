# SKILL ANALYZER 1.3.0

**A modular, evidence-led analysis system with a portable Agent Skills core and a Universal AI Invocation Gateway.**

SKILL ANALYZER combines ten analytical specialists, five shared engines, two utility skills, and the Universal Access Manager orchestrator with six access subskills. The Universal AI Invocation Gateway provides a canonical command registry, platform invocation adapters, a JSON envelope contract, and a local prompt compiler.

## What changed in 1.3.0

- Adds Universal Access Manager as one orchestrator with six specialist skills for consumer API keys, inbound MCP access, outbound MCP/REST connectors, credential vault, and identity/policy enforcement.
- Adds the canonical Gateway command access and the Gemini CLI shortcut /analyzer:access.
- Adds Access Manager architecture, trust boundaries, security invariants, runtime acceptance criteria, tests, and portability validation.
- Explicitly labels key issuance, credential storage, and outbound connectors as backend-dependent capabilities, not active features of the existing runtime.

## What changed in 1.2.0

- Adds a deployable cloud runtime for Remote MCP and JSON HTTP API on one public origin.
- Adds OAuth 2.1/OIDC JWT verification, centralized command routing, OpenAI-compatible model execution, Redis rate limiting, and metadata-only audit logging.
- Adds a Docker image, cloud deployment guide, remote-gateway profile, and cloud integration tests.
- Local adapter installation is optional when using the hosted service: callers connect to the remote MCP endpoint or HTTP API.

## What changed in 1.1.0

- Adds the Universal AI Invocation Gateway with eleven canonical commands and alias normalization.
- Adds platform profiles for Codex, Claude Code, GitHub Copilot surfaces, Gemini CLI, Cursor, VS Code, OpenAI API, ChatGPT package, and generic Agent Skills clients.
- Adds a versioned JSON invocation envelope and schema.
- Adds a dependency-free CLI to resolve commands and generate platform-ready prompts or JSON.
- Adds a Gemini CLI extension manifest and eleven custom command shortcuts.
- Extends the exporter to ship Gateway contracts and invocation tooling with each profile.
- Extends static validation and CI with routing, alias, adapter, and command tests.

## Core architecture

The analytical master orchestrator routes to ten responsibilities: analytical-collector, analyzer, negative-collector, positive-converter, evidence-auditor, strategic-foresight, evaluator, komparator, comparative-analytic, and information-authenticator. Five engines provide shared procedures for decisions, human impact/governance, benchmark/regression, knowledge/method intelligence, and FIRE.

The two utility skills, platform-compatibility and invocation-gateway, maintain distribution and invocation. Separately, universal-access-manager routes six access specialists: api-key-manager, mcp-access-manager, custom-mcp-connector, custom-api-connector, credential-vault, and identity-policy-engine.

## Quick start

~~~~bash
# Validate the package and Gateway contracts
python scripts/validate_portability.py

# List available commands
python scripts/invoke.py list

# Generate a prompt for any supported host profile
python scripts/invoke.py resolve audit --target "Your system or document" --platform generic --depth deep

# Generate machine-readable invocation JSON
python scripts/invoke.py resolve compare --target "Option A versus Option B" --platform openai-api --format json

# Export platform-specific skills and Gateway adapters
python scripts/export_platforms.py --target all --output ./dist

# Run routing contract tests
python -m unittest discover -s tests -v
~~~~

See [GATEWAY.md](GATEWAY.md) for command syntax, installation, platform-specific invocation, and the JSON contract. See [ACCESS_MANAGER.md](ACCESS_MANAGER.md) for access orchestration and security boundaries. See [PORTABILITY.md](PORTABILITY.md) for distribution profiles and compatibility boundaries.

## Gemini CLI quick install

The repository root includes a Gemini extension manifest, context entrypoint, bundled Agent Skills, and custom prompt commands:

~~~~bash
gemini extensions install https://github.com/hsaidno-cpu/skill-analyzer
~~~~

After installation, use commands such as /analyzer:audit, /analyzer:compare, /analyzer:forecast, or /analyzer:access. Verify the extension and skills with the relevant Gemini CLI list commands.

## Reliability boundary

The Gateway normalizes intent and prepares routing. The CLI does not call an AI model, grant platform tools, spawn agents, or persist execution traces. A passing package or static CI job does not prove that a particular host discovers a skill, selects the correct model behavior, executes a subagent, or produces correct conclusions. Platform-specific behavior must be tested and recorded against the exact host, model/provider, version, product surface, and evidence.


## Hosted Universal Cloud Gateway

The repository includes a deployable service package:

- Remote MCP (Streamable HTTP): `https://YOUR_DOMAIN/mcp`
- HTTP API: `https://YOUR_DOMAIN/v1/invoke`
- Command discovery: `https://YOUR_DOMAIN/v1/commands`
- Health/readiness: `/healthz` and `/readyz`

Both protocols share one public base URL. A caller that uses the hosted service does not need to install local SKILL ANALYZER adapters or copy the skill directory. It needs an OAuth 2.1/OIDC access token with the `analyzer:invoke` scope.

See [CLOUD_DEPLOYMENT.md](CLOUD_DEPLOYMENT.md) for local setup, production secrets, OIDC configuration, Redis, and a Cloud Run reference deployment. See [CLOUD_ARCHITECTURE.md](CLOUD_ARCHITECTURE.md) for trust boundaries.

**Deployment status:** the service implementation is committed, but this repository has not provisioned a public cloud endpoint. A cloud account, domain, OIDC issuer, model API key, Redis service, and deployment operation are required before a public URL exists.