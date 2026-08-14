"""
Configuración de entorno de Alembic para FARO — Foundation Layer.

Usa la URL síncrona (psycopg2) construida desde app.core.config.settings.
target_metadata apunta a app.db.base.Base, que hoy no tiene modelos:
las migraciones autogeneradas quedarán vacías hasta que se agreguen
modelos en fases posteriores.
"""

from logging.config import fileConfig

from alembic import context
from sqlalchemy import engine_from_config, pool

from app.core.config import settings
from app.db.base import Base

# Import central de modelos: registra las tablas de Authentication (y las
# de fases futuras) en Base.metadata para que --autogenerate las detecte.
# app/db/base.py permanece sin cambios (Foundation Layer intacta).
import app.models  # noqa: E402,F401

config = context.config
config.set_main_option("sqlalchemy.url", settings.DATABASE_URL_SYNC)

if config.config_file_name is not None:
    fileConfig(config.config_file_name)

target_metadata = Base.metadata


def run_migrations_offline() -> None:
    url = config.get_main_option("sqlalchemy.url")
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
    )
    with context.begin_transaction():
        context.run_migrations()


def run_migrations_online() -> None:
    connectable = engine_from_config(
        config.get_section(config.config_ini_section, {}),
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,
    )

    with connectable.connect() as connection:
        context.configure(connection=connection, target_metadata=target_metadata)
        with context.begin_transaction():
            context.run_migrations()


if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
