"""Excepciones de dominio del módulo de Authentication.

Se traducen a HTTPException dentro de app/api/auth.py, manteniendo
app/services/auth_service.py libre de detalles de FastAPI/HTTP.
"""


class AuthError(Exception):
    """Base para errores de autenticación."""


class EmailAlreadyRegisteredError(AuthError):
    pass


class PhoneAlreadyRegisteredError(AuthError):
    pass


class InvalidCredentialsError(AuthError):
    pass


class AccountInactiveError(AuthError):
    pass


class InvalidOrExpiredTokenError(AuthError):
    pass


class EmailNotVerifiedError(AuthError):
    pass


class GoogleTokenInvalidError(AuthError):
    pass
