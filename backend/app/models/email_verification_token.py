"""
Modelo `email_verification_tokens`.

Igual que refresh_tokens: tabla obligatoria del sprint, no detallada en
docs/05-database-design.md V1. Solo se guarda el hash del token
(SHA-256); el valor en texto plano se envía una única vez (email).

Expiración: 24 horas (settings.EMAIL_VERIFICATION_TOKEN_EXPIRE_HOURS).
docs/13-authentication-design.md no especifica un TTL explícito para este
token (solo lo hace para el de reset de password, 15 min); 24h es un
valor razonable documentado aquí como decisión de implementación.
"""

from __future__ import annotations

import uuid
from datetime import datetime

from sqlalchemy import DateTime, ForeignKey, String
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy.sql import func

from app.db.base import Base


class EmailVerificationToken(Base):
    __tablename__ = "email_verification_tokens"

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), primary_key=True, default=uuid.uuid4
    )

    user_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True
    )

    token_hash: Mapped[str] = mapped_column(String, unique=True, nullable=False, index=True)

    expires_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False)
    used_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), nullable=False, server_default=func.now()
    )
