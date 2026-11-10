# FIRE CONTROL PLANE — FAILURE INTELLIGENCE & RECONSTRUCTION

## Purpose

FIRE is the common control plane for failure events, unknowns, reconstruction, and closure across all SKILL ANALYZER specialists. It provides a consistent protocol; it does not create hidden host telemetry, a database, or technical enforcement by itself.

## 1. Operating modes

- **Manual intake:** user supplies an error, failed test, transcript, screenshot, log, or description. Store only sanitized evidence references available in the current work artifact.
- **Test-integrated intake:** a local/CI runner emits structured failure events and artifacts. The runner must preserve stdout, stderr, exit code, environment, and artifact references separately.
- **Runtime-integrated intake:** host instrumentation records route decisions, engine activations, gate transitions, and release decisions. This mode requires a real telemetry source and authorization; do not infer it from prompt output.

Always state which mode is operating. Missing logs are a coverage gap, not proof of no failure.

## 2. Severity and triage

- **P0 Critical:** safety/security/privacy breach, gate bypass, evidence fabrication, destructive data loss, or failure that invalidates a core release guarantee. Contain immediately; block release.
- **P1 Material:** wrong primary route, required engine omission, incorrect material conclusion, broken reconstruction, or release integrity risk. HOLD by default.
- **P2 Moderate:** supporting function or reporting inconsistency with bounded impact. Fix or release only with visible caveat if no blocker is affected.
- **P3 Minor:** cosmetic or low-impact issue. Track and prioritize proportionally.

Severity is not a probability score. Explain impact and conditions. A high-uncertainty high-impact event remains subject to containment.

## 3. Reproduction protocol

Record exact sanitized input, product/plugin version, release ID, environment/host, relevant settings, preconditions, steps, expected behavior, observed behavior, evidence, and reproduction attempts. Distinguish:
- `REPRODUCED`: same material failure observed under recorded conditions;
- `NOT_REPRODUCIBLE`: attempts fail to recreate it, with attempts and environment documented;
- `BLOCKED`: required access/tool/data unavailable;
- `INSUFFICIENT_DATA`: incident report lacks reproducible conditions.

Do not turn `NOT_REPRODUCIBLE` into `FALSE_REPORT`. Preserve source and uncertainty.

## 4. RCA protocol

For each incident, identify:
1. Direct cause: immediate mechanism producing the failure.
2. Contributing factors: conditions increasing likelihood or severity.
3. Latent/systemic cause: design, governance, process, environment, or dependency that allowed the failure.
4. Detection gap: why existing checks did not detect/prevent it.
5. Test-oracle issue: whether expected behavior itself was wrong or underspecified.
6. Alternative hypotheses and disconfirming tests.

Use 5 Whys, Fishbone, FMEA, Fault Tree, Bow-tie, timeline/process tracing, causal graph, or counterfactual tests as appropriate. Do not force a single root cause if multiple causal paths remain plausible. Mark RCA as hypothesis, partial, confirmed, or inconclusive.

## 5. Evidence and trace controls

Link each material incident claim to evidence registry entries. Build trace nodes for the incident, environment, artifacts, observations, hypotheses, controls, tests, and release. Keep observed facts separate from inferred edges. Evidence without locator/provenance is lower-confidence and cannot silently support a critical claim.

## 6. Reconstruction protocol

Create a reconstruction packet before implementation. Specify baseline and candidate, expected vs observed behavior, affected components, evidence basis, proposed changes, dependencies, side effects, rollback, acceptance criteria, and tests. After implementation, capture actual results. If the candidate differs from baseline in multiple dimensions, isolate changes or disclose confounding changes.

A reconstruction is `VERIFIED` only when:
- all critical acceptance criteria pass;
- negative/boundary cases show the failure is not merely moved elsewhere;
- relevant regression tests pass;
- evidence references are stored;
- Gate 2 accepts the claims;
- no P0/P1 blocker remains.

Retest evidence must include the test ID, case version, actual output, status, environment, and evidence reference. A retest that was not executed remains `NOT RUN` or `BLOCKED`.

## 7. Closure and recurrence

`CLOSED` requires closure evidence. `ACCEPTED_LIMITATION` requires authorized risk acceptance and review conditions. Reoccurrence links to prior incidents, compares environment/version, and tests whether the prior RCA or prevention was incomplete. Preserve all occurrences; deduplicate only the shared root-cause grouping.

## 8. Change governance

For each update, record change ID, source version/release, target version, files changed, manifest diff, defaultPrompt preservation check, sub-skill inventory diff, references diff, package validation, test results, upload result, read-back result, skill registry result, host tests, and rollback pointer. Package/source success is separate from host behavior success.

## 9. Output report

A FIRE report contains: scope and intake mode; incident/defect list; severity and impact; reproduction status; RCA evidence and alternatives; containment; reconstruction packets; corrective/preventive actions; tests and observed results; residual unknowns; release disposition; closure status; recurrence monitoring; and limitations.


## 10. Capability readiness and execution preflight

Before reproduction, experiments, package operations, tool calls, or runtime verification, use `capability-readiness.md`. Record exact operation, provider, authorization scope, required artifacts, environment, limitations, and status. If required capability is blocked/unavailable/access-denied/not-checked/expired, mark the operation blocked; do not route around the restriction. Re-check time-sensitive permissions and artifacts at execution time.

## 11. Controlled experiment and reproducibility

Use `controlled-experiment.md` to set target authorization, baseline/candidate, independent variable, controls, confounders, expected behavior, acceptance criteria, repetition, stopping rules, execution bounds, side effects, rollback, and evidence capture. Preserve stdout, stderr, exit code, tool errors, runner errors, and product failures as separate facts. Never assume a process capture tool is a sandbox.

## 12. Change impact and version differential

Use `change-impact-analysis.md` for every material update. Compare identity/release, manifests, default prompts, files, skills, references, schemas, routing, engine triggers, gate states, output contracts, dependencies, and preserved behavior. Map changed nodes to dependent components and tests. Distinguish additive, behavioral, breaking, metadata, dependency, reference, removal, preserved, and unknown changes. Verify overlay/deletion semantics and read back the effective source after update.

## 13. Evaluation-to-Implementation Assurance

Every accepted recommendation that requires action must be converted into a `REQ-ID` with trace links, scope/non-goals, acceptance criteria, verification tests, dependencies, owner/authority where known, readiness, risk, rollback, and closure requirements. Preserve deferred/rejected proposals and rationale. Do not close an implementation because a file was edited or a package was uploaded. Required progression is specified in `evaluation-to-implementation.md`.

## 14. Postmortem and learning review

For material or recurring failures, produce a postmortem that distinguishes timeline, impact, direct cause, contributing factors, systemic cause, detection gap, oracle issue, hypotheses rejected, controls that failed, successful controls, residual risk, owner/actions, and recurrence signals. Avoid blame-based conclusions. Convert every accepted preventive action to a requirement and regression case. If a defect recurs, create a new occurrence linked to the parent; do not overwrite its history.

## 15. Persistence boundary

FIRE schemas and packaged Markdown define data contracts; they are not a live database, event bus, telemetry source, or persistent cross-conversation memory. If no external store is connected, the active report/artifact is the record for that task and must be explicitly saved by an available workflow. Report retention and backup as `NOT AVAILABLE` unless actually provided.
