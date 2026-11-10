# KNOWLEDGE & METHOD INTELLIGENCE REPOSITORY

## Repository purpose

A structured, versioned catalogue for reusable methods, frameworks, tools, evaluation designs, decision techniques, and analytical patterns. This file defines the record schema and governance. It is not itself a complete encyclopedia and does not imply a live database or automatic learning.

## Method record schema

Use one record per method, with a stable `MTH-ID`:
- Canonical name and aliases.
- Method family and type: empirical method, analytical framework, operational tool, heuristic, evaluation design, decision model, or experimental synthesis.
- Status: established, professionally used, conceptual, heuristic, adapted/experimental, contested, or unverified.
- Core question and intended use.
- Suitable domain, level, unit of analysis, time horizon.
- Required data/input and minimum competence/resources.
- Procedure and expected output.
- Assumptions and applicability conditions.
- Validity boundary and known limitations.
- Common misuse and failure modes.
- Evidence supporting the method's validity/usefulness, including provenance.
- Complementary methods and methods that may conflict or duplicate.
- Effort/cost and implementation considerations.
- Source register, review date, version, editor note, and change history.

## Classification rules

Do not confuse:
- a named framework with a validated empirical method;
- a workshop tool with a causal identification design;
- a heuristic with a predictive model;
- a composite workflow invented for one project with a recognized standard;
- popularity with demonstrated validity.

Record the epistemic status and evidence for each method. Do not claim "scientifically proven" without evidence tied to the exact use and context.

## Selection and composition

A method should be selected only if it:
1. answers a necessary analytical question;
2. has inputs that can realistically be obtained;
3. adds perspective or validation not already supplied;
4. has assumptions compatible with the case or explicitly testable;
5. offers decision value proportional to cost and effort.

When combining methods, record their sequence, dependencies, complementary function, overlaps, contradictory assumptions, and integration risks. Do not create an arbitrary mega-framework just to make the analysis look sophisticated.

## Quality and update governance

- Preserve provenance of method descriptions and any claimed validation.
- Record source date, edition/version, and jurisdiction/domain when relevant.
- Review high-impact or fast-changing methods when an actual research/update opportunity exists.
- Mark records as needing review when evidence is outdated, conflicting, or unavailable.
- Keep deprecated methods with warnings if they remain historically relevant.
- Every revision should have a version/change note and a reason.
- Do not represent a model-generated suggestion as a verified repository entry until sources and applicability are checked.

## Existing catalogue integration

Use the plugin's existing `references/method-selection-guide.md` as the initial method catalogue. Do not silently replace its entries. Add or revise records only with clear provenance and applicability notes. If a candidate method is absent, describe it as a candidate pending review rather than claiming the repository is exhaustive.

## Repository search report

When the repository informs a task, state:
- which method families/records were consulted;
- which method was selected and why;
- which alternatives were rejected and why;
- whether entries were current or flagged for review;
- which gaps require external research or expert input.

## Non-goals

The repository does not automatically learn from conversation, does not guarantee complete coverage, does not independently update itself, and does not make every stored method appropriate for every problem.
