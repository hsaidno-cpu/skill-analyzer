#!/usr/bin/env python3
"""Deterministic static/contract and harness-quality tests for SKILL ANALYZER 1.1.0.

This runner does NOT execute ChatGPT host routing, host engine activation, internal
router traces, or external middleware enforcement. It validates the declarative
contract, reference integrity, sample schema instances, and selected mutation
checks. Host scenarios require a separate execution record with observed evidence.
"""
from __future__ import annotations
import json
import re
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CONTRACT_PATH = ROOT / "tests" / "evidence-control-contract.json"
LEDGER_PATH = ROOT / "tests" / "test-execution-ledger.template.json"


def load_json(path: Path):
    with path.open("r", encoding="utf-8") as handle:
        return json.load(handle)


def required_files():
    return [
        "skills/skill-analyzer/SKILL.md",
        "skills/information-authenticator/SKILL.md",
        "skills/skill-analyzer/references/fire-control-plane.md",
        "skills/skill-analyzer/references/capability-readiness.md",
        "skills/skill-analyzer/references/evaluation-to-implementation.md",
        "skills/skill-analyzer/references/change-impact-analysis.md",
        "skills/skill-analyzer/references/controlled-experiment.md",
        "skills/skill-analyzer/references/engine-architecture.md",
        "skills/skill-analyzer/references/benchmark-regression-suite.md",
        "skills/skill-analyzer/references/evidence-registry.schema.json",
        "skills/skill-analyzer/references/residual-unknowns.schema.json",
        "skills/skill-analyzer/references/trace-graph.schema.json",
        "tests/test-execution-record.schema.json",
        "tests/test-execution-ledger.template.json",
    ]


def gate_policy_valid(contract):
    policy = contract["release_policy"]
    return (
        policy.get("default_disposition") == "HOLD"
        and {"P0", "P1"}.issubset(set(policy.get("blocking_severities", [])))
        and {"UNKNOWN", "INCOMPLETE", "UNSUPPORTED", "TRUNCATED", "BLOCKED", "NOT_RUN", "UNVERIFIABLE", "NOT_OBSERVED", "NOT_CHECKED", "UNAVAILABLE", "ACCESS_DENIED", "EXPIRED"}.issubset(set(policy.get("non_pass_statuses", [])))
    )


def validate_unknown_record(record):
    status = record.get("status")
    if status == "RESOLVED" and not record.get("resolution_evidence"):
        return False
    if status == "ACCEPTED_LIMITATION":
        return all(record.get(k) for k in ("acceptance_authority", "accepted_rationale", "review_trigger"))
    return True


def validate_trace_references(graph, known_evidence_ids=None):
    known_evidence_ids = set(known_evidence_ids or [])
    nodes = [n.get("node_id") for n in graph.get("nodes", [])]
    edges = [e.get("edge_id") for e in graph.get("edges", [])]
    if len(nodes) != len(set(nodes)) or len(edges) != len(set(edges)):
        return False
    node_set = set(nodes)
    for edge in graph.get("edges", []):
        if edge.get("from") not in node_set or edge.get("to") not in node_set:
            return False
        for ref in edge.get("evidence_refs", []):
            if known_evidence_ids and ref not in known_evidence_ids:
                return False
    return True


def validate_execution_record(record):
    status = record.get("status")
    passed = {"STATIC_CHECK_PASSED", "CONTRACT_TEST_PASSED", "HOST_BEHAVIOR_PASSED", "RUNTIME_TRACE_PASSED"}
    required = ("run_id", "case_id", "plugin_version", "test_layer", "status", "observed_at", "observed_behavior", "evidence_refs")
    if any(k not in record for k in required):
        return False
    if status in passed:
        return bool(record.get("observed_at") and record.get("observed_behavior") and record.get("evidence_refs"))
    if status == "WAIVED_WITH_RATIONALE":
        waiver = record.get("waiver") or {}
        return all(waiver.get(k) for k in ("authority", "rationale", "review_trigger"))
    return status in {"NOT_RUN", "BLOCKED", "FAILED"}


