# BENCHMARK, REGRESSION & IMPLEMENTATION-ASSURANCE SUITE 0.9.0

## Purpose and evidence boundary

The machine-readable test contract is `tests/evidence-control-contract.json` and defines **70 required scenarios** across routing, engine selection, authentication, evidence, FIRE, reconstruction, readiness, change impact, experiments, implementation assurance, and test governance. It defines expected behavior; it is not an execution log.

The dependency-aware contract runner is `tests/test_evidence_control_contract.py`. Its test count measures checks of the package contract, schemas, reference integrity, mutation-detection logic, and preservation rules. It does not execute the 70 host scenarios. Use `tests/test-execution-ledger.template.json` to record each actual run; never change `NOT_RUN` to PASS without observed behavior and evidence.

## Evidence layers

Keep these result types separate:
- `STATIC_CHECK_PASSED`: files, manifests, paths, and source structure inspected.
- `CONTRACT_TEST_PASSED`: deterministic declarations and data invariants validated.
- `HARNESS_TEST_PASSED`: the runner itself and test oracles behaved as specified.
- `HOST_BEHAVIOR_PASSED`: observed ChatGPT host response meets a case's expected behavior.
- `RUNTIME_TRACE_PASSED`: internal routing/engine/gate transition is observed through actual instrumentation.
- `PACKAGE_READBACK_PASSED`: uploaded release and effective source were read back and checked.

A lower evidence layer cannot be promoted to a higher one. Skill registry presence is not proof of router selection. Output style is not internal routing trace.

## Coverage set — 70 required scenarios

| Group | Range | Count | Focus |
|---|---:|---:|---|
| R | R01–R15 | 15 | Router precedence, specialist choice, and narrow creative exemption |
| E | E01–E08 | 8 | Engine activation and non-activation |
| G | G01–G12 | 12 | Gate bypass, evidence status, privacy, and fail-closed |
| F | F01–F10 | 10 | FIRE lifecycle, unknowns, trace graph, reconstruction, recurrence |
| C | C01–C05 | 5 | Capability readiness, permission, provider and fallback |
| D | D01–D05 | 5 | Baseline/candidate change impact, references, tests, rollback |
| X | X01–X05 | 5 | Authorized controlled experiments, reproducibility, side effects |
| I | I01–I05 | 5 | Evaluation-to-implementation assurance |
| T | T01–T05 | 5 | Mutation, oracle quality, schema-instance and evidence-layer controls |

Full prompt/scenario, expected route, expected engine, required artifacts, and oracle rationale are held in the JSON contract.

## Test record

Every actual execution record contains run ID, case ID, plugin version/release, environment, test layer, status, timestamp, observed behavior, evidence references, severity, defect ID, and waiver if applicable. Allowed statuses are defined in `tests/test-execution-record.schema.json`. `NOT_RUN`, `BLOCKED`, `FAILED`, and `WAIVED_WITH_RATIONALE` are not PASS.

## Test quality controls

- Review the test oracle independently from the implementation; a bad expected result is an oracle defect.
- Run mutation checks against critical gate, route, readiness, and lifecycle assertions.
- Validate JSON Schema documents and representative valid/invalid instances.
- Validate graph node/edge references; JSON Schema alone cannot enforce every cross-record constraint.
- Preserve positive, negative, ambiguous, boundary, regression, and adversarial tests.
- Report test selection rationale and any tests not run, blocked, or waived.

## Release disposition

- **PASS:** all required layers for the release were actually executed; required cases have evidence; no open P0/P1; all required gates pass; material unknowns are dispositioned; reconstruction and read-back claims are verified.
- **PASS WITH CAVEATS:** no P0/P1 blocker; only authorized, time-bounded non-blocking limitations remain with mitigation, review trigger, and residual risk.
- **HOLD:** required tests not run/blocked, coverage incomplete, unknowns unresolved, capability readiness unverified, change impact incomplete, P0/P1 open, or read-back/host evidence required but unavailable.
- **FAIL:** critical contract, safety, integrity, authentication, evidence, or preservation control is violated.

## Required report

Report contract cases defined, contract tests run, mutation tests run/caught, schema instance validations, host scenarios run/passed/failed/blocked/not run, runtime traces available, package read-back, source preservation, open defects, residual unknowns, limitations, and final release disposition. Do not compress evidence layers into one pass percentage.
