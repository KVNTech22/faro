"""
Base declarativa de SQLAlchemy.

IMPORTANTE (Foundation Layer):
Este archivo NO define modelos funcionales (Circulos, Dependientes,
Mascotas, PerfilMedico, etc). Solo expone `Base`, que Alembic usa como
`target_metadata` para autogenerar migraciones en fases posteriores.

Cuando se agreguen modelos en la siguiente fase, se importan aquí para
que Alembic los detecte, p. ej.:
    from app.models.circulo import Circulo  # noqa
"""

from sqlalchemy.orm import DeclarativeBase


class Base(DeclarativeBase):
    pass