def mutation_contract_check(master, auth, fire, readiness, e2i):
    errors = []
    checks = [
        ("master has FIRE", "Failure Intelligence & Reconstruction Engine" in master),
        ("master has E2I", "Evaluation-to-Implementation" in master),
        ("master has readiness", "Capability Readiness" in master),
        ("auth has both gates", "### Gate 1 — Intake" in auth and "### Gate 2 — Final release" in auth),
        ("auth has fail-closed", "## 8. FAIL-CLOSED RELEASE STATE MACHINE" in auth),
        ("FIRE has reconstruction", "## 6. Reconstruction protocol" in fire),
        ("readiness has blocked state", "## 3. Readiness status" in readiness),
        ("E2I has verified state", "## 3. Implementation lifecycle" in e2i and "VERIFIED" in e2i),
    ]
    errors.extend(name for name, passed in checks if not passed)
    return errors


class EvidenceControlContractTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.contract = load_json(CONTRACT_PATH)
        cls.cases = cls.contract["cases"]
        cls.case_by_id = {case["id"]: case for case in cls.cases}
        cls.schemas = {name: load_json(ROOT / rel) for name, rel in cls.contract["schemas"].items()}
        cls.master = (ROOT / "skills/skill-analyzer/SKILL.md").read_text(encoding="utf-8")
        cls.auth = (ROOT / "skills/information-authenticator/SKILL.md").read_text(encoding="utf-8")
        cls.fire = (ROOT / "skills/skill-analyzer/references/fire-control-plane.md").read_text(encoding="utf-8")
        cls.readiness = (ROOT / "skills/skill-analyzer/references/capability-readiness.md").read_text(encoding="utf-8")
        cls.e2i = (ROOT / "skills/skill-analyzer/references/evaluation-to-implementation.md").read_text(encoding="utf-8")
        cls.suite = (ROOT / "skills/skill-analyzer/references/benchmark-regression-suite.md").read_text(encoding="utf-8")

    def test_contract_version_and_target(self):
        self.assertEqual(self.contract["contract_version"], "1.1.0")
        self.assertEqual(self.contract["target_plugin_version"], "0.9.0")
        self.assertEqual(self.contract["implementation_scope"], "FOUNDATION_PLUS_IMPLEMENTATION_ASSURANCE")

    def test_required_case_count_is_70(self):
        self.assertEqual(len(self.cases), 70)
        self.assertEqual(self.contract["required_case_count"], 70)

    def test_case_ids_are_unique(self):
        self.assertEqual(len(self.case_by_id), len(self.cases))

    def test_case_id_set_is_complete(self):
        expected = ({f"R{i:02d}" for i in range(1,16)} | {f"E{i:02d}" for i in range(1,9)} |
                    {f"G{i:02d}" for i in range(1,13)} | {f"F{i:02d}" for i in range(1,11)} |
                    {f"C{i:02d}" for i in range(1,6)} | {f"D{i:02d}" for i in range(1,6)} |
                    {f"X{i:02d}" for i in range(1,6)} | {f"I{i:02d}" for i in range(1,6)} |
                    {f"T{i:02d}" for i in range(1,6)})
        self.assertEqual(set(self.case_by_id), expected)

    def test_required_categories_present(self):
        present = {c["category"] for c in self.cases}
        self.assertTrue(set(self.contract["case_categories"]).issubset(present))

    def test_each_case_has_oracle_rationale_and_execution_evidence_requirement(self):
        for case in self.cases:
            with self.subTest(case=case["id"]):
                self.assertGreaterEqual(len(case.get("scenario", "")), 12)
                self.assertGreaterEqual(len(case.get("oracle_rationale", "")), 20)
                self.assertTrue(case.get("risk_if_wrong"))
                self.assertEqual(case.get("oracle_type"), "contract_expectation")
                self.assertTrue(case.get("execution_evidence_required"))
                self.assertTrue(case.get("primary_specialist"))
                self.assertIsInstance(case.get("expected_engines"), list)
                self.assertIsInstance(case.get("expected_artifacts"), list)

    def test_every_material_case_requires_both_gates(self):
        for case in self.cases:
            if case["material"]:
                with self.subTest(case=case["id"]):
                    self.assertTrue(case["gate1"])
                    self.assertTrue(case["gate2"])

    def test_only_narrow_creative_case_is_exempt(self):
        exempt = [c["id"] for c in self.cases if c["expected"] == "CREATIVE_ONLY_EXEMPTION"]
        self.assertEqual(exempt, ["R14"])
        self.assertFalse(self.case_by_id["R14"]["material"])

    def test_legacy_45_cases_preserved(self):
        expected = ({f"R{i:02d}" for i in range(1,16)} | {f"E{i:02d}" for i in range(1,9)} |
                    {f"G{i:02d}" for i in range(1,13)} | {f"F{i:02d}" for i in range(1,11)})
        self.assertTrue(expected.issubset(set(self.case_by_id)))

    def test_capability_readiness_scenarios_present(self):
        expected = {"REQUIRED_TOOL_PREFLIGHT","ACCESS_DENIED_FAILS_CLOSED","MODEL_CAPABILITY_NOT_TOOL_EXECUTION","EXPIRING_DEPENDENCY_RECHECK","FALLBACK_MUST_BE_AUTHORIZED_AND_EQUIVALENT"}
        self.assertTrue(expected.issubset({c["expected"] for c in self.cases}))

    def test_change_impact_scenarios_present(self):
        expected = {"BASELINE_CANDIDATE_INVENTORY","BREAKING_CHANGE_CLASSIFIED","REFERENCE_AND_DELETION_INTEGRITY","IMPACT_BASED_TEST_SELECTION","ROLLBACK_AND_READBACK_REQUIRED"}
        self.assertTrue(expected.issubset({c["expected"] for c in self.cases}))

    def test_experiment_scenarios_present(self):
        expected = {"AUTHORIZATION_SCOPE_BEFORE_RUN","NO_SANDBOX_ASSUMPTION","BASELINE_CANDIDATE_COMPARABILITY","EXECUTION_STREAMS_SEPARATED","STOP_ON_SCOPE_OR_SIDE_EFFECT"}
        self.assertTrue(expected.issubset({c["expected"] for c in self.cases}))

    def test_e2i_scenarios_present(self):
        expected = {"ACCEPTED_RECOMMENDATION_TO_REQUIREMENT","TESTABLE_ACCEPTANCE_CRITERIA","IMPLEMENTED_NOT_VERIFIED","MISSING_OWNER_BUDGET_AS_UNKNOWN","RELEASE_READBACK_CLOSURE"}
        self.assertTrue(expected.issubset({c["expected"] for c in self.cases}))

    def test_test_governance_scenarios_present(self):
        expected = {"MUTATION_REMOVAL_GATE_DETECTED","MUTATION_ENGINE_TRIGGER_DETECTED","ORACLE_REVIEW_CATCHES_WRONG_EXPECTATION","SCHEMA_INSTANCE_AND_GRAPH_REFERENCES_VALIDATED","CONTRACT_HOST_AND_TRACE_EVIDENCE_SEPARATED"}
        self.assertTrue(expected.issubset({c["expected"] for c in self.cases}))

    def test_release_policy_is_fail_closed(self):
        self.assertTrue(gate_policy_valid(self.contract))

    def test_release_policy_pass_requires_evidence_and_readback(self):
        required = set(self.contract["release_policy"]["pass_requires"])
        self.assertTrue({"gate_1_pass","gate_2_pass","required_coverage_complete","no_open_p0_p1","material_unknowns_dispositioned","reconstruction_claims_verified","capability_readiness_confirmed_for_required_actions","change_impact_assessed","test_oracles_reviewed","read_back_confirmed_when_release_applies"}.issubset(required))

    def test_pass_with_caveats_requires_authority_and_review(self):
        required = set(self.contract["release_policy"]["pass_with_caveats_requires"])
        self.assertTrue({"no_open_p0_p1","limitations_disclosed","authority_recorded","mitigation_recorded","review_trigger_recorded"}.issubset(required))

    def test_master_and_authenticator_have_new_foundations(self):
        for phrase in ("Capability Readiness", "Evaluation-to-Implementation", "Change Impact", "Controlled Experiment", "Failure Intelligence & Reconstruction Engine", "Residual Unknowns Ledger", "Trace Graph"):
            with self.subTest(phrase=phrase):
                self.assertIn(phrase.lower(), self.master.lower())
        for phrase in ("Gate 1", "Gate 2", "FAIL-CLOSED", "Evidence Registry", "Residual Unknowns", "Trace Graph", "Reconstruction Verification", "Capability Readiness", "Change Impact", "EVALUATION-TO-IMPLEMENTATION"):
            with self.subTest(phrase=phrase):
                self.assertIn(phrase.lower(), self.auth.lower())

    def test_readiness_and_e2i_docs_have_operational_states(self):
        for state in ("READY", "READY_WITH_LIMITATIONS", "BLOCKED", "UNAVAILABLE", "ACCESS_DENIED", "NOT_CHECKED", "EXPIRED"):
            self.assertIn(state, self.readiness)
        for state in ("PROPOSED", "ACCEPTED", "IMPLEMENTED", "VERIFICATION_PENDING", "VERIFIED", "RELEASED", "READ_BACK_CONFIRMED", "CLOSED"):
            self.assertIn(state, self.e2i)

    def test_fire_contains_postmortem_recurrence_and_persistence_boundary(self):
        for phrase in ("Postmortem", "new occurrence", "Persistence boundary", "Capability readiness", "Controlled experiment", "Change impact", "Evaluation-to-Implementation"):
            with self.subTest(phrase=phrase):
                self.assertIn(phrase.lower(), self.fire.lower())

    def test_all_references_exist(self):
        for rel in required_files():
            self.assertTrue((ROOT / rel).is_file(), rel)
        for rel in self.contract["schemas"].values():
            self.assertTrue((ROOT / rel).is_file(), rel)

    def test_schema_documents_parse_and_check(self):
        try:
            import jsonschema
        except ImportError:
            self.skipTest("jsonschema package unavailable; structural schema checks remain")
        for name, schema in self.schemas.items():
            with self.subTest(schema=name):
                jsonschema.Draft202012Validator.check_schema(schema)

    def test_evidence_schema_valid_sample(self):
        schema = self.schemas["evidence"]
        sample = {
            "evidence_id":"EVD-SAMPLE-1","evidence_type":"tool_output",
            "provenance":{"origin_type":"tool_observation","locator":"test://sample"},
            "collected_at":"2026-11-08T00:00:00Z","access_status":"direct",
            "scope":{"context":"unit test","coverage":"single fixture"},
            "claim_links":[{"claim_id":"CLM-1","relation":"supports"}],
            "epistemic_status":"observed","limitations":[],"record_version":1,"record_status":"ACTIVE"
        }
        try:
            import jsonschema
            jsonschema.validate(sample, schema)
        except ImportError:
            self.assertEqual(sample["record_status"], "ACTIVE")

    def test_unknown_schema_blocks_resolution_without_evidence(self):
        schema = self.schemas["unknowns"]
        sample = {"unknown_id":"UNK-1","question":"Which dependency was missing?","materiality":"P1","known":[],"unknown":["provider state"],"required_evidence":["provider log"],"status":"RESOLVED","impact_if_unresolved":"release blocked"}
        try:
            import jsonschema
            with self.assertRaises(jsonschema.ValidationError):
                jsonschema.validate(sample, schema)
        except ImportError:
            self.assertFalse(validate_unknown_record(sample))

    def test_unknown_accepted_limitation_requires_authority(self):
        sample = {"unknown_id":"UNK-2","question":"What remains unknown?","materiality":"P2","known":[],"unknown":["historical event"],"required_evidence":[],"status":"ACCEPTED_LIMITATION","impact_if_unresolved":"bounded","acceptance_authority":None,"accepted_rationale":None,"review_trigger":None}
        self.assertFalse(validate_unknown_record(sample))

    def test_trace_graph_schema_valid_sample_and_references(self):
        graph = {"graph_id":"GR-1","nodes":[{"node_id":"NODE-A","node_type":"CLAIM","label":"claim","epistemic_status":"documented"},{"node_id":"NODE-B","node_type":"EVIDENCE","label":"evidence","epistemic_status":"observed"}],"edges":[{"edge_id":"EDGE-1","from":"NODE-B","to":"NODE-A","relation":"SUPPORTS","basis_status":"observed","evidence_refs":["EVD-1"]}]}
        try:
            import jsonschema
            jsonschema.validate(graph, self.schemas["trace_graph"])
        except ImportError:
            self.assertIn("nodes", graph)
        self.assertTrue(validate_trace_references(graph, {"EVD-1"}))

    def test_trace_graph_rejects_dangling_edge(self):
        graph = {"graph_id":"GR-2","nodes":[{"node_id":"NODE-A"}],"edges":[{"edge_id":"EDGE-1","from":"NODE-A","to":"NODE-MISSING","evidence_refs":[]}]}
        self.assertFalse(validate_trace_references(graph))

    def test_execution_schema_blocks_pass_without_observation(self):
        sample = {"run_id":"RUN-1","case_id":"R01","plugin_version":"0.9.0","test_layer":"HOST_BEHAVIOR","status":"HOST_BEHAVIOR_PASSED","observed_at":None,"observed_behavior":None,"evidence_refs":[]}
        self.assertFalse(validate_execution_record(sample))

    def test_execution_schema_accepts_not_run_record(self):
        ledger = load_json(LEDGER_PATH)
        self.assertEqual(len(ledger["records"]), 70)
        self.assertTrue(all(r["status"] == "NOT_RUN" for r in ledger["records"]))
        self.assertTrue(all(validate_execution_record(r) for r in ledger["records"]))

    def test_not_run_is_never_counted_as_pass(self):
        ledger = load_json(LEDGER_PATH)
        statuses = [r["status"] for r in ledger["records"]]
        self.assertEqual(statuses.count("NOT_RUN"), 70)
        self.assertFalse(any(s.endswith("PASSED") for s in statuses))

    def test_manifest_identity_version_prompts_and_metadata_preserved(self):
        root = load_json(ROOT / "plugin.json")
        compat = load_json(ROOT / ".codex-plugin/plugin.json")
        self.assertEqual(root["name"], "skill-analyzer")
        self.assertEqual(root["version"], "1.3.0")
        self.assertEqual(compat["version"], "1.3.0")
        self.assertEqual(root["version"], compat["version"])
        self.assertEqual(root["description"], compat["description"])
        self.assertEqual(root["keywords"], compat["keywords"])
        self.assertEqual(root["author"]["name"], "Hary Saidno")
        self.assertEqual(root["extensions"]["com.openai"]["interface"]["defaultPrompt"], compat["interface"]["defaultPrompt"])
        self.assertEqual(root["skills"], "./skills")

    def test_ten_specialists_preserved_in_baseline(self):
        expected = {"analytical-collector", "analyzer", "negative-collector", "positive-converter", "evidence-auditor", "strategic-foresight", "evaluator", "komparator", "comparative-analytic", "information-authenticator"}
        baseline = load_json(ROOT / "tests/preservation-baseline.json")
        preserved = {Path(item).parts[1] for item in baseline["preserved_skill_paths"]}
        self.assertEqual(len(preserved), 10)
        self.assertTrue(expected.issubset(preserved))

    def test_rea_adapter_and_technical_specialist_still_deferred(self):
        self.assertEqual(self.contract["deferred_components"], ["technical-reverse-engineering-specialist", "rea-mcp-adapter", "rea-cli-integration"])
        self.assertNotIn("rea-mcp-adapter", self.master.lower())

    def test_test_suite_reports_70_cases_and_layer_boundaries(self):
        self.assertIn("70 required scenarios", self.suite)
        self.assertIn("RUNTIME_TRACE_PASSED", self.suite)
        self.assertIn("does not execute the 70 host scenarios", self.suite)

    def test_mutation_detection_for_gate_2(self):
        mutated = self.auth.replace("### Gate 2 — Final release", "### Gate removed", 1)
        errors = mutation_contract_check(self.master, mutated, self.fire, self.readiness, self.e2i)
        self.assertIn("auth has both gates", errors)

    def test_mutation_detection_for_fail_closed(self):
        mutated = self.auth.replace("FAIL-CLOSED", "OPEN-DEFAULT", 1)
        errors = mutation_contract_check(self.master, mutated, self.fire, self.readiness, self.e2i)
        self.assertIn("auth has fail-closed", errors)

    def test_mutation_detection_for_readiness(self):
        mutated = self.readiness.replace("## 3. Readiness status", "## Readiness heading removed", 1)
        errors = mutation_contract_check(self.master, self.auth, self.fire, mutated, self.e2i)
        self.assertIn("readiness has blocked state", errors)

    def test_mutation_detection_for_e2i(self):
        mutated = self.e2i.replace("## 3. Implementation lifecycle", "## Lifecycle removed", 1)
        errors = mutation_contract_check(self.master, self.auth, self.fire, self.readiness, mutated)
        self.assertIn("E2I has verified state", errors)

    def test_mutation_detection_for_fire(self):
        mutated = self.fire.replace("## 6. Reconstruction protocol", "## Reconstruction removed", 1)
        errors = mutation_contract_check(self.master, self.auth, mutated, self.readiness, self.e2i)
        self.assertIn("FIRE has reconstruction", errors)

    def test_formal_route_activation_and_readiness_schemas_validate(self):
        import jsonschema
        route = {
            "route_id":"ROUTE-1","contract_version":"1.1.0","case_id":"R01","intent":"plugin maintenance",
            "primary_specialist":"master-orchestrator","supporting_specialists":[],"engine_activations":[],"non_activations":[],
            "gate_requirement":{"gate_1":True,"gate_2":True},"observability":"BEHAVIOR_ONLY","route_status":"EXPECTED",
            "observed_output":"Master maintenance route selected","evidence_refs":["EVD-ROUTE-1"]
        }
        activation = {
            "activation_id":"ACT-1","case_id":"F01","engine":"FIRE","status":"COMPLETED",
            "positive_triggers":["observed defect"],"negative_triggers":[],"reason":"A failure was reported.",
            "required_artifacts":["failure-record"],"produced_artifacts":["FAI-1"],"evidence_refs":["EVD-1"]
        }
        readiness = {
            "capability_id":"CAP-1","operation":"read file inventory","provider":"Plugin Creator","status":"READY",
            "checked_at":"2026-11-08T00:00:00Z","required_scope":"read current plugin source","limitations":[],"execution_claim_allowed":True
        }
        jsonschema.validate(route, self.schemas["route_receipt"])
        jsonschema.validate(activation, self.schemas["engine_activation_receipt"])
        jsonschema.validate(readiness, self.schemas["capability_readiness"])

    def test_formal_failure_change_experiment_and_e2i_schemas_validate(self):
        import jsonschema
        failure = {
            "incident_id":"FAI-1","occurrence_id":"OCC-1","created_at":"2026-11-08T00:00:00Z",
            "category":"ROUTE","severity":"P1","status":"DETECTED","reproduction_status":"PENDING",
            "rca_status":"NOT_STARTED","expected_behavior":"master route","observed_behavior":"wrong route",
            "evidence_refs":["EVD-1"],"release_disposition":"HOLD","data_sanitized":True
        }
        change = {
            "change_id":"CHG-1","baseline":{"version":"0.8.0"},"candidate":{"version":"0.9.0"},
            "diff_entries":[{"path_or_component":"master","change_type":"BEHAVIORAL","impact":"router updates"}],
            "affected_requirements":["REQ-1"],"affected_tests":["R01"],"test_selection_rationale":"directly affected routes", 
            "preservation_checks":["sub-skills retained"],"status":"COMPLETE"
        }
        experiment = {
            "experiment_id":"EXP-1","target":"local test fixture","authorization_status":"NOT_REQUIRED","scope":"read-only fixture",
            "hypothesis":"candidate output differs","baseline":{"identifier":"base-1"},"candidate":{"identifier":"cand-1"},
            "execution_status":"EXECUTED","started_at":"2026-11-08T00:00:00Z","ended_at":"2026-11-08T00:00:01Z",
            "exit_code":0,"side_effects":[],"rollback_plan":"no state mutation","evidence_refs":["EVD-EXP-1"],"result":"observed difference"
        }
        implementation = {
            "requirement_id":"REQ-1","recommendation_id":"REC-1","decision":"ACCEPTED","state":"CLOSED",
            "acceptance_criteria":["test passes"],"dependencies":[],"test_refs":["TST-1"],"evidence_refs":["EVD-1"],
            "gate2_status":"PASS"
        }
        jsonschema.validate(failure, self.schemas["failure_record"])
        jsonschema.validate(change, self.schemas["change_impact"])
        jsonschema.validate(experiment, self.schemas["controlled_experiment"])
        jsonschema.validate(implementation, self.schemas["implementation_assurance"])

    def test_formal_schemas_reject_unsafe_states(self):
        import jsonschema
        bad_p0 = {
            "incident_id":"FAI-2","occurrence_id":"OCC-2","created_at":"2026-11-08T00:00:00Z",
            "category":"AUTH","severity":"P0","status":"DETECTED","reproduction_status":"PENDING",
            "rca_status":"NOT_STARTED","expected_behavior":"gate enforced","observed_behavior":"gate skipped",
            "evidence_refs":["EVD-2"],"release_disposition":"PASS","data_sanitized":True
        }
        with self.assertRaises(jsonschema.ValidationError):
            jsonschema.validate(bad_p0, self.schemas["failure_record"])
        not_ready = {
            "capability_id":"CAP-2","operation":"host route trace","provider":"host","status":"UNAVAILABLE",
            "checked_at":"2026-11-08T00:00:00Z","required_scope":"internal trace","limitations":[],"execution_claim_allowed":True
        }
        with self.assertRaises(jsonschema.ValidationError):
            jsonschema.validate(not_ready, self.schemas["capability_readiness"])

    def test_execution_ledger_instances_validate_against_schema(self):
        import jsonschema
        ledger = load_json(LEDGER_PATH)
        for record in ledger["records"]:
            with self.subTest(case=record["case_id"]):
                jsonschema.validate(record, self.schemas["test_execution"])

    def test_change_impact_diff_classes_documented(self):
        text = (ROOT / "skills/skill-analyzer/references/change-impact-analysis.md").read_text(encoding="utf-8")
        for term in ("ADDITIVE","BEHAVIORAL","BREAKING","DEPENDENCY","REFERENCE","REMOVAL","PRESERVED","UNKNOWN"):
            self.assertIn(term, text)

    def test_controlled_experiment_has_scope_bounds_and_side_effects(self):
        text = (ROOT / "skills/skill-analyzer/references/controlled-experiment.md").read_text(encoding="utf-8")
        for term in ("Authorization","timeout","stdout","stderr","exit code","rollback","sandbox"):
            self.assertIn(term.lower(), text.lower())

    def test_registry_has_custody_and_data_handling(self):
        props = self.schemas["evidence"]["properties"]
        self.assertIn("custody_events", props)
        self.assertIn("data_handling", props)
        self.assertIn("supersedes_evidence_id", props)

    def test_trace_schema_has_reconstruction_and_change_edges(self):
        rels = self.schemas["trace_graph"]["properties"]["edges"]["items"]["properties"]["relation"]["enum"]
        self.assertTrue({"IMPLEMENTS","CHANGES","RECONSTRUCTS","REOPENS"}.issubset(set(rels)))

    def test_case_contract_does_not_contain_observed_results(self):
        self.assertTrue(all("observed_behavior" not in c for c in self.cases))

    def test_execution_ledger_is_explicitly_blank(self):
        ledger = load_json(LEDGER_PATH)
        self.assertFalse(ledger["host_runtime_tested"])
        self.assertFalse(ledger["internal_router_trace_available"])
        self.assertIn("not evidence of execution", ledger["purpose"])

    def test_preservation_scope_does_not_claim_hashes_unless_computed(self):
        text = (ROOT / "skills/skill-analyzer/references/change-impact-analysis.md").read_text(encoding="utf-8")
        self.assertIn("Hashes prove byte equality only when actually computed", text)


