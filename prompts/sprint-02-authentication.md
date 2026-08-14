Proyecto: FARO

Lee obligatoriamente:

PROJECT_CONTEXT.md
CURRENT_SPRINT.md
docs/05-database-design.md
docs/06-api-spec.md
docs/07-security.md
docs/13-authentication-design.md
docs/14-emergency-engine.md

Foundation Layer ya fue aprobada y no debe modificarse.

Implementar exclusivamente:

PHASE 2 - AUTHENTICATION

Objetivo:

Crear el módulo completo de autenticación para FARO.

Tecnologías obligatorias:

- FastAPI
- PostgreSQL
- SQLAlchemy 2.x
- Alembic
- JWT
- Argon2id

Funcionalidades:

1. Register
2. Verify Email
3. Login
4. Refresh Token
5. Logout
6. Forgot Password
7. Reset Password
8. Google Sign-In
9. Get Current User

Tablas obligatorias:

- users
- refresh_tokens
- email_verification_tokens
- password_reset_tokens

Todos los IDs deben ser UUID.

Todos los tokens deben almacenarse hasheados.

Nunca almacenar:

- passwords en texto plano
- refresh tokens en texto plano
- verification tokens en texto plano
- reset tokens en texto plano

Reglas obligatorias:

- Argon2id para passwords
- Access Token: 15 minutos
- Refresh Token: 30 días
- Refresh Token hasheado
- Email obligatorio
- Teléfono obligatorio
- Email verification requerida
- Compatible con docs/05-database-design.md
- Compatible con docs/06-api-spec.md
- Compatible con docs/07-security.md
- Compatible con docs/13-authentication-design.md

Entregar:

1. Estructura de carpetas
2. SQLAlchemy Models
3. Alembic Migration
4. Pydantic Schemas
5. Services
6. Routers
7. Dependencias nuevas necesarias
8. Variables de entorno nuevas
9. Flujo completo de autenticación
10. Pasos para integración futura con Firebase y Android

No implementar:

- Circles
- Pets
- Dependents
- Emergency Engine
- Notifications
- Firebase
- FCM
- SMS
- WhatsApp

No modificar:

- Arquitectura
- Base de datos fuera de Authentication
- Foundation Layer

Solo Authentication.