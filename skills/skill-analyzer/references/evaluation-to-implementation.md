# EVALUATION-TO-IMPLEMENTATION ASSURANCE PROTOCOL (E2I)

## Purpose

E2I converts accepted findings and recommendations into controlled, traceable implementation work. It closes the gap between “a good suggestion was written” and “a change was approved, implemented, verified, read back, and released.” It coordinates Positive Converter, Evaluator, Benchmark & Regression, FIRE, and Information Authenticator without claiming that any external tool was called when it was not.

## 1. Admission rule

Only an explicit user-approved or authorized recommendation may enter implementation. Unaccepted suggestions remain `PROPOSED`; they must not silently become requirements. Classify each recommendation as `ACCEPTED`, `DEFERRED`, `REJECTED`, or `NEEDS_DECISION`, with rationale and decision authority where known.

## 2. Requirement conversion

For every accepted recommendation, create a stable `REQ-ID` and record:
- originating `REC-ID`, `FND-ID`, `RSK-ID`, `EVD-ID`, `UNK-ID`, and relevant trace edges;
- problem statement and intended outcome;
- scope, non-goals, affected users/systems, and constraints;
- measurable acceptance criteria, including negative/boundary behavior;
- verification method, test IDs, and required evidence;
- dependencies, owner role, authority, resources, and schedule when known;
- risks, privacy/safety controls, rollback/stop criteria, and unresolved decisions.

Do not invent an owner, budget, timeline, baseline, or acceptance threshold. Record missing inputs as implementation unknowns with impact and decision owner.

## 3. Implementation lifecycle

`PROPOSED → ACCEPTED → REQUIREMENT_DEFINED → READY_FOR_IMPLEMENTATION → IMPLEMENTING → IMPLEMENTED → VERIFICATION_PENDING → VERIFIED → RELEASE_APPROVED → RELEASED → READ_BACK_CONFIRMED → CLOSED`.

Alternative outcomes: `DEFERRED`, `REJECTED`, `BLOCKED`, `FAILED`, `ROLLED_BACK`, `ACCEPTED_LIMITATION`. A transition requires its evidence. `IMPLEMENTED` is not `VERIFIED`; `VERIFIED` is not `RELEASED`; `RELEASED` is not `READ_BACK_CONFIRMED`.

## 4. Readiness and design

Before implementation, run Capability Readiness. Establish the baseline and candidate, change impact, data handling, dependencies, migration needs, controlled experiment/pilot approach, tests, and rollback. For plugin updates, verify exact plugin ID, scope, current release ID, manifest semantics, defaultPrompt preservation, file inventory, and archive layout.

## 5. Verification contract

Every accepted requirement needs:
- at least one positive acceptance test;
- relevant negative, boundary, and regression tests;
- test-oracle rationale and reviewer/authority where known;
- observed output, status, environment, timestamp, and evidence reference;
- residual unknowns and limitations;
- Gate 2 disposition for material factual or release claims.

A test not run, blocked, truncated, unsupported, or lacking evidence cannot satisfy acceptance. If the test oracle is disputed, resolve the oracle before using the test result to approve implementation.

## 6. Release and read-back

For release work, record package validation, manifest and inventory diff, upload result, returned release ID, source read-back, file references, skill registry, host behavior tests, and rollback pointer. A successful upload proves that the host accepted a package; it does not alone prove runtime behavior. State each evidence layer separately.

## 7. Closure

Close a requirement only when acceptance criteria pass, required evidence is attached, dependencies and unknowns have a disposition, Gate 2 is acceptable, and read-back/release evidence exists when applicable. Preserve deferred/rejected requirements and reasons. Reopen when regression or recurrence evidence appears.

## 8. Output — Implementation Assurance Ledger

`REQ-ID | REC-ID | decision | acceptance criteria | owner/dependencies | readiness | change ID | tests | observed results | evidence | gate disposition | release/read-back | state`.

E2I is a control protocol. Persistent requirement tracking requires a real repository or project-management store; a packaged template is not a live task database.
