from __future__ import annotations

import hashlib
import hmac
import json
import logging
from datetime import datetime, timezone
from typing import Any

logger = logging.getLogger("skill_analyzer.audit")


def principal_fingerprint(subject: str, salt: str) -> str:
    key = salt.encode("utf-8") if salt else b"development-only-unstable-salt"
    return hmac.new(key, subject.encode("utf-8"), hashlib.sha256).hexdigest()[:20]


def emit_audit_event(
    *,
    event: str,
    request_id: str,
    actor: str,
    salt: str,
    command: str | None = None,
    status: str,
    duration_ms: int | None = None,
    provider: str | None = None,
    model: str | None = None,
    input_bytes: int | None = None,
    output_chars: int | None = None,
    error_code: str | None = None,
    http_status: int | None = None,
) -> None:
    """Emit metadata only. Never pass prompts, completions, tokens, or request headers."""
    record: dict[str, Any] = {
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "event": event,
        "request_id": request_id,
        "actor_fingerprint": principal_fingerprint(actor, salt),
        "status": status,
    }
    optional = {
        "command": command,
        "duration_ms": duration_ms,
        "provider": provider,
        "model": model,
        "input_bytes": input_bytes,
        "output_chars": output_chars,
        "error_code": error_code,
        "http_status": http_status,
    }
    record.update({key: value for key, value in optional.items() if value is not None})
    logger.info(json.dumps(record, separators=(",", ":"), ensure_ascii=False))
