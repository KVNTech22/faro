"""
Servicio de envío de emails — STUB para Phase 2 (Authentication).

Fuera de alcance de este sprint: proveedor real de email (SES, SendGrid,
Postmark, etc). Esta capa existe para que auth_service.py no dependa de
un proveedor concreto: hoy solo registra (log) el envío; integrar un
proveedor real es un cambio aislado a este archivo, sin tocar routers,
services de negocio ni modelos.

En desarrollo, el link se imprime en el log del contenedor faro-api para
poder probar el flujo end-to-end sin infraestructura de correo.
"""

from __future__ import annotations

import logging

from app.core.config import settings

logger = logging.getLogger("faro.email")


async def send_verification_email(*, to_email: str, raw_token: str) -> None:
    link = f"{settings.EMAIL_VERIFICATION_URL_BASE}?token={raw_token}"
    logger.info("Email verification link for %s: %s", to_email, link)


async def send_password_reset_email(*, to_email: str, raw_token: str) -> None:
    link = f"{settings.PASSWORD_RESET_URL_BASE}?token={raw_token}"
    logger.info("Password reset link for %s: %s", to_email, link)
