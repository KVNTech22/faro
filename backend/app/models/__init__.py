"""
Import central de modelos.

app/db/base.py define `Base` sin modelos (Foundation Layer). Este módulo
importa los modelos de Authentication para que:
  1. Alembic (autogenerate) los detecte vía Base.metadata.
  2. app/db/base.py no tenga que modificarse (Foundation Layer intacta).
"""

from app.models.email_verification_token import EmailVerificationToken  # noqa: F401
from app.models.password_reset_token import PasswordResetToken  # noqa: F401
from app.models.refresh_token import RefreshToken  # noqa: F401
from app.models.user import User  # noqa: F401

__all__ = [
    "User",
    "RefreshToken",
    "EmailVerificationToken",
    "PasswordResetToken",
]
