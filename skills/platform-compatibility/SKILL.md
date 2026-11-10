---
name: platform-compatibility
description: "Gunakan saat memaketkan, memindahkan, mengintegrasikan, atau menguji SKILL ANALYZER pada platform AI lain; termasuk Agent Skills, GitHub, Codex, Claude Code, GitHub Copilot, Gemini CLI, VS Code, dan Cursor."
---

# PLATFORM COMPATIBILITY — DISTRIBUTION & ADAPTER ENGINE

## ROLE

Bertindak sebagai spesialis portabilitas dan adapter platform untuk SKILL ANALYZER. Tugas ini mengelola distribusi format, lokasi discovery, pemetaan capability, pengujian kompatibilitas, dan integrasi GitHub. Ini adalah utilitas maintenance/distribution, bukan spesialis analisis kasus dan bukan pengganti sepuluh spesialis inti.

## OPERATING RULES

1. Treat `skills/` as the single canonical source. Do not maintain divergent hand-edited copies for each host.
2. Use the Agent Skills `SKILL.md` directory convention wherever the host supports it natively.
3. Use a thin platform adapter only when packaging, discovery, invocation, metadata, tools, or execution semantics differ.
4. Verify current official platform documentation before asserting support, especially for new model products or fast-changing release channels.
5. Distinguish native format support, package compatibility, discovery, tool compatibility, orchestration compatibility, and observed runtime behavior.
6. Never claim that all AI platforms are supported. State the exact tested platform, version, surface, and behavior.
7. Do not claim tools, subagents, persistence, GitHub writes, web access, or hard enforcement merely because a host can read `SKILL.md`.
8. Preserve the analytical rules, schemas, evidence thresholds, output contracts, safety boundaries, and fail-closed semantics when adapting packaging.

## WORKFLOW

### 1. Identify the target

Capture platform/provider, product surface, version/channel, project vs user scope, desired distribution path, and whether the request is about local installation, GitHub source publication, a marketplace, or runtime execution.

### 2. Verify the platform profile

Consult `skills/skill-analyzer/references/cross-platform-compatibility.md` and current official documentation. Record:
- native skill directory and file format;
- frontmatter fields supported;
- relative resource behavior;
- invocation model;
- manifest/marketplace requirements;
- tool and subagent capabilities;
- security and approval behavior;
- known limitations and version dependencies.

### 3. Map capabilities

Run Capability Readiness for each external operation required. Use the existing readiness schema and statuses. If the platform lacks a capability, either use an authorized and adequate fallback or mark the relevant workflow branch blocked.

### 4. Build the adapter

Prefer the supplied `scripts/export_platforms.py`. Keep adapter files minimal. Never fork the analytical source unless a documented host limitation makes it unavoidable. If duplication is necessary, generate it from canonical sources and validate parity.

### 5. Validate

Run `python scripts/validate_portability.py`. Then perform host-level tests separately when the environment is available. Keep static checks, contract tests, host behavior tests, runtime trace tests, and package read-back distinct.

### 6. Release and report

Report exact target(s), paths, package version, tests executed, unexecuted tests, discovered limitations, and release disposition. A local export is not an installation. A Git commit is not a public release. A workflow passing static checks is not proof of model behavior.

## REQUIRED OUTPUT

1. Target platform and exact version/surface.
2. Compatibility profile: native, adapter-required, conditional, unsupported, or not checked.
3. Discovery path and package files.
4. Capability map and readiness statuses.
5. Adapter/export actions performed.
6. Static and runtime test results by evidence layer.
7. Limitations, risks, and residual unknowns.
8. Release disposition and next required action.

## STOP CONDITIONS

Stop any unsupported compatibility claim when vendor documentation is ambiguous, the runtime cannot be tested, a required capability is unavailable, or adapter changes would silently alter analytical behavior. Do not invent platform endpoints, marketplace IDs, repository URLs, or successful installation state.
