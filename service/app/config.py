from __future__ import annotations

import json
import os
from dataclasses import dataclass
from urllib.parse import urlsplit


def _csv(name: str, default: str = "") -> tuple[str, ...]:
    return tuple(item.strip() for item in os.getenv(name, default).split(",") if item.strip())


@dataclass(frozen=True)
class Settings:
    app_env: str
    public_base_url: str
    mcp_resource_url: str
    oidc_issuer_url: str
    oidc_jwks_url: str
    oidc_audience: str
    allowed_algorithms: tuple[str, ...]
    dev_bearer_tokens: dict
    llm_base_url: str
    llm_api_key: str
    llm_model: str
    llm_timeout_seconds: float
    llm_max_output_tokens: int
    max_target_chars: int
    max_context_chars: int
    max_constraint_count: int
    rate_limit_backend: str
    redis_url: str
    rate_limit_per_minute: int
    audit_hash_salt: str
    allowed_hosts: tuple[str, ...]
    allowed_origins: tuple[str, ...]
    log_level: str

    @property
    def is_production(self) -> bool:
        return self.app_env == "production"

    @property
    def provider_ready(self) -> bool:
        return bool(self.llm_base_url and self.llm_api_key and self.llm_model)

    @classmethod
    def from_env(cls) -> "Settings":
        app_env = os.getenv("APP_ENV", "development").strip().lower()
        if app_env not in {"development", "test", "staging", "production"}:
            raise RuntimeError("APP_ENV must be development, test, staging, or production")

        public_base_url = os.getenv("PUBLIC_BASE_URL", "http://127.0.0.1:8000").rstrip("/")
        parsed_base = urlsplit(public_base_url)
        if parsed_base.scheme not in {"http", "https"} or not parsed_base.netloc:
            raise RuntimeError("PUBLIC_BASE_URL must be an absolute HTTP(S) URL")

        mcp_resource_url = os.getenv("MCP_RESOURCE_URL", f"{public_base_url}/mcp").rstrip("/")
        resource = urlsplit(mcp_resource_url)
        if resource.scheme != "https" and app_env == "production":
            raise RuntimeError("MCP_RESOURCE_URL must use HTTPS in production")
        if not resource.netloc or resource.path != "/mcp":
            raise RuntimeError("MCP_RESOURCE_URL must be the full public MCP endpoint ending in /mcp")
        if app_env == "production" and parsed_base.scheme != "https":
            raise RuntimeError("PUBLIC_BASE_URL must use HTTPS in production")

        dev_tokens_raw = os.getenv("DEV_BEARER_TOKENS_JSON", "{}")
        try:
            dev_tokens = json.loads(dev_tokens_raw)
        except json.JSONDecodeError as exc:
            raise RuntimeError("DEV_BEARER_TOKENS_JSON must be valid JSON") from exc
        if not isinstance(dev_tokens, dict):
            raise RuntimeError("DEV_BEARER_TOKENS_JSON must be a JSON object")

        allowed_hosts = list(_csv("MCP_ALLOWED_HOSTS"))
        if not allowed_hosts:
            allowed_hosts = [parsed_base.netloc, f"{parsed_base.hostname}:*"]
            if app_env != "production":
                allowed_hosts.extend([
                    "127.0.0.1:8000", "127.0.0.1:*",
                    "localhost:8000", "localhost:*",
                ])

        allowed_origins = _csv("MCP_ALLOWED_ORIGINS")
        if not allowed_origins and app_env != "production":
            allowed_origins = (
                "http://localhost:3000",
                "http://127.0.0.1:3000",
                "http://localhost:6274",
                "http://127.0.0.1:6274",
            )

        oidc_audience = os.getenv("OIDC_AUDIENCE", mcp_resource_url)
        if oidc_audience != mcp_resource_url:
            raise RuntimeError("OIDC_AUDIENCE must exactly match MCP_RESOURCE_URL to prevent resource-token confusion")
        allowed_algorithms = _csv("OIDC_ALLOWED_ALGORITHMS", "RS256")
        if not allowed_algorithms or not set(allowed_algorithms).issubset({"RS256", "ES256", "PS256"}):
            raise RuntimeError("OIDC_ALLOWED_ALGORITHMS may contain only RS256, ES256, and PS256")

        oidc_issuer_url = os.getenv("OIDC_ISSUER_URL", "")
        oidc_jwks_url = os.getenv("OIDC_JWKS_URL", "")
        if app_env == "production":
            if urlsplit(oidc_issuer_url).scheme != "https":
                raise RuntimeError("OIDC_ISSUER_URL must use HTTPS in production")
            if urlsplit(oidc_jwks_url).scheme != "https":
                raise RuntimeError("OIDC_JWKS_URL must use HTTPS in production")

        rate_backend = os.getenv(
            "RATE_LIMIT_BACKEND",
            "redis" if app_env == "production" else "memory",
        ).strip().lower()
        if rate_backend not in {"redis", "memory"}:
            raise RuntimeError("RATE_LIMIT_BACKEND must be redis or memory")

        settings = cls(
            app_env=app_env,
            public_base_url=public_base_url,
            mcp_resource_url=mcp_resource_url,
            oidc_issuer_url=oidc_issuer_url,
            oidc_jwks_url=oidc_jwks_url,
            oidc_audience=oidc_audience,
            allowed_algorithms=allowed_algorithms,
            dev_bearer_tokens=dev_tokens,
            llm_base_url=os.getenv("LLM_BASE_URL", "https://api.openai.com/v1").rstrip("/"),
            llm_api_key=os.getenv("LLM_API_KEY", ""),
            llm_model=os.getenv("LLM_MODEL", ""),
            llm_timeout_seconds=float(os.getenv("LLM_TIMEOUT_SECONDS", "90")),
            llm_max_output_tokens=int(os.getenv("LLM_MAX_OUTPUT_TOKENS", "2500")),
            max_target_chars=int(os.getenv("MAX_TARGET_CHARS", "20000")),
            max_context_chars=int(os.getenv("MAX_CONTEXT_CHARS", "40000")),
            max_constraint_count=int(os.getenv("MAX_CONSTRAINT_COUNT", "20")),
            rate_limit_backend=rate_backend,
            redis_url=os.getenv("REDIS_URL", ""),
            rate_limit_per_minute=int(os.getenv("RATE_LIMIT_PER_MINUTE", "20")),
            audit_hash_salt=os.getenv("AUDIT_HASH_SALT", ""),
            allowed_hosts=tuple(dict.fromkeys(allowed_hosts)),
            allowed_origins=allowed_origins,
            log_level=os.getenv("LOG_LEVEL", "INFO").upper(),
        )

        if app_env == "production":
            required = {
                "OIDC_ISSUER_URL": settings.oidc_issuer_url,
                "OIDC_JWKS_URL": settings.oidc_jwks_url,
                "OIDC_AUDIENCE": settings.oidc_audience,
                "LLM_API_KEY": settings.llm_api_key,
                "LLM_MODEL": settings.llm_model,
                "REDIS_URL": settings.redis_url if rate_backend == "redis" else "",
                "AUDIT_HASH_SALT": settings.audit_hash_salt,
            }
            missing = [name for name, value in required.items() if not value]
            if missing:
                raise RuntimeError(
                    "Production configuration is incomplete: " + ", ".join(missing)
                )
            if settings.dev_bearer_tokens:
                raise RuntimeError("DEV_BEARER_TOKENS_JSON must be empty in production")

        if settings.rate_limit_backend == "redis" and not settings.redis_url:
            raise RuntimeError("REDIS_URL is required when RATE_LIMIT_BACKEND=redis")
        if not settings.allowed_hosts:
            raise RuntimeError("MCP_ALLOWED_HOSTS or a valid PUBLIC_BASE_URL is required")
        return settings
