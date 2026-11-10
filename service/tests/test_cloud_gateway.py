from __future__ import annotations

import json
import os
import unittest
from unittest.mock import patch

from service.app.audit import principal_fingerprint
from service.app.auth import GatewayTokenVerifier
from service.app.config import Settings
from service.app.limiter import RateLimiter
from service.app.runtime import list_commands, resolve_route


class CloudGatewayTests(unittest.IsolatedAsyncioTestCase):
    def make_settings(self, **overrides):
        base = {
            "APP_ENV": "test",
            "PUBLIC_BASE_URL": "http://127.0.0.1:8000",
            "DEV_BEARER_TOKENS_JSON": json.dumps({
                "local-test-token": {
                    "sub": "test-client",
                    "scopes": ["analyzer:invoke", "analyzer:read"]
                }
            }),
            "RATE_LIMIT_BACKEND": "memory",
            "RATE_LIMIT_PER_MINUTE": "2",
        }
        base.update(overrides)
        with patch.dict(os.environ, base, clear=False):
            return Settings.from_env()

    async def test_development_bearer_token_is_verified(self):
        settings = self.make_settings()
        verifier = GatewayTokenVerifier(settings)
        access = await verifier.verify_token("local-test-token")
        self.assertIsNotNone(access)
        self.assertEqual(access.subject, "test-client")
        self.assertIn("analyzer:invoke", access.scopes)

    async def test_invalid_development_token_is_rejected(self):
        settings = self.make_settings()
        verifier = GatewayTokenVerifier(settings)
        self.assertIsNone(await verifier.verify_token("wrong-token"))

    async def test_runtime_resolves_canonical_route(self):
        route = resolve_route("/analyzer:audit")
        self.assertEqual(route["id"], "audit")
        self.assertIn("analyzer", route["primary_skills"])

    async def test_command_catalog_is_not_empty(self):
        commands = list_commands()
        self.assertGreaterEqual(len(commands), 11)
        self.assertIn("audit", {item["id"] for item in commands})

    async def test_local_rate_limit_blocks_after_threshold(self):
        settings = self.make_settings()
        limiter = RateLimiter(settings)
        first, _ = await limiter.allow("test-client")
        second, _ = await limiter.allow("test-client")
        third, retry = await limiter.allow("test-client")
        self.assertTrue(first)
        self.assertTrue(second)
        self.assertFalse(third)
        self.assertGreaterEqual(retry, 1)

    def test_actor_fingerprint_is_pseudonymous_and_salted(self):
        a = principal_fingerprint("person-123", "salt-a")
        b = principal_fingerprint("person-123", "salt-b")
        self.assertNotEqual(a, b)
        self.assertNotIn("person-123", a)

    def test_production_configuration_fails_closed_without_oidc(self):
        env = {
            "APP_ENV": "production",
            "PUBLIC_BASE_URL": "https://gateway.example.com",
            "MCP_RESOURCE_URL": "https://gateway.example.com/mcp",
        }
        with patch.dict(os.environ, env, clear=True):
            with self.assertRaises(RuntimeError):
                Settings.from_env()


if __name__ == "__main__":
    unittest.main()
