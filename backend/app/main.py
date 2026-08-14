"""
Entry point de FARO API.

Foundation Layer (Phase 1): router de health, sin prefijo, sin cambios.
Authentication (Phase 2): router /auth, montado bajo settings.API_V1_PREFIX
(/api/v1), igual que la Base URL de docs/06-api-spec.md.
"""

from fastapi import FastAPI

from app.api.auth import router as auth_router
from app.api.health import router as health_router
from app.core.config import settings

app = FastAPI(
    title=settings.PROJECT_NAME,
    description="FARO API",
    version="0.2.0",
)

# Foundation Layer — sin cambios respecto a Phase 1.
app.include_router(health_router)

# Phase 2 — Authentication.
app.include_router(auth_router, prefix=settings.API_V1_PREFIX)
