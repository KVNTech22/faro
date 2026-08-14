"""
Endpoint de salud del Foundation Layer.

No es un endpoint de negocio ni de autenticación: únicamente confirma
que faro-api está arriba y que puede alcanzar faro-postgres y faro-redis.
Sirve para validar el arranque de la infraestructura.
"""

from fastapi import APIRouter, Depends
from redis.asyncio import Redis
from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.config import settings
from app.core.database import get_db

router = APIRouter(tags=["health"])


@router.get("/health")
async def health_check(db: AsyncSession = Depends(get_db)) -> dict:
    db_status = "ok"
    redis_status = "ok"

    try:
        await db.execute(text("SELECT 1"))
    except Exception:
        db_status = "unavailable"

    try:
        redis_client = Redis.from_url(settings.REDIS_URL)
        await redis_client.ping()
        await redis_client.close()
    except Exception:
        redis_status = "unavailable"

    return {
        "service": "faro-api",
        "status": "ok",
        "database": db_status,
        "redis": redis_status,
    }
