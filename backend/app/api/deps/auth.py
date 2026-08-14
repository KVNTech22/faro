"""
Dependencia FastAPI que resuelve el usuario autenticado a partir del
Authorization: Bearer <access_token>.
"""

from __future__ import annotations

import uuid

import jwt
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import get_db
from app.core.security import decode_access_token
from app.models.user import User
from app.services.auth_service import get_user_by_id

# tokenUrl es solo documentación para el esquema OpenAPI (Swagger "Authorize").
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="api/v1/auth/login", auto_error=False)

_CREDENTIALS_EXCEPTION = HTTPException(
    status_code=status.HTTP_401_UNAUTHORIZED,
    detail="Could not validate credentials",
    headers={"WWW-Authenticate": "Bearer"},
)


async def get_current_user(
    token: str | None = Depends(oauth2_scheme),
    db: AsyncSession = Depends(get_db),
) -> User:
    if token is None:
        raise _CREDENTIALS_EXCEPTION

    try:
        payload = decode_access_token(token)
    except jwt.PyJWTError:
        raise _CREDENTIALS_EXCEPTION from None

    if payload.get("type") != "access":
        raise _CREDENTIALS_EXCEPTION

    user_id_raw = payload.get("sub")
    if user_id_raw is None:
        raise _CREDENTIALS_EXCEPTION

    try:
        user_id = uuid.UUID(user_id_raw)
    except ValueError:
        raise _CREDENTIALS_EXCEPTION from None

    user = await get_user_by_id(db, user_id)
    if user is None or not user.is_active:
        raise _CREDENTIALS_EXCEPTION

    return user
