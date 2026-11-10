# SKILL ANALYZER 1.0.0

**A modular, evidence-led analysis system with a portable Agent Skills core.**

SKILL ANALYZER combines ten analytical specialists with five cross-skill engines for decision intelligence, human impact and governance, benchmark/regression assurance, knowledge and method intelligence, and failure intelligence/reconstruction (FIRE).

## What changed in 1.0.0

- Preserves the ten analytical specialists and five shared engines.
- Establishes `skills/` as the canonical Agent Skills source tree.
- Adds compatibility profiles for OpenAI/Codex, Claude Code, GitHub Copilot, Gemini CLI, VS Code, and Cursor.
- Adds an exporter for target-specific skill discovery paths.
- Adds manifest/frontmatter/reference/schema static validation and GitHub Actions CI.
- Explicitly separates portable instructions from host-specific tools, subagents, persistence, and enforcement.

## Core architecture

The master orchestrator routes to ten analytical responsibilities: analytical-collector, analyzer, negative-collector, positive-converter, evidence-auditor, strategic-foresight, evaluator, komparator, comparative-analytic, and information-authenticator. Five engines provide shared procedures for decisions, human impact/governance, benchmark/regression, knowledge/method intelligence, and FIRE.

`platform-compatibility` is a distribution and maintenance utility. It is not an additional analytical specialist.

## Quick start

```bash
python scripts/validate_portability.py
python scripts/export_platforms.py --target all --output ./dist
```

See [PORTABILITY.md](PORTABILITY.md) for supported profiles, installation locations, and capability boundaries.

## Reliability boundary

A valid package or passing static CI job does not prove that a particular model selects a skill, follows its workflow, executes a subagent, has the required tools, or produces correct conclusions. Platform-specific behavior must be tested separately and recorded with the exact host, model/provider, version, surface, and evidence.
