# CONTROLLED EXPERIMENT & REPRODUCIBILITY PROTOCOL

## Purpose

A controlled experiment isolates a proposed cause or change and records what actually happened. Use it for reproducing failures, verifying fixes, testing workflows, and comparing baseline/candidate behavior. It does not assume that a local process, REA capture, container, or tool is automatically a sandbox.

## 1. Authorization and target scope

Before execution, record target ownership/authority, permitted operations, data scope, read/write/network access, process scope, and external side effects. Do not test an unauthorized target or broaden scope during execution. If scope or permission is unclear, mark `BLOCKED`.

## 2. Preflight

Run Capability Readiness. Confirm tool/provider availability, inputs, dependencies, environment, version, permissions, output path, and data sensitivity. Re-check expiring URLs/tokens/permissions immediately before execution without recording secret values.

## 3. Experiment design

Record:
- `EXP-ID`, question/hypothesis, baseline and candidate identifiers;
- independent variable/change under test and dependent observations;
- held-constant factors and known confounders;
- control/baseline condition and comparison condition;
- expected result and test oracle rationale;
- sample/repetition plan and stopping rule;
- acceptance threshold and uncertainty;
- allowed side effects and rollback/recovery procedure.

Change one material factor at a time where feasible. If several changes must be bundled, document the confounding and avoid attributing effects to one change.

## 4. Execution bounds

Where the execution environment supports them, set and record timeout, process count, CPU/memory limits, filesystem scope, network scope, and output size limits. Use read-only/dry-run mode first when possible. Snapshot relevant state before mutation. Do not describe a process as sandboxed unless isolation was actually verified.

Prohibit destructive, irreversible, privacy-invasive, or externally consequential tests unless explicitly authorized, necessary, and protected by a safe plan. Stop if scope expands, an unexpected side effect occurs, resource limits are exceeded, or a safety boundary is crossed.

## 5. Evidence capture

Capture separately: exact sanitized input, tool/provider and version, start/end time, stdout, stderr, exit code, structured output, relevant files/observations, environment, errors, and evidence locators. Preserve failed and partial runs. Do not merge tool error, runner error, and product failure into one status.

## 6. Reproducibility and comparison

Repeat enough times to distinguish stable behavior from intermittent behavior when the risk warrants it. Compare baseline and candidate under materially equivalent conditions. Identify environmental drift, dependency changes, data differences, or missing observations. Use statuses `REPRODUCED`, `NOT_REPRODUCIBLE`, `INTERMITTENT`, `BLOCKED`, `INCOMPLETE`, and `INVALID_EXPERIMENT`.

## 7. Reporting

Report hypothesis, design, authorization, preflight, controls, actual execution, outputs, deviations, side effects, comparison, result, limitations, evidence references, and whether the result supports, contradicts, or leaves the hypothesis unresolved.
