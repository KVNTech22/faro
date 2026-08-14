"""
Pydantic schemas para el módulo de Authentication.

Alineados con docs/06-api-spec.md (sección Authentication API) y las
reglas de docs/13-authentication-design.md (password policy, campos
obligatorios de registro, etc).
"""

from __future__ import annotations

import re
import uuid

from pydantic import BaseModel, EmailStr, Field, field_validator

_PASSWORD_MIN_LENGTH = 8
_E164_PATTERN = re.compile(r"^\+[1-9]\d{7,14}$")


def _validate_e164_phone(phone: str) -> str:
    """
    Formato oficial de teléfono: E.164 (ej. +573001234567).
    Validación centralizada — reutilizar esta función en cualquier otro
    schema que reciba un número de teléfono.
    """
    phone = phone.strip()
    if not _E164_PATTERN.match(phone):
        raise ValueError("Phone must be in E.164 format, e.g. +573001234567")
    return phone


def _validate_password_strength(password: str) -> str:
    if len(password) < _PASSWORD_MIN_LENGTH:
        raise ValueError(f"Password must be at least {_PASSWORD_MIN_LENGTH} characters long")
    if not re.search(r"[A-Z]", password):
        raise ValueError("Password must contain at least one uppercase letter")
    if not re.search(r"[a-z]", password):
        raise ValueError("Password must contain at least one lowercase letter")
    if not re.search(r"\d", password):
        raise ValueError("Password must contain at least one number")
    return password


# --- Register ---


class RegisterRequest(BaseModel):
    email: EmailStr
    password: str
    phone: str = Field(..., min_length=6, max_length=20)
    full_name: str = Field(..., min_length=2, max_length=200)

    @field_validator("email")
    @classmethod
    def normalize_email(cls, v: str) -> str:
        return v.strip().lower()

    @field_validator("password")
    @classmethod
    def validate_password(cls, v: str) -> str:
        return _validate_password_strength(v)

    @field_validator("phone")
    @classmethod
    def validate_phone(cls, v: str) -> str:
        return _validate_e164_phone(v)


class RegisterResponse(BaseModel):
    message: str
    email_verification_sent: bool


# --- Verify Email ---


class VerifyEmailRequest(BaseModel):
    token: str


class MessageResponse(BaseModel):
    message: str


# --- Login ---


class LoginRequest(BaseModel):
    email: EmailStr
    password: str

    @field_validator("email")
    @classmethod
    def normalize_email(cls, v: str) -> str:
        return v.strip().lower()


class TokenResponse(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str = "bearer"
    expires_in: int


# --- Refresh Token ---


class RefreshTokenRequest(BaseModel):
    refresh_token: str


class AccessTokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"
    expires_in: int


# --- Logout ---


class LogoutRequest(BaseModel):
    refresh_token: str


# --- Forgot / Reset Password ---


class ForgotPasswordRequest(BaseModel):
    email: EmailStr

    @field_validator("email")
    @classmethod
    def normalize_email(cls, v: str) -> str:
        return v.strip().lower()


class ResetPasswordRequest(BaseModel):
    token: str
    new_password: str

    @field_validator("new_password")
    @classmethod
    def validate_new_password(cls, v: str) -> str:
        return _validate_password_strength(v)


# --- Google Sign-In ---


class GoogleSignInRequest(BaseModel):
    id_token: str


class GoogleSignInResponse(TokenResponse):
    is_new_user: bool


# --- Current User ---


class CurrentUserResponse(BaseModel):
    id: uuid.UUID
    email: EmailStr
    full_name: str
    phone: str | None
    email_verified: bool
    phone_verified: bool

    model_config = {"from_attributes": True}