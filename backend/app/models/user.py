"""
Modelo `users`, según docs/05-database-design.md (sección USERS).

No se agregan columnas fuera de lo especificado en el documento. Nota de
compatibilidad: docs/06-api-spec.md (Register) recibe `full_name`, pero la
base de datos define `first_name` / `last_name` por separado; el split se
resuelve en app/services/auth_service.py, sin tocar el esquema.
"""

from __future__ import annotations

import uuid
from datetime import date, datetime

from sqlalchemy import Boolean, Date, DateTime, String
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy.sql import func

from app.db.base import Base


class User(Base):
    __tablename__ = "users"

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), primary_key=True, default=uuid.uuid4
    )

    email: Mapped[str] = mapped_column(String, unique=True, nullable=False, index=True)
    email_verified: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False)

    # Nullable: usuarios creados vía Google Sign-In pueden no tener
    # teléfono todavía (se completa en onboarding posterior). El registro
    # tradicional (POST /auth/register) sigue exigiéndolo vía Pydantic
    # (RegisterRequest.phone es obligatorio), no a nivel de columna.
    phone: Mapped[str | None] = mapped_column(String, unique=True, nullable=True, index=True)
    phone_verified: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False)

    # Nullable: un usuario creado vía Google Sign-In puede no tener password.
    password_hash: Mapped[str | None] = mapped_column(String, nullable=True)

    google_id: Mapped[str | None] = mapped_column(String(255), nullable=True, unique=True)

    first_name: Mapped[str] = mapped_column(String, nullable=False)
    last_name: Mapped[str] = mapped_column(String, nullable=False)

    last_login_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)
    birth_date: Mapped[date | None] = mapped_column(Date, nullable=True)
    avatar_url: Mapped[str | None] = mapped_column(String, nullable=True)

    is_active: Mapped[bool] = mapped_column(Boolean, nullable=False, default=True)
    is_deleted: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False)

    last_seen_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)
    timezone: Mapped[str] = mapped_column(String(100), nullable=False, default="America/Bogota")

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), nullable=False, server_default=func.now()
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False,
        server_default=func.now(),
        onupdate=func.now(),
    )