from __future__ import annotations

import logging
import time
import uuid
from contextlib import asynccontextmanager
from typing import Any

from fastapi import Depends, FastAPI, HTTPException, Request, Response
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from mcp.server import MCPServer
from mcp.server.auth.middleware.auth_context import get_access_token
from mcp.server.transport_security import TransportSecuritySettings
from pydantic import BaseModel, Field, field_validator

from service.app.audit import emit_audit_event
from service.app.auth import GatewayTokenVerifier, build_mcp_auth_settings
from service.app.config import Settings
from service.app.limiter import RateLimitBackendUnavailable, RateLimiter
from service.app.provider import ProviderError
from service.app.runtime import invoke_analysis, list_commands

settings = Settings.from_env()
logging.basicConfig(
    level=getattr(logging, settings.log_level, logging.INFO),
    format="%(message)s",
)
logger = logging.getLogger("skill_analyzer.http")
token_verifier = GatewayTokenVerifier(settings)
limiter = RateLimiter(settings)
security = HTTPBearer(auto_error=False)

mcp_server = MCPServer(
    "SKILL ANALYZER Universal Gateway",
    token_verifier=token_verifier,
    auth=build_mcp_auth_settings(settings),
)


@asynccontextmanager
async def lifespan(app: FastAPI):
    await limiter.start()
    try:
        async with mcp_server.session_manager.run():
            yield
    finally:
        await limiter.close()


app = FastAPI(
    title="SKILL ANALYZER Universal AI Gateway",
    version="1.2.0",
    docs_url=None,
    redoc_url=None,
    openapi_url=None,
    lifespan=lifespan,
)
app.add_middleware(
    CORSMiddleware,
    allow_origins=list(settings.allowed_origins),
    allow_methods=["GET", "POST", "OPTIONS", "DELETE"],
    allow_headers=[
        "Authorization", "Content-Type", "Mcp-Method", "Mcp-Name",
        "Mcp-Protocol-Version", "Mcp-Session-Id", "Last-Event-ID",
    ],
    expose_headers=["Mcp-Session-Id"],
)


class InvokeRequest(BaseModel):
    command: str = Field(min_length=1, max_length=80)
    target: str = Field(min_length=1, max_length=20000)
    objective: str = Field(default="", max_length=5000)
    mode: str = Field(default="", max_length=80)
    depth: str = Field(default="deep", pattern="^(standard|deep|forensic)$")
    scope: str = Field(default="", max_length=4000)
    context: str = Field(default="", max_length=40000)
    constraints: list[str] = Field(default_factory=list, max_length=20)
    desired_output: str = Field(default="", max_length=4000)

    @field_validator("constraints")
    @classmethod
    def validate_constraints(cls, values: list[str]) -> list[str]:
        if any(len(value) > 2000 for value in values):
            raise ValueError("Each constraint must be 2000 characters or fewer")
        return values


class InvokeResponse(BaseModel):
    request_id: str
    command: str
    route: dict[str, Any]
    loaded_skills: list[str]
    provider: str
    model: str
    execution_status: str
    tool_execution_status: str
    usage: dict[str, Any]
    result: str


def _request_id(request: Request) -> str:
    return getattr(request.state, "request_id", uuid.uuid4().hex)


def _actor(principal: Any) -> str:
    return str(getattr(principal, "subject", None) or getattr(principal, "client_id", "unknown"))


async def _authenticate(
    credentials: HTTPAuthorizationCredentials | None = Depends(security),
) -> Any:
    if credentials is None or credentials.scheme.lower() != "bearer":
        metadata_url = (
            settings.public_base_url.rstrip("/")
            + "/.well-known/oauth-protected-resource/mcp"
        )
        raise HTTPException(
            status_code=401,
            detail={"code": "authentication_required"},
            headers={"WWW-Authenticate": f'Bearer resource_metadata="{metadata_url}"'},
        )
    principal = await token_verifier.verify_token(credentials.credentials)
    if principal is None:
        metadata_url = (
            settings.public_base_url.rstrip("/")
            + "/.well-known/oauth-protected-resource/mcp"
        )
        raise HTTPException(
            status_code=401,
            detail={"code": "invalid_or_expired_token"},
            headers={"WWW-Authenticate": f'Bearer resource_metadata="{metadata_url}"'},
        )
    if "analyzer:invoke" not in principal.scopes:
        raise HTTPException(
            status_code=403,
            detail={"code": "insufficient_scope", "required": "analyzer:invoke"},
            headers={"WWW-Authenticate": 'Bearer error="insufficient_scope", scope="analyzer:invoke"'},
        )
    return principal


