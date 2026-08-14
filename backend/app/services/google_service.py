"""
Verificación de Google ID Tokens para Google Sign-In.

docs/13-authentication-design.md:
- El email debe venir verificado por Google.
- Si el email ya existe, las cuentas se enlazan (no se crean duplicados).
"""

from __future__ import annotations

from dataclasses import dataclass

from google.auth.transport import requests as google_requests
from google.oauth2 import id_token as google_id_token

from app.core.config import settings
from app.core.exceptions import GoogleTokenInvalidError


@dataclass
class GoogleUserInfo:
    google_id: str
    email: str
    email_verified: bool
    first_name: str
    last_name: str


def verify_google_id_token(raw_id_token: str) -> GoogleUserInfo:
    try:
        payload = google_id_token.verify_oauth2_token(
            raw_id_token,
            google_requests.Request(),
            audience=settings.GOOGLE_CLIENT_ID or None,
        )
    except Exception as exc:  # token inválido, expirado, audience incorrecta, etc.
        raise GoogleTokenInvalidError(str(exc)) from exc

    if not payload.get("email_verified", False):
        raise GoogleTokenInvalidError("Google email is not verified")

    return GoogleUserInfo(
        google_id=payload["sub"],
        email=payload["email"].strip().lower(),
        email_verified=True,
        first_name=payload.get("given_name", ""),
        last_name=payload.get("family_name", ""),
    )