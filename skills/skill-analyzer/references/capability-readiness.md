# CAPABILITY READINESS & PREFLIGHT GATE

## Purpose

Capability Readiness prevents SKILL ANALYZER from promising or recording an operation before the required tool, access, artifact, provider, environment, and permission have been checked. It is a preflight protocol, not a tool installer and not a source of hidden host telemetry.

## 1. When required

Run preflight before any material action that depends on an external or local capability, including plugin packaging/update, file mutation, test execution, network/source inspection, code execution, runtime capture, decompilation, database access, or host-level verification. Pure reasoning that does not need an external capability does not require an artificial tool check.

## 2. Readiness dimensions

For every required capability, inspect only what the environment actually exposes:
- exact tool/provider identity and operation name;
- availability in the current session and whether the required operation is in its schema;
- authorization/permission scope and target ownership;
- required input artifacts, file paths, source, and output destination;
- dependency chain and version/compatibility requirements;
- network/connectivity, quota/rate limits, expiry, and execution constraints when observable;
- data sensitivity, allowed handling, and side-effect risk;
- expected output/evidence and an approved fallback, if one exists.

Never request, display, or write credentials, API tokens, cookies, or secrets into a readiness record. Record only whether authorized access was available and the scope needed.

## 3. Readiness status

Use one status per capability:
- `READY`: all required checks passed for the requested operation.
- `READY_WITH_LIMITATIONS`: operation can proceed only within named limits; the final output must preserve those limits.
- `BLOCKED`: a required dependency, input, permission, or verification is absent.
- `UNAVAILABLE`: the capability is not exposed in the current environment.
- `ACCESS_DENIED`: the provider/tool refused the required access.
- `NOT_CHECKED`: no inspection was performed; never represent this as ready.
- `EXPIRED`: an authorization, URL, session, or artifact reference expired.
- `NOT_APPLICABLE`: the task does not require the capability.

Do not collapse `BLOCKED`, `UNAVAILABLE`, `ACCESS_DENIED`, `NOT_CHECKED`, or `EXPIRED` into a successful execution status.

## 4. Capability record

`CAP-ID | requested operation | tool/provider | requirement | readiness status | evidence/diagnostic | scope/limits | checked_at | fallback | next action`.

For repeatable work, include plugin version, release ID, environment identifier, and test/run ID. Readiness is time-bounded: re-check immediately before execution if permissions, presigned URLs, quotas, versions, or source release could have changed.

## 5. Decision rules

1. If a required operation is `READY`, execute only within the verified scope.
2. If `READY_WITH_LIMITATIONS`, proceed only when the task can be safely narrowed and the limitation is disclosed.
3. If a required operation is `BLOCKED`, `UNAVAILABLE`, `ACCESS_DENIED`, `NOT_CHECKED`, or `EXPIRED`, mark that operation blocked and do not claim it was executed.
4. A fallback is valid only if it is independently available, authorized, functionally adequate, and does not bypass the original control or permission boundary.
5. If no safe fallback exists, stop that branch and continue only with separable tasks that do not depend on it.
6. Distinguish model reasoning capability from host tool capability. A model's ability to describe a test does not mean it executed the test.

## 6. Output — Capability Readiness Report

Report required capabilities, readiness status, checked scope, unavailable dependencies, approved fallback, blocked actions, and claims that must not be made. Do not expose secrets or unnecessary personal data.

## 7. Safety and stop conditions

Do not probe unauthorized systems, circumvent access controls, bypass quota restrictions, or use an alternate executor merely to evade a denied/limited capability. Do not claim sandboxing unless a verified sandbox exists. Stop before destructive, irreversible, or externally consequential action unless the scope, authorization, backup/rollback, and stop criteria are established.
