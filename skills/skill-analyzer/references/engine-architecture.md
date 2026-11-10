# FIVE CROSS-SKILL ENGINES — OPERATIONAL SPECIFICATION 0.9.0

Engines are conditional procedures embedded in the SKILL ANALYZER master, not automatically autonomous agents. They must produce the required artifact when activated. A statement that an engine is active is not evidence that its procedure ran.

## 1. Decision Intelligence Engine

**Trigger:** material decision, multiple options, prioritization, resource allocation, strategy selection, irreversible action, or decision under uncertainty.

**Decision packet:** decision ID and deadline; owner/authority; affected parties; objectives and constraints; options including status quo, defer, pilot, hybrid, exit/no action; criteria; evidence, assumptions and unknowns; trade-offs; sensitivity; value of information; decision rule; trigger, contingency and stop condition.

**Controls:** no invented scores, weights, costs, probabilities, or expected values; no hidden normative priorities; human accountability remains with the authorized decision owner.

## 2. Human Impact, Ethics & Governance Engine

**Trigger:** people/groups may be affected; rights, safety, privacy, access, livelihoods, public services, power relations, environment, or cultural impacts are material.

**Assessment:** stakeholder map; direct/indirect and short/long-term impacts; distribution of benefits and burdens; rights and safety; procedural/distributive fairness; accessibility; consent; transparency; conflicts of interest; accountable owner; oversight; human review; appeals, complaints, remedies, and incident response.

**Release rule:** severe non-compensable harms or rights conflicts are red lines. Aggregate benefit cannot automatically offset severe harm to a group. Require mitigation, redesign, oversight, or HOLD.

## 3. Benchmark & Regression Testing Engine

**Trigger:** plugin/skill/prompt/workflow/system audit or update; changed routing, architecture, rubric, output schema; reported recurring failure.

**Test layers:** static integrity; routing; engine activation and non-activation; functional specialist workflows; evidence/epistemic; logic/causality; human-impact/safety; regression; output contract; failure lifecycle; packaging; host behavior when observable.

**Test record:** `TST-ID | case | version | layer | setup/input | expected | observed | evidence | severity | status | defect | correction | retest`.

Separate `NOT RUN`, `BLOCKED`, `STATIC CHECK PASSED`, `CONTRACT TEST PASSED`, `HOST BEHAVIOR PASSED`, `RUNTIME TRACE PASSED`, `FAILED`, and `WAIVED WITH RATIONALE`. Do not infer internal router execution from skill catalog presence or answer style. A manual matrix is not an automated runner.

**Release controls:** P0 open blocks release. P1 open blocks by default; an eligible waiver must be explicit, authorized, time-bound, mitigated, and must not weaken evidence, authentication, safety, privacy, or integrity controls. Required tests not run or blocked do not pass.

## 4. Knowledge & Method Intelligence Engine

**Trigger:** method selection, multidisciplinary analysis, unfamiliar method, framework synthesis, deliberate repository maintenance.

**Method record:** canonical name/aliases; method family/type; status; core question; domain/unit; required inputs; procedure/output; assumptions; validity boundary; limitations and failure modes; validation evidence and provenance; complementary/conflicting methods; cost/skills; review date, version, and change history.

**Boundary:** packaged references are static, versioned knowledge, not a live database or self-updating memory. Do not claim repository changes unless a file/release update was saved.

## 5. Failure Intelligence & Reconstruction Engine (FIRE)

**Purpose:** cross-skill failure governance and evidence-based reconstruction. FIRE integrates with Analyzer, Negative Collector, Positive Converter, Evidence Auditor, Information Authenticator, Evaluator, and Benchmark Engine.

**Activation triggers:** observed failure, expected/actual mismatch, defect, anomalous output, failed/blocked test, tool/provider error, missing/truncated evidence, failed control, release problem, recurring issue, or reconstruction request.

### 5.1 Lifecycle

