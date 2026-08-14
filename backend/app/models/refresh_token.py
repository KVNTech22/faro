"""
Modelo `refresh_tokens`.

No está en docs/05-database-design.md V1 (ese documento no detalla las
tablas internas de Authentication), pero es una tabla obligatoria del
sprint de Phase 2. Sigue las mismas convenciones del proyecto: UUID PK,
timestamps, y agrega lo mínimo necesario para revocación segura, según
docs/07-security.md y docs/13-authentication-design.md:

- El token en texto plano NUNCA se persiste, solo su hash SHA-256
  (`token_hash`, ver app/core/security.hash_opaque_token).
- Revocación: logout, cambio de password, cuenta desactivada.
"""

from __future__ import annotations

import uuid
from datetime import datetime

from sqlalchemy import DateTime, ForeignKey, String
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy.sql import func

from app.db.base import Base


class RefreshToken(Base):
    __tablename__ = "refresh_tokens"

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), primary_key=True, default=uuid.uuid4
    )

    user_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True
    )

    token_hash: Mapped[str] = mapped_column(String, unique=True, nullable=False, index=True)

    expires_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False)
    revoked_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), nullable=False, server_default=func.now()
    )
