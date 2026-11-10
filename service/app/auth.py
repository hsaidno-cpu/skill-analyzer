from __future__ import annotations

import asyncio
import hmac
import logging
import time
from typing import Any

import jwt
from jwt import PyJWKClient
from jwt.exceptions import PyJWTError
from mcp.server.auth.provider import AccessToken, TokenVerifier
from mcp.server.auth.settings import AuthSettings
from pydantic import AnyHttpUrl

from service.app.config import Settings

logger = logging.getLogger("skill_analyzer.auth")


def _extract_scopes(claims: dict[str, Any]) -> list[str]:
    raw = claims.get("scope", claims.get("scp", []))
    if isinstance(raw, str):
        return [scope for scope in raw.split() if scope]
    if isinstance(raw, list):
        return [str(scope) for scope in raw if scope]
    return []


class GatewayTokenVerifier(TokenVerifier):
    """Validates OIDC JWTs in production and configured local tokens in development."""

    def __init__(self, settings: Settings) -> None:
        self.settings = settings
        self._jwks = (
            PyJWKClient(settings.oidc_jwks_url, cache_jwk_set=True, lifespan=300, timeout=8)
            if settings.oidc_jwks_url
            else None
        )

    async def verify_token(self, token: str) -> AccessToken | None:
        if not token or len(token) > 16384:
            return None

        if self.settings.app_env in {"development", "test"} and self.settings.dev_bearer_tokens:
            return self._verify_development_token(token)

        if self._jwks is None or not self.settings.oidc_issuer_url:
            return None

        try:
            signing_key = await asyncio.to_thread(
                self._jwks.get_signing_key_from_jwt, token
            )
            claims = jwt.decode(
                token,
                signing_key.key,
                algorithms=list(self.settings.allowed_algorithms),
                issuer=self.settings.oidc_issuer_url,
                audience=self.settings.oidc_audience,
                options={
                    "require": ["exp", "iss", "aud", "sub"],
                    "verify_signature": True,
                    "verify_exp": True,
                    "verify_iss": True,
                    "verify_aud": True,
                },
                leeway=30,
            )
            scopes = _extract_scopes(claims)
            subject = str(claims["sub"])
            client_id = str(claims.get("azp") or claims.get("client_id") or subject)
            expires_at = int(claims["exp"])
            if expires_at <= int(time.time()):
                return None
            return AccessToken(
                token=token,
                client_id=client_id,
                scopes=scopes,
                expires_at=expires_at,
                resource=self.settings.mcp_resource_url,
                subject=subject,
                claims=claims,
            )
        except (PyJWTError, KeyError, TypeError, ValueError):
            return None
        except Exception as exc:
            logger.warning("OIDC token verification unavailable: %s", type(exc).__name__)
            return None

    def _verify_development_token(self, token: str) -> AccessToken | None:
        for raw_token, metadata in self.settings.dev_bearer_tokens.items():
            if not isinstance(raw_token, str) or not hmac.compare_digest(raw_token, token):
                continue
            if not isinstance(metadata, dict):
                return None
            scopes = metadata.get("scopes", ["analyzer:invoke"])
            if not isinstance(scopes, list):
                return None
            subject = str(metadata.get("sub", "local-development-client"))
            return AccessToken(
                token=token,
                client_id=str(metadata.get("client_id", subject)),
                scopes=[str(scope) for scope in scopes],
                resource=self.settings.mcp_resource_url,
                subject=subject,
                claims={"sub": subject, "iss": "local-development"},
            )
        return None


def build_mcp_auth_settings(settings: Settings) -> AuthSettings:
    # Development issuer is descriptive only; no OAuth authorization server is embedded.
    issuer = settings.oidc_issuer_url or "http://localhost:9000"
    return AuthSettings(
        issuer_url=AnyHttpUrl(issuer),
        resource_server_url=AnyHttpUrl(settings.mcp_resource_url),
        required_scopes=["analyzer:invoke"],
        validate_token_resource=True,
    )
