"""
Lógica de negocio de Authentication.

Sin dependencias de FastAPI (HTTPException, etc.) — los routers
(app/api/auth.py) traducen las excepciones de app/core/exceptions.py a
respuestas HTTP. Esto mantiene el servicio testeable de forma aislada.
"""

from __future__ import annotations

import uuid
from datetime import datetime, timedelta, timezone

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.config import settings
from app.core.exceptions import (
    AccountInactiveError,
    EmailAlreadyRegisteredError,
    InvalidCredentialsError,
    InvalidOrExpiredTokenError,
    PhoneAlreadyRegisteredError,
)
from app.core.security import (
    create_access_token,
    generate_opaque_token,
    hash_opaque_token,
    hash_password,
    verify_password,
)
from app.models.email_verification_token import EmailVerificationToken
from app.models.password_reset_token import PasswordResetToken
from app.models.refresh_token import RefreshToken
from app.models.user import User
from app.services import email_service
from app.services.google_service import GoogleUserInfo


def _split_full_name(full_name: str) -> tuple[str, str]:
    """
    docs/06-api-spec.md (Register) recibe `full_name`; docs/05-database-design.md
    define `first_name` / `last_name` por separado en `users`. Se hace un
    split simple (primer token = first_name, resto = last_name) sin alterar
    el esquema de base de datos.
    """
    parts = full_name.strip().split(maxsplit=1)
    if len(parts) == 1:
        return parts[0], ""
    return parts[0], parts[1]


async def _get_user_by_email(db: AsyncSession, email: str) -> User | None:
    result = await db.execute(select(User).where(User.email == email, User.is_deleted.is_(False)))
    return result.scalar_one_or_none()


async def _get_user_by_phone(db: AsyncSession, phone: str) -> User | None:
    result = await db.execute(select(User).where(User.phone == phone, User.is_deleted.is_(False)))
    return result.scalar_one_or_none()


async def get_user_by_id(db: AsyncSession, user_id: uuid.UUID) -> User | None:
    result = await db.execute(
        select(User).where(User.id == user_id, User.is_deleted.is_(False))
    )
    return result.scalar_one_or_none()


# --- Register + Verify Email ---


async def register_user(db: AsyncSession, *, email: str, password: str, phone: str, full_name: str) -> User:
    if await _get_user_by_email(db, email):
        raise EmailAlreadyRegisteredError(email)
    if await _get_user_by_phone(db, phone):
        raise PhoneAlreadyRegisteredError(phone)

    first_name, last_name = _split_full_name(full_name)

    user = User(
        email=email,
        phone=phone,
        password_hash=hash_password(password),
        first_name=first_name,
        last_name=last_name,
        email_verified=False,
        phone_verified=False,
        is_active=True,
    )
    db.add(user)
    await db.flush()  # obtiene user.id sin cerrar la transacción

    await _issue_email_verification_token(db, user)

    await db.commit()
    return user


async def _issue_email_verification_token(db: AsyncSession, user: User) -> None:
    raw_token = generate_opaque_token()
    expires_at = datetime.now(timezone.utc) + timedelta(
        hours=settings.EMAIL_VERIFICATION_TOKEN_EXPIRE_HOURS
    )
    db.add(
        EmailVerificationToken(
            user_id=user.id,
            token_hash=hash_opaque_token(raw_token),
            expires_at=expires_at,
        )
    )
    await email_service.send_verification_email(to_email=user.email, raw_token=raw_token)


async def verify_email(db: AsyncSession, *, raw_token: str) -> None:
    token_hash = hash_opaque_token(raw_token)
    result = await db.execute(
        select(EmailVerificationToken).where(EmailVerificationToken.token_hash == token_hash)
    )
    token_row = result.scalar_one_or_none()

    now = datetime.now(timezone.utc)
    if (
        token_row is None
        or token_row.used_at is not None
        or token_row.expires_at < now
    ):
        raise InvalidOrExpiredTokenError("email verification token")

    user = await get_user_by_id(db, token_row.user_id)
    if user is None:
        raise InvalidOrExpiredTokenError("email verification token")

    user.email_verified = True
    token_row.used_at = now
    await db.commit()


# --- Login / Tokens ---


async def authenticate_user(db: AsyncSession, *, email: str, password: str) -> User:
    user = await _get_user_by_email(db, email)
    if user is None or user.password_hash is None or not verify_password(password, user.password_hash):
        raise InvalidCredentialsError()
    if not user.is_active:
        raise AccountInactiveError()

    user.last_login_at = datetime.now(timezone.utc)
    await db.commit()
    return user


async def issue_token_pair(db: AsyncSession, user: User) -> tuple[str, str, int]:
    access_token, _ = create_access_token(user_id=str(user.id), email=user.email)

    raw_refresh_token = generate_opaque_token()
    expires_at = datetime.now(timezone.utc) + timedelta(days=settings.REFRESH_TOKEN_EXPIRE_DAYS)
    db.add(
        RefreshToken(
            user_id=user.id,
            token_hash=hash_opaque_token(raw_refresh_token),
            expires_at=expires_at,
        )
    )
    await db.commit()

    expires_in = settings.ACCESS_TOKEN_EXPIRE_MINUTES * 60
    return access_token, raw_refresh_token, expires_in


