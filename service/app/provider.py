from __future__ import annotations

from typing import Any

import httpx

from service.app.config import Settings


class ProviderError(RuntimeError):
    def __init__(self, code: str, http_status: int = 502) -> None:
        super().__init__(code)
        self.code = code
        self.http_status = http_status


def provider_name(base_url: str) -> str:
    return httpx.URL(base_url).host or "configured-provider"


async def generate_completion(
    settings: Settings,
    *,
    system_prompt: str,
    user_prompt: str,
) -> tuple[str, dict[str, Any]]:
    if not settings.provider_ready:
        raise ProviderError("provider_not_configured", 503)

    endpoint = settings.llm_base_url.rstrip("/") + "/chat/completions"
    payload = {
        "model": settings.llm_model,
        "messages": [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt},
        ],
        "temperature": 0.2,
        "max_tokens": settings.llm_max_output_tokens,
    }
    headers = {
        "Authorization": f"Bearer {settings.llm_api_key}",
        "Content-Type": "application/json",
    }

    try:
        async with httpx.AsyncClient(
            timeout=httpx.Timeout(settings.llm_timeout_seconds, connect=10.0),
            follow_redirects=False,
        ) as client:
            response = await client.post(endpoint, json=payload, headers=headers)
    except httpx.TimeoutException as exc:
        raise ProviderError("provider_timeout", 504) from exc
    except httpx.HTTPError as exc:
        raise ProviderError("provider_connection_error", 502) from exc

    if response.status_code in {401, 403}:
        raise ProviderError("provider_authentication_failed", 502)
    if response.status_code == 429:
        raise ProviderError("provider_rate_limited", 503)
    if response.status_code >= 500:
        raise ProviderError("provider_unavailable", 503)
    if response.status_code >= 400:
        raise ProviderError("provider_request_rejected", 502)

    try:
        body = response.json()
        content = body["choices"][0]["message"]["content"]
    except (ValueError, KeyError, IndexError, TypeError) as exc:
        raise ProviderError("provider_invalid_response", 502) from exc

    if isinstance(content, list):
        content = "\n".join(
            str(part.get("text", "")) if isinstance(part, dict) else str(part)
            for part in content
        )
    if not isinstance(content, str) or not content.strip():
        raise ProviderError("provider_empty_response", 502)

    usage = body.get("usage", {})
    safe_usage = {
        "input_tokens": usage.get("prompt_tokens"),
        "output_tokens": usage.get("completion_tokens"),
    } if isinstance(usage, dict) else {}
    return content.strip(), safe_usage
