"""
Router de Authentication. Prefijo /auth, montado bajo /api/v1 en app/main.py
(coincide con la Base URL de docs/06-api-spec.md:
https://api.faro.kvnttech.com/api/v1).

Endpoints (los 9 del sprint, tomados literalmente de docs/06-api-spec.md):
  POST /auth/register
  POST /auth/verify-email
  POST /auth/login
  POST /auth/refresh
  POST /auth/logout
  POST /auth/forgot-password
  POST /auth/reset-password
  POST /auth/google
  GET  /auth/me
"""

from __future__ import annotations

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.deps.auth import get_current_user
from app.core.database import get_db
from app.core.exceptions import (
    AccountInactiveError,
    EmailAlreadyRegisteredError,
    GoogleTokenInvalidError,
    InvalidCredentialsError,
    InvalidOrExpiredTokenError,
    PhoneAlreadyRegisteredError,
)
from app.core.rate_limit import auth_rate_limit
from app.models.user import User
from app.schemas.auth import (
    AccessTokenResponse,
    CurrentUserResponse,
    ForgotPasswordRequest,
    GoogleSignInRequest,
    GoogleSignInResponse,
    LoginRequest,
    LogoutRequest,
    MessageResponse,
    RefreshTokenRequest,
    RegisterRequest,
    RegisterResponse,
    ResetPasswordRequest,
    TokenResponse,
    VerifyEmailRequest,
)
from app.services import auth_service
from app.services.google_service import verify_google_id_token

router = APIRouter(prefix="/auth", tags=["authentication"], dependencies=[Depends(auth_rate_limit)])


@router.post("/register", response_model=RegisterResponse, status_code=status.HTTP_201_CREATED)
async def register(payload: RegisterRequest, db: AsyncSession = Depends(get_db)) -> RegisterResponse:
    try:
        await auth_service.register_user(
            db,
            email=payload.email,
            password=payload.password,
            phone=payload.phone,
            full_name=payload.full_name,
        )
    except EmailAlreadyRegisteredError:
        raise HTTPException(status.HTTP_409_CONFLICT, "Email is already registered") from None
    except PhoneAlreadyRegisteredError:
        raise HTTPException(status.HTTP_409_CONFLICT, "Phone is already registered") from None

    return RegisterResponse(message="User registered successfully", email_verification_sent=True)


@router.post("/verify-email", response_model=MessageResponse)
async def verify_email(payload: VerifyEmailRequest, db: AsyncSession = Depends(get_db)) -> MessageResponse:
    try:
        await auth_service.verify_email(db, raw_token=payload.token)
    except InvalidOrExpiredTokenError:
        raise HTTPException(status.HTTP_400_BAD_REQUEST, "Invalid or expired verification token") from None

    return MessageResponse(message="Email verified successfully")


@router.post("/login", response_model=TokenResponse)
async def login(payload: LoginRequest, db: AsyncSession = Depends(get_db)) -> TokenResponse:
    try:
        user = await auth_service.authenticate_user(db, email=payload.email, password=payload.password)
    except InvalidCredentialsError:
        raise HTTPException(status.HTTP_401_UNAUTHORIZED, "Invalid email or password") from None
    except AccountInactiveError:
        raise HTTPException(status.HTTP_403_FORBIDDEN, "Account is inactive") from None

    access_token, refresh_token, expires_in = await auth_service.issue_token_pair(db, user)
    return TokenResponse(access_token=access_token, refresh_token=refresh_token, expires_in=expires_in)


@router.post("/refresh", response_model=AccessTokenResponse)
async def refresh(payload: RefreshTokenRequest, db: AsyncSession = Depends(get_db)) -> AccessTokenResponse:
    try:
        access_token, expires_in = await auth_service.refresh_access_token(
            db, raw_refresh_token=payload.refresh_token
        )
    except InvalidOrExpiredTokenError:
        raise HTTPException(status.HTTP_401_UNAUTHORIZED, "Invalid or expired refresh token") from None

    return AccessTokenResponse(access_token=access_token, expires_in=expires_in)


@router.post("/logout", response_model=MessageResponse)
async def logout(
    payload: LogoutRequest,
    db: AsyncSession = Depends(get_db),
    _current_user: User = Depends(get_current_user),
) -> MessageResponse:
    await auth_service.revoke_refresh_token(db, raw_refresh_token=payload.refresh_token)
    return MessageResponse(message="Logged out successfully")


@router.post("/forgot-password", response_model=MessageResponse)
async def forgot_password(
    payload: ForgotPasswordRequest, db: AsyncSession = Depends(get_db)
) -> MessageResponse:
    # Mensaje genérico siempre, exista o no el email (anti account-enumeration).
    await auth_service.request_password_reset(db, email=payload.email)
    return MessageResponse(message="Password reset email sent")


@router.post("/reset-password", response_model=MessageResponse)
async def reset_password(
    payload: ResetPasswordRequest, db: AsyncSession = Depends(get_db)
) -> MessageResponse:
    try:
        await auth_service.reset_password(db, raw_token=payload.token, new_password=payload.new_password)
    except InvalidOrExpiredTokenError:
        raise HTTPException(status.HTTP_400_BAD_REQUEST, "Invalid or expired reset token") from None

    return MessageResponse(message="Password updated successfully")


@router.post("/google", response_model=GoogleSignInResponse)
async def google_sign_in(
    payload: GoogleSignInRequest, db: AsyncSession = Depends(get_db)
) -> GoogleSignInResponse:
    try:
        google_user = verify_google_id_token(payload.id_token)
    except GoogleTokenInvalidError:
        raise HTTPException(status.HTTP_401_UNAUTHORIZED, "Invalid Google token") from None

    user, is_new_user = await auth_service.sign_in_with_google(db, google_user)
    access_token, refresh_token, expires_in = await auth_service.issue_token_pair(db, user)

    return GoogleSignInResponse(
        access_token=access_token,
        refresh_token=refresh_token,
        expires_in=expires_in,
        is_new_user=is_new_user,
    )


@router.get("/me", response_model=CurrentUserResponse)
async def get_me(current_user: User = Depends(get_current_user)) -> CurrentUserResponse:
    return CurrentUserResponse(
        id=current_user.id,
        email=current_user.email,
        full_name=f"{current_user.first_name} {current_user.last_name}".strip(),
        phone=current_user.phone,
        email_verified=current_user.email_verified,
        phone_verified=current_user.phone_verified,
    )
