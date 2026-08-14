# FARO — Foundation Layer — Árbol de Carpetas

```
faro-backend/
├── app/
│   ├── __init__.py
│   ├── main.py                  # Entry point FastAPI (health check únicamente)
│   ├── core/
│   │   ├── __init__.py
│   │   ├── config.py             # Settings (pydantic-settings), lee .env
│   │   └── database.py           # Engine + SessionLocal (SQLAlchemy async)
│   ├── db/
│   │   ├── __init__.py
│   │   └── base.py               # Base declarativa (target_metadata para Alembic)
│   └── api/
│       ├── __init__.py
│       └── health.py             # Router /health (único endpoint permitido)
├── alembic/
│   ├── versions/                 # Migraciones (vacío por ahora)
│   ├── env.py                    # Configurado para autogenerate + async
│   └── script.py.mako
├── alembic.ini
├── docker-compose.yml
├── Dockerfile
├── requirements.txt
├── .env.example
├── .dockerignore
├── .gitignore
└── README.md
```

## Notas de diseño

- **app/api/health.py** es el único router incluido en esta capa. No contiene
  lógica de negocio: solo confirma que la API, la base de datos y Redis
  responden. Esto NO es autenticación ni un endpoint funcional — es
  infraestructura de arranque necesaria para verificar que el Foundation
  Layer está vivo.
- **app/db/base.py** define únicamente `Base` (declarative base) sin ningún
  modelo. Los modelos funcionales (Circulos, Dependientes, Mascotas, etc.)
  se agregan en la siguiente fase, no aquí.
- **alembic/** queda configurado y funcional pero `versions/` se entrega
  vacío — la primera migración real se generará cuando existan modelos.
- No se incluye ningún módulo de auth, JWT, OAuth, ni tablas de usuarios.
