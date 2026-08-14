"""
Configuración base del Foundation Layer.
No contiene reglas de negocio ni parámetros de autenticación:
únicamente lo necesario para levantar API, DB y Redis.
"""

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

    # --- Proyecto ---
    PROJECT_NAME: str = "FARO"
    ENVIRONMENT: str = "development"
    API_V1_PREFIX: str = "/api/v1"

    # --- PostgreSQL ---
    POSTGRES_USER: str
    POSTGRES_PASSWORD: str
    POSTGRES_DB: str
    POSTGRES_HOST: str = "faro-postgres"
    POSTGRES_PORT: int = 5432

    # --- Redis ---
    REDIS_HOST: str = "faro-redis"
    REDIS_PORT: int = 6379
    REDIS_PASSWORD: str

    # --- Authentication (Phase 2) ---
    JWT_SECRET_KEY: str
    JWT_ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 15
    REFRESH_TOKEN_EXPIRE_DAYS: int = 30
    EMAIL_VERIFICATION_TOKEN_EXPIRE_HOURS: int = 24
    PASSWORD_RESET_TOKEN_EXPIRE_MINUTES: int = 15

    # Google Sign-In
    GOOGLE_CLIENT_ID: str = ""

    # Rate limiting (docs/07-security.md: Auth 10 req/min)
    AUTH_RATE_LIMIT_PER_MINUTE: int = 10

    # Frontend URLs usadas para construir links de verificación/reset
    # (hasta que exista un servicio de email real / deep link Android)
    EMAIL_VERIFICATION_URL_BASE: str = "https://api.faro.kvnttech.com/api/v1/auth/verify-email"
    PASSWORD_RESET_URL_BASE: str = "https://api.faro.kvnttech.com/api/v1/auth/reset-password"

    @property
    def DATABASE_URL(self) -> str:
        return (
            f"postgresql+asyncpg://{self.POSTGRES_USER}:{self.POSTGRES_PASSWORD}"
            f"@{self.POSTGRES_HOST}:{self.POSTGRES_PORT}/{self.POSTGRES_DB}"
        )

    @property
    def DATABASE_URL_SYNC(self) -> str:
        """Usada por Alembic (migraciones síncronas)."""
        return (
            f"postgresql+psycopg2://{self.POSTGRES_USER}:{self.POSTGRES_PASSWORD}"
            f"@{self.POSTGRES_HOST}:{self.POSTGRES_PORT}/{self.POSTGRES_DB}"
        )

    @property
    def REDIS_URL(self) -> str:
        return f"redis://:{self.REDIS_PASSWORD}@{self.REDIS_HOST}:{self.REDIS_PORT}/0"


settings = Settings()
