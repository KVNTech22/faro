"""
Utilidades criptográficas del módulo de Authentication.

- Password hashing: Argon2id (argon2-cffi), según docs/07-security.md y
  docs/13-authentication-design.md.
- JWT: access tokens (15 min) firmados con HS256.
- Tokens opacos (refresh / email-verification / password-reset): se generan
  con secrets.token_urlsafe() y SOLO se persiste su hash SHA-256 en la base
  de datos. El valor en texto plano se entrega una única vez (en la
  respuesta / email) y nunca se guarda.
"""

from __future__ import annotations

import hashlib
import secrets
from datetime import datetime, timedelta, timezone
from typing import Any

import jwt
from argon2 import PasswordHasher
from argon2.exceptions import VerifyMismatchError, VerificationError, InvalidHashError

from app.core.config import settings

# --- Password hashing (Argon2id) ---
# argon2-cffi's PasswordHasher usa Argon2id por defecto (type=argon2.Type.ID).
_password_hasher = PasswordHasher()


def hash_password(plain_password: str) -> str:
    return _password_hasher.hash(plain_password)


def verify_password(plain_password: str, password_hash: str) -> bool:
    try:
        return _password_hasher.verify(password_hash, plain_password)
    except (VerifyMismatchError, VerificationError, InvalidHashError):
        return False


def needs_rehash(password_hash: str) -> bool:
    """Permite re-hashear si cambian los parámetros de Argon2id en el futuro."""
    return _password_hasher.check_needs_rehash(password_hash)


# --- JWT (Access Token) ---


def create_access_token(*, user_id: str, email: str) -> tuple[str, datetime]:
    """
    Genera el JWT de acceso (15 minutos, ver settings.ACCESS_TOKEN_EXPIRE_MINUTES).

    Nota sobre el claim "role": docs/07-security.md especifica que el JWT
    debe incluir user_id, email y role. Sin embargo, en el esquema actual
    (docs/05-database-design.md) el rol (OWNER/ADMIN/MEMBER) vive en
    `circle_members`, es decir, es un rol POR CÍRCULO, no un rol global del
    usuario — y la tabla `users` no tiene columna `role`. Como esta fase
    NO puede modificar la base de datos ni el módulo de Circles (fuera de
    alcance), el claim `role` se omite del access token por ahora. Cuando
    se implemente el módulo de Circles, se puede añadir como claim
    contextual (p. ej. resuelto por círculo en cada request) sin romper
    este contrato.
    """
    now = datetime.now(timezone.utc)
    expires_at = now + timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)

    payload: dict[str, Any] = {
        "sub": str(user_id),
        "email": email,
        "type": "access",
        "iat": int(now.timestamp()),
        "exp": int(expires_at.timestamp()),
        "jti": secrets.token_hex(16),
    }
    token = jwt.encode(payload, settings.JWT_SECRET_KEY, algorithm=settings.JWT_ALGORITHM)
    return token, expires_at


def decode_access_token(token: str) -> dict[str, Any]:
    """Lanza jwt.PyJWTError (o subclases) si el token es inválido/expiró."""
    return jwt.decode(token, settings.JWT_SECRET_KEY, algorithms=[settings.JWT_ALGORITHM])


# --- Tokens opacos (refresh / verification / reset) ---


def generate_opaque_token() -> str:
    """Token aleatorio de alta entropía, enviado al cliente una sola vez."""
    return secrets.token_urlsafe(48)


def hash_opaque_token(raw_token: str) -> str:
    """
    SHA-256 es suficiente aquí (no es un password de baja entropía: son
    48 bytes aleatorios), y es lo que se compara en cada request de
    refresh/verify/reset. Nunca se guarda `raw_token`.
    """
    return hashlib.sha256(raw_token.encode("utf-8")).hexdigest()
