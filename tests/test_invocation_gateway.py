"""Contract tests for the Universal AI Invocation Gateway."""
from __future__ import annotations

import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))

import invoke  # noqa: E402


class InvocationGatewayTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.registry, cls.platforms = invoke.load_catalog()

    def test_canonical_command_resolves(self):
        self.assertEqual(invoke.resolve_command("audit", self.registry)["id"], "audit")

    def test_slash_alias_resolves(self):
        self.assertEqual(invoke.resolve_command("/analyzer:audit", self.registry)["id"], "audit")

    def test_gemini_group_alias_resolves(self):
        self.assertEqual(invoke.resolve_command("/analyzer compare", self.registry)["id"], "compare")

    def test_unknown_command_is_rejected(self):
        with self.assertRaises(ValueError):
            invoke.resolve_command("invented-command", self.registry)

    def test_platform_adapter_is_explicit(self):
        envelope = invoke.build_envelope(
            "audit", "sample target", self.registry, self.platforms, platform_id="codex"
        )
        self.assertFalse(envelope["platform"]["native_slash_command"])
        self.assertIn(".agents/skills/", envelope["platform"]["project_skill_paths"])

    def test_unreported_capability_stays_not_checked(self):
        envelope = invoke.build_envelope(
            "audit", "sample target", self.registry, self.platforms
        )
        self.assertEqual(envelope["capability_readiness"]["statuses"]["web_search"], "NOT_CHECKED")

    def test_blocked_capability_blocks_dependent_branch(self):
        envelope = invoke.build_envelope(
            "audit", "sample target", self.registry, self.platforms,
            capability_declarations=["web_search=UNAVAILABLE"]
        )
        self.assertIn("web_search", envelope["capability_readiness"]["blocked_branches"])

    def test_cli_never_claims_execution(self):
        envelope = invoke.build_envelope(
            "audit", "sample target", self.registry, self.platforms
        )
        self.assertEqual(envelope["execution"]["status"], "PREPARED_NOT_EXECUTED")
        self.assertIn("PREPARED_NOT_EXECUTED", envelope["prompt"])

    def test_invalid_capability_status_is_rejected(self):
        with self.assertRaises(ValueError):
            invoke.parse_capability_declaration("web_search=PASS")


if __name__ == "__main__":
    unittest.main()