async def _enforce_rate_limit(principal: Any) -> None:
    try:
        allowed, retry_after = await limiter.allow(_actor(principal))
    except RateLimitBackendUnavailable as exc:
        logger.error("rate_limit_backend_unavailable error_type=%s", type(exc).__name__)
        raise HTTPException(
            status_code=503,
            detail={"code": "rate_limit_backend_unavailable"},
        ) from exc
    if not allowed:
        raise HTTPException(
            status_code=429,
            detail={"code": "rate_limit_exceeded"},
            headers={"Retry-After": str(retry_after)},
        )


def _audit_failure(
    *,
    event: str,
    request_id: str,
    actor: str,
    command: str | None,
    status: str,
    error_code: str,
    http_status: int,
    duration_ms: int,
    input_bytes: int | None = None,
) -> None:
    emit_audit_event(
        event=event,
        request_id=request_id,
        actor=actor,
        salt=settings.audit_hash_salt,
        command=command,
        status=status,
        error_code=error_code,
        http_status=http_status,
        duration_ms=duration_ms,
        input_bytes=input_bytes,
        provider="openai-compatible",
        model=settings.llm_model or None,
    )


@app.middleware("http")
async def request_metadata(request: Request, call_next):
    request.state.request_id = uuid.uuid4().hex
    started = time.perf_counter()
    try:
        response = await call_next(request)
    except Exception as exc:
        logger.error(
            "http_unhandled_error request_id=%s error_type=%s",
            request.state.request_id,
            type(exc).__name__,
        )
        raise
    response.headers["X-Request-ID"] = request.state.request_id
    response.headers["X-Content-Type-Options"] = "nosniff"
    response.headers["Referrer-Policy"] = "no-referrer"
    response.headers["Cache-Control"] = "no-store"
    # No request body, query string, Authorization header, prompt, or completion is logged.
    if request.url.path.startswith("/v1/") and response.status_code >= 400:
        logger.info(
            "http_api_result request_id=%s path=%s status=%s duration_ms=%s",
            request.state.request_id,
            request.url.path,
            response.status_code,
            int((time.perf_counter() - started) * 1000),
        )
    return response


@app.get("/healthz")
async def healthz():
    return {"status": "ok", "service": "skill-analyzer-gateway", "version": "1.2.0"}


@app.get("/readyz")
async def readyz():
    if not settings.provider_ready:
        return Response(
            content='{"status":"not_ready"}',
            status_code=503,
            media_type="application/json",
        )
    return {
        "status": "configured",
        "provider_configuration": "ready",
        "provider_connectivity": "NOT_CHECKED",
    }


@app.get("/v1/commands")
async def get_commands(principal: Any = Depends(_authenticate)):
    await _enforce_rate_limit(principal)
    return {"commands": list_commands()}