`DETECTED → TRIAGED → REPRODUCTION_PENDING → REPRODUCED / NOT_REPRODUCIBLE / BLOCKED / INSUFFICIENT_DATA → RCA_HYPOTHESIS / RCA_PARTIAL / RCA_CONFIRMED / RCA_INCONCLUSIVE → CONTAINED → FIX_DESIGNED → IMPLEMENTED → VERIFYING → VERIFIED → CLOSED`

A verified fix that later recurs is linked to its predecessor and re-opened or recorded as recurrence according to the incident policy. `ACCEPTED_LIMITATION` is a separate terminal decision requiring authorized rationale, impact, mitigation, and review trigger; it is not the same as `RESOLVED`.

### 5.2 Failure record

Minimum fields: incident ID; first/last observed time; source of report; plugin/build/release version; environment; sanitized input reference; expected behavior; observed behavior; category; severity; impact; evidence references; reproduction steps and status; direct cause; contributing factors; systemic cause; competing hypotheses; containment; corrective action; preventive control; retest IDs/results; residual unknowns; owner/role if known; release disposition; closure evidence; recurrence links.

Categories: `ROUTE`, `ENGINE`, `AUTH`, `EVIDENCE`, `LOGIC`, `OUTPUT`, `HARNESS`, `ORACLE`, `INTEGRATION`, `PACKAGE`, `PERSISTENCE`, `GOVERNANCE`, `ENVIRONMENT`.

### 5.3 Root-cause analysis

Separate direct cause, contributing factors, latent/systemic conditions, detection failure, and test-oracle failure. Use methods appropriate to the event: timeline reconstruction, 5 Whys, Fishbone, Fault Tree, FMEA, Bow-tie, process tracing, causal graph, counterfactual tests. A method output is a hypothesis until supported by evidence. Preserve competing hypotheses and disconfirming tests.

### 5.4 Reconstruction packet

Each material reconstruction must specify:
- target and baseline version/state;
- intended behavior and observed behavior;
- evidence and scope used to infer behavior;
- difference/gap and competing explanations;
- proposed change and affected dependencies;
- risks, side effects, rollback/recovery;
- acceptance criteria;
- positive, negative, boundary, mutation, and regression tests;
- actual results, environment and evidence;
- residual unknowns and final disposition.

Implementation is not verification. A test not run is not passed. If the environment is unavailable, mark `BLOCKED` and keep the claim open.

### 5.5 Closure rule

Close only when the cause is corrected or an authorized limitation is accepted; corrective action is present; prevention/detection control is present where needed; relevant positive/negative/regression tests pass; evidence is linked; unknowns have valid dispositions; and Information Authenticator passes Gate 2. No defect is closed solely because an explanatory note was written.

### 5.6 Data and privacy safeguards

Capture only the minimum information needed. Sanitize prompts, credentials, API keys, tokens, personal data, and customer content. Do not store hidden chain-of-thought. Record observable events, concise rationale, artifacts, and test evidence. A file-based register is only as persistent as its storage location and backup policy; do not represent it as live telemetry.

### 5.7 FIRE operating boundary

FIRE in this plugin specifies governance, schemas, workflows, and acceptance rules. Persistent incident storage, automatic event capture, host routing traces, CI execution, and hard release blocking require external tools/services. If these are unavailable, use manual evidence intake and state the coverage limitation. Never invent tool output or automatic monitoring.


## 6. Cross-engine assurance protocols

The following protocols are shared controls, not new autonomous agents:
- **Capability Readiness:** preflight of tools, providers, permissions, artifacts, versions, environment, and constraints before a dependent action.
- **Change Impact Analysis:** baseline/candidate comparison, dependency impact propagation, preservation checks, and test selection.
- **Controlled Experiment:** authorized, bounded, reproducible comparison with explicit side-effect and rollback controls.
- **Evaluation-to-Implementation Assurance:** accepted recommendation → requirement → implementation → verification → release/read-back → closure.

These protocols are defined in `capability-readiness.md`, `change-impact-analysis.md`, `controlled-experiment.md`, and `evaluation-to-implementation.md`. Each must emit its required record when invoked. A protocol reference is not proof that an external tool, database, sandbox, or host service exists.