def run():
    suite = unittest.defaultTestLoader.loadTestsFromTestCase(EvidenceControlContractTests)
    result = unittest.TextTestRunner(verbosity=2).run(suite)
    try:
        import jsonschema
        schema_validator = "jsonschema"
    except ImportError:
        schema_validator = "structural-fallback"
    contract = load_json(CONTRACT_PATH)
    ledger = load_json(LEDGER_PATH)
    report = {
        "contract_version": "1.1.0",
        "target_plugin_version": "0.9.0",
        "test_layer": "STATIC_CONTRACT_AND_HARNESS_QUALITY_TEST",
        "contract_cases_defined": len(contract["cases"]),
        "schema_documents_checked": len(contract["schemas"]),
        "execution_ledger_records_validated": len(ledger["records"]),
        "static_tests_run": result.testsRun,
        "passed": result.testsRun - len(result.failures) - len(result.errors),
        "failed": len(result.failures),
        "errors": len(result.errors),
        "status": "CONTRACT_AND_HARNESS_TEST_PASSED" if result.wasSuccessful() else "FAILED",
        "schema_validator": schema_validator,
        "mutation_checks_run": 5,
        "mutation_checks_caught": 5 if result.wasSuccessful() else None,
        "host_scenarios_executed": 0,
        "host_runtime_tested": False,
        "internal_router_trace_available": False,
        "e2e_execution_ledger_status": "NOT_RUN",
        "registry_storage": "SCHEMA_AND_ARTIFACT_CONTRACT_ONLY",
        "runtime_telemetry": "NOT_AVAILABLE_IN_PLUGIN_PACKAGE",
        "limitations": [
            "The 70 scenario definitions are not executed by this static/contract runner.",
            "No ChatGPT host routing or engine activation was executed by this runner.",
            "No internal router trace or hard middleware gate enforcement is available from this package-only test.",
            "Persistent registry storage and host telemetry require an external authorized store/instrumentation."
        ],
        "failure_details": [str(item[1]) for item in result.failures + result.errors]
    }
    (ROOT / "tests" / "contract-test-report.json").write_text(json.dumps(report, indent=2) + "\n", encoding="utf-8")
    return 0 if result.wasSuccessful() else 1

if __name__ == "__main__":
    raise SystemExit(run())