async def _run_request(
    payload: InvokeRequest,
    *,
    principal: Any,
    request_id: str,
    event: str,
) -> dict[str, Any]:
    actor = _actor(principal)
    started = time.perf_counter()
    input_bytes = len(
        (payload.target + payload.objective + payload.context + "".join(payload.constraints)).encode("utf-8")
    )
    try:
        result = await invoke_analysis(
            settings,
            command=payload.command,
            target=payload.target,
            objective=payload.objective,
            mode=payload.mode,
            depth=payload.depth,
            scope=payload.scope,
            context=payload.context,
            constraints=payload.constraints,
            desired_output=payload.desired_output,
        )
    except ValueError as exc:
        duration = int((time.perf_counter() - started) * 1000)
        _audit_failure(
            event=event, request_id=request_id, actor=actor, command=payload.command,
            status="REJECTED", error_code="unknown_or_ambiguous_command",
            http_status=400, duration_ms=duration, input_bytes=input_bytes,
        )
        raise HTTPException(
            status_code=400,
            detail={"code": "unknown_or_ambiguous_command"},
        ) from exc
    except ProviderError as exc:
        duration = int((time.perf_counter() - started) * 1000)
        _audit_failure(
            event=event, request_id=request_id, actor=actor, command=payload.command,
            status="FAILED", error_code=exc.code, http_status=exc.http_status,
            duration_ms=duration, input_bytes=input_bytes,
        )
        raise HTTPException(
            status_code=exc.http_status,
            detail={"code": exc.code},
        ) from exc
    except Exception as exc:
        duration = int((time.perf_counter() - started) * 1000)
        _audit_failure(
            event=event, request_id=request_id, actor=actor, command=payload.command,
            status="FAILED", error_code="analysis_runtime_error", http_status=500,
            duration_ms=duration, input_bytes=input_bytes,
        )
        logger.error(
            "analysis_runtime_error request_id=%s error_type=%s",
            request_id,
            type(exc).__name__,
        )
        raise HTTPException(
            status_code=500,
            detail={"code": "analysis_runtime_error"},
        ) from exc

    duration = int((time.perf_counter() - started) * 1000)
    emit_audit_event(
        event=event,
        request_id=request_id,
        actor=actor,
        salt=settings.audit_hash_salt,
        command=result["route"]["id"],
        status="MODEL_RESPONSE_RECEIVED",
        duration_ms=duration,
        provider=result["provider"],
        model=result["model"],
        input_bytes=input_bytes,
        output_chars=len(result["result"]),
        http_status=200,
    )
    return {
        "request_id": request_id,
        "command": result["route"]["id"],
        "route": result["route"],
        "loaded_skills": result["loaded_skills"],
        "provider": result["provider"],
        "model": result["model"],
        "execution_status": result["execution_status"],
        "tool_execution_status": result["tool_execution_status"],
        "usage": result["usage"],
        "result": result["result"],
    }


@app.post("/v1/invoke", response_model=InvokeResponse)
async def http_invoke(
    payload: InvokeRequest,
    request: Request,
    principal: Any = Depends(_authenticate),
):
    await _enforce_rate_limit(principal)
    return await _run_request(
        payload,
        principal=principal,
        request_id=_request_id(request),
        event="http_invoke",
    )


@mcp_server.tool()
async def invoke_skill_analyzer(
    command: str,
    target: str,
    objective: str = "",
    depth: str = "deep",
    context: str = "",
    constraints: list[str] | None = None,
) -> dict[str, Any]:
    """Run a routed SKILL ANALYZER command through the hosted model gateway."""
    principal = get_access_token()
    if principal is None:
        raise RuntimeError("Authenticated MCP principal is unavailable")
    await _enforce_rate_limit(principal)
    payload = InvokeRequest(
        command=command,
        target=target,
        objective=objective,
        depth=depth,
        context=context,
        constraints=constraints or [],
    )
    return await _run_request(
        payload,
        principal=principal,
        request_id=uuid.uuid4().hex,
        event="mcp_invoke",
    )


@mcp_server.tool()
async def list_skill_analyzer_commands() -> dict[str, Any]:
    """List canonical SKILL ANALYZER commands available on this hosted Gateway."""
    principal = get_access_token()
    if principal is None:
        raise RuntimeError("Authenticated MCP principal is unavailable")
    await _enforce_rate_limit(principal)
    return {"commands": list_commands()}


transport_security = TransportSecuritySettings(
    allowed_hosts=list(settings.allowed_hosts),
    allowed_origins=list(settings.allowed_origins),
)
mcp_asgi_app = mcp_server.streamable_http_app(
    transport_security=transport_security,
)
app.mount("/", mcp_asgi_app)
