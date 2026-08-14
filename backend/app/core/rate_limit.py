"""
Rate limiting básico basado en Redis para el router de Authentication.

docs/07-security.md especifica "Auth: 10 requests/min" como límite inicial
a nivel de backend (además de Cloudflare, que está fuera del alcance de
este código). Esta implementación usa un contador simple con TTL en
faro-redis, por IP + endpoint.
"""

from __future__ import annotations

from fastapi import HTTPException, Request, status
from redis.asyncio import Redis

from app.core.config import settings

_redis_client: Redis | None = None


def _get_redis() -> Redis:
    global _redis_client
    if _redis_client is None:
        _redis_client = Redis.from_url(settings.REDIS_URL, decode_responses=True)
    return _redis_client


async def enforce_rate_limit(request: Request, *, bucket: str, limit: int, window_seconds: int = 60) -> None:
    client_ip = request.client.host if request.client else "unknown"
    key = f"ratelimit:{bucket}:{client_ip}"

    redis_client = _get_redis()
    try:
        current = await redis_client.incr(key)
        if current == 1:
            await redis_client.expire(key, window_seconds)
    except Exception:
        # Si Redis no está disponible, no bloqueamos auth por un fallo de
        # infraestructura secundaria; solo se omite el rate limit local
        # (Cloudflare sigue aplicando límites en el borde).
        return

    if current > limit:
        raise HTTPException(
            status_code=status.HTTP_429_TOO_MANY_REQUESTS,
            detail="Too many requests. Please try again later.",
        )


async def auth_rate_limit(request: Request) -> None:
    """Dependencia FastAPI: 10 requests/min por IP en el router /auth."""
    await enforce_rate_limit(request, bucket="auth", limit=settings.AUTH_RATE_LIMIT_PER_MINUTE)