async def _get_valid_refresh_token(db: AsyncSession, raw_refresh_token: str) -> RefreshToken:
    token_hash = hash_opaque_token(raw_refresh_token)
    result = await db.execute(select(RefreshToken).where(RefreshToken.token_hash == token_hash))
    token_row = result.scalar_one_or_none()

    now = datetime.now(timezone.utc)
    if token_row is None or token_row.revoked_at is not None or token_row.expires_at < now:
        raise InvalidOrExpiredTokenError("refresh token")
    return token_row


async def refresh_access_token(db: AsyncSession, *, raw_refresh_token: str) -> tuple[str, int]:
    token_row = await _get_valid_refresh_token(db, raw_refresh_token)

    user = await get_user_by_id(db, token_row.user_id)
    if user is None or not user.is_active:
        raise InvalidOrExpiredTokenError("refresh token")

    access_token, _ = create_access_token(user_id=str(user.id), email=user.email)
    expires_in = settings.ACCESS_TOKEN_EXPIRE_MINUTES * 60
    return access_token, expires_in


async def revoke_refresh_token(db: AsyncSession, *, raw_refresh_token: str) -> None:
    """Logout. Si el token ya no es válido, se trata como no-op idempotente."""
    token_hash = hash_opaque_token(raw_refresh_token)
    result = await db.execute(select(RefreshToken).where(RefreshToken.token_hash == token_hash))
    token_row = result.scalar_one_or_none()

    if token_row is not None and token_row.revoked_at is None:
        token_row.revoked_at = datetime.now(timezone.utc)
        await db.commit()


async def revoke_all_refresh_tokens_for_user(db: AsyncSession, user_id: uuid.UUID) -> None:
    """
    Usado en cambio de contraseña / desactivación de cuenta, según
    docs/07-security.md ("Revocación: Logout, Cambio de contraseña,
    Cuenta desactivada").
    """
    now = datetime.now(timezone.utc)
    result = await db.execute(
        select(RefreshToken).where(RefreshToken.user_id == user_id, RefreshToken.revoked_at.is_(None))
    )
    for token_row in result.scalars().all():
        token_row.revoked_at = now
    await db.commit()


# --- Forgot / Reset Password ---


async def request_password_reset(db: AsyncSession, *, email: str) -> None:
    """
    No revela si el email existe o no (mismo mensaje genérico en el
    router), para evitar enumeración de cuentas.
    """
    user = await _get_user_by_email(db, email)
    if user is None:
        return

    raw_token = generate_opaque_token()
    expires_at = datetime.now(timezone.utc) + timedelta(
        minutes=settings.PASSWORD_RESET_TOKEN_EXPIRE_MINUTES
    )
    db.add(
        PasswordResetToken(
            user_id=user.id,
            token_hash=hash_opaque_token(raw_token),
            expires_at=expires_at,
        )
    )
    await db.commit()
    await email_service.send_password_reset_email(to_email=user.email, raw_token=raw_token)


async def reset_password(db: AsyncSession, *, raw_token: str, new_password: str) -> None:
    token_hash = hash_opaque_token(raw_token)
    result = await db.execute(
        select(PasswordResetToken).where(PasswordResetToken.token_hash == token_hash)
    )
    token_row = result.scalar_one_or_none()

    now = datetime.now(timezone.utc)
    if token_row is None or token_row.used_at is not None or token_row.expires_at < now:
        raise InvalidOrExpiredTokenError("password reset token")

    user = await get_user_by_id(db, token_row.user_id)
    if user is None:
        raise InvalidOrExpiredTokenError("password reset token")

    user.password_hash = hash_password(new_password)
    token_row.used_at = now
    await db.commit()

    # Invalida todas las sesiones existentes tras un cambio de contraseña.
    await revoke_all_refresh_tokens_for_user(db, user.id)


# --- Google Sign-In ---


async def sign_in_with_google(db: AsyncSession, google_user: GoogleUserInfo) -> tuple[User, bool]:
    """
    Reglas (docs/13-authentication-design.md):
    - Si existe un usuario con ese google_id, se usa.
    - Si no, pero existe un usuario con ese email, se enlaza (se setea
      google_id sobre la cuenta existente) — nunca se duplican usuarios.
    - Si no existe ninguno, se crea un usuario nuevo. `phone` es
      nullable para usuarios Google (Google no lo provee) — queda en
      NULL con `phone_verified=False` hasta que el usuario lo complete
      en un onboarding posterior (fuera de alcance de este endpoint).
      No se usan valores placeholder.
    """
    result = await db.execute(select(User).where(User.google_id == google_user.google_id))
    user = result.scalar_one_or_none()
    if user is not None:
        user.last_login_at = datetime.now(timezone.utc)
        await db.commit()
        return user, False

    existing_by_email = await _get_user_by_email(db, google_user.email)
    if existing_by_email is not None:
        existing_by_email.google_id = google_user.google_id
        existing_by_email.email_verified = True
        existing_by_email.last_login_at = datetime.now(timezone.utc)
        await db.commit()
        return existing_by_email, False

    new_user = User(
        email=google_user.email,
        phone=None,
        password_hash=None,
        google_id=google_user.google_id,
        first_name=google_user.first_name or "",
        last_name=google_user.last_name or "",
        email_verified=True,
        phone_verified=False,
        is_active=True,
        last_login_at=datetime.now(timezone.utc),
    )
    db.add(new_user)
    await db.commit()
    return new_user, True