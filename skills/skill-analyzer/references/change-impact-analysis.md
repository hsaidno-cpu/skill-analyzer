# CHANGE IMPACT & VERSION DIFFERENTIAL ANALYSIS

## Purpose

This protocol identifies what changed between a baseline and candidate, why it changed, which components may be affected, and which tests must be rerun. It applies to plugins, skills, prompts, policies, workflows, documents, and technical systems. A version number or ZIP hash alone is not a semantic change analysis.

## 1. Baseline and candidate identity

Record for both sides, when available: product/plugin ID, version, release ID, source revision, environment, configuration, manifest, file inventory, skill/provider inventory, and capture timestamp. Verify that the baseline and candidate are the intended artifacts. If one side is unavailable, report a partial comparison rather than inventing a diff.

## 2. Difference classes

Classify each observed change:
- `ADDITIVE`: new file, field, capability, or test without changing existing contract;
- `BEHAVIORAL`: routing, trigger, engine, gate, workflow, or output behavior changed;
- `BREAKING`: compatibility, field, path, status, interface, or expected behavior changed incompatibly;
- `METADATA`: version, description, keywords, author/presentation metadata;
- `DEPENDENCY`: provider, tool, schema, permission, or version dependency changed;
- `REFERENCE`: file path, schema, skill link, or cross-reference changed;
- `REMOVAL`: file or capability removed, with explicit justification;
- `PRESERVED`: intentionally unchanged content or behavior checked against a baseline;
- `UNKNOWN`: comparison could not establish the nature or impact of a difference.

## 3. Change inventory

Compare:
1. Manifest semantics: schema, name/identity, version, description, author, keywords, extensions, defaultPrompt type/order/text, skills path, audience/scope.
2. Files: additions, modifications, removals, file sizes, hashes if actually computed, encoding, path and casing.
3. Skill registry: identifiers, frontmatter, descriptions, aliases, links, dependencies, and preservation of unchanged skills.
4. Cross-file references: target existence, schema links, local paths, and renamed/moved components.
5. Behavior contract: router precedence, specialist ownership, engine triggers and anti-triggers, gates, output contract, stop conditions.
6. Data contracts: schema changes, required fields, enum/status migration, backward compatibility, and sample validity.
7. Tests: added, removed, changed, skipped, blocked, and impact-selected test cases.

## 4. Dependency and impact propagation

For each changed node, follow its references/dependencies through the Trace Graph. Produce `CHG-ID → changed components → dependent components → affected requirements → required tests → release risk`. Do not infer dependency merely from similar names. Mark unknown dependencies explicitly.

## 5. Test selection

Run:
- mandatory smoke tests for every release;
- all direct tests for changed components;
- transitive dependency tests where evidence shows an impact path;
- preserved golden cases for unchanged critical behavior;
- negative and boundary cases for changed triggers/statuses;
- mutation tests for changed controls;
- package/manifest/read-back and host tests appropriate to the change.

A reduction in test scope requires a written risk rationale and authority. Do not claim full regression when only impacted tests were run.

## 6. Preservation and overlay safety

For overlay updates, compare the candidate archive's paths with the current inventory. Confirm every intended changed file is included, every retained file is intentionally omitted, and every removal is listed by exact path in the deletion request. Do not delete a compatibility/generated manifest when its source still regenerates it. Verify effective configuration after update by read-back.

Hashes prove byte equality only when actually computed. Equal file size does not prove equality; omitted overlay files are preserved by host overlay semantics only if the update operation behaves as documented and is verified after save.

## 7. Release impact report

Include baseline/candidate identity; change list and classification; preservation diff; dependency/impact graph; test selection rationale; results by evidence layer; open P0/P1; rollback pointer; release disposition; and limitations.
