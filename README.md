# SKILL ANALYZER 1.1.0

**A modular, evidence-led analysis system with a portable Agent Skills core and a Universal AI Invocation Gateway.**

SKILL ANALYZER combines ten analytical specialists, five shared engines, and two utility skills. The Universal AI Invocation Gateway adds a canonical command registry, platform invocation adapters, a JSON envelope contract, and a local prompt compiler.

## What changed in 1.1.0

- Adds the Universal AI Invocation Gateway with eleven canonical commands and alias normalization.
- Adds platform profiles for Codex, Claude Code, GitHub Copilot surfaces, Gemini CLI, Cursor, VS Code, OpenAI API, ChatGPT package, and generic Agent Skills clients.
- Adds a versioned JSON invocation envelope and schema.
- Adds a dependency-free CLI to resolve commands and generate platform-ready prompts or JSON.
- Adds a Gemini CLI extension manifest and eleven custom command shortcuts.
- Extends the exporter to ship Gateway contracts and invocation tooling with each profile.
- Extends static validation and CI with routing, alias, adapter, and command tests.

## Core architecture

The master orchestrator routes to ten analytical responsibilities: analytical-collector, analyzer, negative-collector, positive-converter, evidence-auditor, strategic-foresight, evaluator, komparator, comparative-analytic, and information-authenticator. Five engines provide shared procedures for decisions, human impact/governance, benchmark/regression, knowledge/method intelligence, and FIRE.

The two utility skills, platform-compatibility and invocation-gateway, maintain distribution and access. They are not additional analytical specialists.

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

See [GATEWAY.md](GATEWAY.md) for command syntax, installation, platform-specific invocation, and the JSON contract. See [PORTABILITY.md](PORTABILITY.md) for distribution profiles and compatibility boundaries.

## Gemini CLI quick install

The repository root includes a Gemini extension manifest, context entrypoint, bundled Agent Skills, and custom prompt commands:

~~~~bash
gemini extensions install https://github.com/hsaidno-cpu/skill-analyzer
~~~~

After installation, use commands such as /analyzer:audit, /analyzer:compare, or /analyzer:forecast. Verify the extension and skills with the relevant Gemini CLI list commands.

## Reliability boundary

The Gateway normalizes intent and prepares routing. The CLI does not call an AI model, grant platform tools, spawn agents, or persist execution traces. A passing package or static CI job does not prove that a particular host discovers a skill, selects the correct model behavior, executes a subagent, or produces correct conclusions. Platform-specific behavior must be tested and recorded against the exact host, model/provider, version, product surface, and evidence.
