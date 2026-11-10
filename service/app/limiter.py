from __future__ import annotations

import asyncio
import hashlib
import time
from collections import defaultdict
from typing import Any

from service.app.config import Settings


class RateLimitBackendUnavailable(RuntimeError):
    pass


class RateLimiter:
    """Redis fixed-window limiter in production, process-local fallback for development."""

    _SCRIPT = """
    local value = redis.call('INCR', KEYS[1])
    if value == 1 then
      redis.call('EXPIRE', KEYS[1], ARGV[1])
    end
    return value
    """

    def __init__(self, settings: Settings) -> None:
        self.settings = settings
        self._redis: Any = None
        self._memory: dict[str, tuple[int, int]] = defaultdict(lambda: (0, 0))
        self._lock = asyncio.Lock()

    async def start(self) -> None:
        if self.settings.rate_limit_backend == "redis":
            try:
                from redis.asyncio import Redis

                self._redis = Redis.from_url(
                    self.settings.redis_url,
                    encoding="utf-8",
                    decode_responses=True,
                    socket_connect_timeout=3,
                    socket_timeout=3,
                    health_check_interval=30,
                )
                await self._redis.ping()
            except Exception as exc:
                raise RateLimitBackendUnavailable(
                    "Redis rate-limit backend could not be initialized"
                ) from exc

    async def close(self) -> None:
        if self._redis is not None:
            await self._redis.aclose()
            self._redis = None

    async def allow(self, principal: str) -> tuple[bool, int]:
        now = int(time.time())
        window = now // 60
        digest = hashlib.sha256(principal.encode("utf-8")).hexdigest()[:24]
        key = f"skill-analyzer:ratelimit:{digest}:{window}"
        limit = self.settings.rate_limit_per_minute

        if self.settings.rate_limit_backend == "redis":
            if self._redis is None:
                raise RateLimitBackendUnavailable("Redis rate limiter is not initialized")
            try:
                count = int(await self._redis.eval(self._SCRIPT, 1, key, 75))
            except Exception as exc:
                raise RateLimitBackendUnavailable("Redis rate limiter request failed") from exc
        else:
            async with self._lock:
                count, expires = self._memory[key]
                if expires <= now:
                    count, expires = 0, now + 75
                count += 1
                self._memory[key] = (count, expires)
                for old_key, (_, old_expiry) in list(self._memory.items()):
                    if old_expiry <= now:
                        self._memory.pop(old_key, None)

        retry_after = max(1, 60 - (now % 60))
        return count <= limit, retry_after
