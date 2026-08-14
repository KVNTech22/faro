"""
Entry point del Foundation Layer de FARO.

Solo incluye el router de health. No se registran endpoints de negocio
ni de autenticación en esta capa.
"""

from fastapi import FastAPI

from app.api.health import router as health_router
from app.core.config import settings

app = FastAPI(
    title=settings.PROJECT_NAME,
    description="FARO API — Foundation Layer",
    version="0.1.0",
)

app.include_router(health_router)
