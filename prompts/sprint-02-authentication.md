Proyecto: FARO

Lee:

PROJECT_CONTEXT.md
CURRENT_SPRINT.md
docs/05-database-design.md
docs/06-api-spec.md
docs/07-security.md
docs/13-authentication-design.md

Foundation Layer ya está aprobada.

Implementar exclusivamente:

PHASE 2 - AUTHENTICATION

Objetivo:

Crear el módulo completo de autenticación para FARO.

Tecnologías:

- FastAPI
- PostgreSQL
- SQLAlchemy 2.x
- Alembic
- JWT
- Argon2id

Requisitos:

1. Register
2. Verify Email
3. Login
4. Refresh Token
5. Logout
6. Forgot Password
7. Reset Password
8. Google Sign-In
9. Get Current User

Reglas obligatorias:

- UUID para IDs
- Argon2id para passwords
- Access Token 15 minutos
- Refresh Token 30 días
- Refresh Token almacenado hasheado
- Email obligatorio
- Teléfono obligatorio
- Email verification requerida
- Compatible con Authentication Design
- Compatible con API Spec

Entregar:

1. Estructura de carpetas
2. SQLAlchemy Models
3. Alembic Migration
4. Pydantic Schemas
5. Services
6. Routers
7. Dependencias nuevas necesarias
8. Variables de entorno nuevas

No implementar:

- Circles
- Pets
- Dependents
- Emergency Engine
- Notifications

Solo Authentication.