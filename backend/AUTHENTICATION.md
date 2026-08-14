# FARO — Phase 2: Authentication

Módulo completo de autenticación. Construido **encima** del Foundation
Layer (Phase 1), sin modificarlo. No incluye Circles, Pets, Dependents,
Emergency Engine, Notifications, Firebase/FCM, SMS ni WhatsApp — eso
queda para fases posteriores.

---

## 1. Estructura de carpetas (nuevo, sobre Foundation Layer)

```
faro-backend/
├── app/
│   ├── main.py                          # [MODIFICADO] registra el router /auth bajo /api/v1
│   ├── core/
│   │   ├── config.py                    # [MODIFICADO] + settings de JWT/tokens/Google/rate-limit
│   │   ├── database.py                  # (sin cambios)
│   │   ├── security.py                  # [NUEVO] Argon2id, JWT, hashing de tokens opacos
│   │   ├── rate_limit.py                # [NUEVO] rate limit Redis (10 req/min en /auth)
│   │   └── exceptions.py                # [NUEVO] excepciones de dominio de Authentication
│   ├── models/
│   │   ├── __init__.py                  # [NUEVO] import central para Alembic autogenerate
│   │   ├── user.py                      # [NUEVO] tabla users
│   │   ├── refresh_token.py             # [NUEVO] tabla refresh_tokens
│   │   ├── email_verification_token.py  # [NUEVO] tabla email_verification_tokens
│   │   └── password_reset_token.py      # [NUEVO] tabla password_reset_tokens
│   ├── schemas/
│   │   └── auth.py                      # [NUEVO] Pydantic request/response models
│   ├── services/
│   │   ├── auth_service.py              # [NUEVO] lógica de negocio (register, login, tokens...)
│   │   ├── google_service.py            # [NUEVO] verificación de Google ID Token
│   │   └── email_service.py             # [NUEVO] stub de envío de emails (verify/reset)
│   ├── api/
│   │   ├── auth.py                      # [NUEVO] router /auth (9 endpoints)
│   │   ├── health.py                    # (sin cambios — Foundation Layer)
│   │   └── deps/
│   │       └── auth.py                  # [NUEVO] dependencia get_current_user (Bearer JWT)
│   └── db/
│       └── base.py                      # (sin cambios — Base sin modelos, tal como en Phase 1)
├── alembic/
│   ├── env.py                           # [MODIFICADO] + `import app.models` para autogenerate
│   └── versions/
│       └── 9491d9ef752d_phase_2_authentication_tables.py   # [NUEVO]
├── requirements.txt                     # [MODIFICADO] + argon2-cffi, pyjwt, google-auth, etc.
└── .env.example                         # [MODIFICADO] + variables de Authentication
```

`app/db/base.py` **no se tocó**: sigue exportando únicamente `Base`. Los
modelos se registran en `Base.metadata` importándolos desde
`app/models/__init__.py`, que a su vez es importado por `alembic/env.py`.
Así, Alembic ve las tablas nuevas sin que Foundation Layer cambie una
línea.

---

## 2. SQLAlchemy Models

| Tabla | Archivo | Notas |
|---|---|---|
| `users` | `app/models/user.py` | Exactamente los campos de `docs/05-database-design.md` (sección USERS). UUID PK, `email`/`phone` únicos, `password_hash` nullable (usuarios Google puros pueden no tener password). |
| `refresh_tokens` | `app/models/refresh_token.py` | No está en el doc V1 de base de datos (que no detalla tablas internas de auth), pero es obligatoria en el sprint. Solo guarda `token_hash` (SHA-256), nunca el token. |
| `email_verification_tokens` | `app/models/email_verification_token.py` | Igual patrón: `token_hash`, `expires_at`, `used_at`. |
| `password_reset_tokens` | `app/models/password_reset_token.py` | Igual patrón; expiración 15 min según `docs/13-authentication-design.md`. |

Todas usan `UUID` como PK (`sqlalchemy.dialects.postgresql.UUID`), timestamps
en UTC (`DateTime(timezone=True)`), y siguen la convención `created_at` /
`updated_at` de `docs/05-database-design.md`.

## 3. Alembic Migration

`alembic/versions/9491d9ef752d_phase_2_authentication_tables.py` — crea las
4 tablas anteriores con sus FKs (`ON DELETE CASCADE` hacia `users`), índices
y constraints únicos. Verificada con `alembic upgrade head --sql` (modo
offline) para confirmar que el DDL generado es correcto antes de aplicarla
contra Postgres real.

Para aplicarla:

```bash
docker compose exec faro-api alembic upgrade head
```

## 4. Pydantic Schemas

`app/schemas/auth.py` — un schema de request/response por endpoint,
alineados 1:1 con los ejemplos JSON de `docs/06-api-spec.md`. Incluye
validación de password policy (mínimo 8 caracteres, mayúscula, minúscula,
número) reutilizada en `RegisterRequest` y `ResetPasswordRequest`.

## 5. Services

`app/services/auth_service.py` concentra toda la lógica de negocio, sin
importar nada de FastAPI — recibe una `AsyncSession` y devuelve
modelos/tuplas, o lanza excepciones de `app/core/exceptions.py`. Esto
permite testear el flujo de auth sin levantar HTTP.

`app/services/google_service.py` verifica el `id_token` contra los
servidores de Google (`google-auth`), validando `email_verified` y
`audience` (`GOOGLE_CLIENT_ID`).

`app/services/email_service.py` es un **stub**: hoy solo loggea el link de
verificación/reset. Ver sección 10 para cómo reemplazarlo por un proveedor
real sin tocar el resto del módulo.

## 6. Routers

`app/api/auth.py`, montado en `app/main.py` bajo `/api/v1` (coincide con la
Base URL `https://api.faro.kvnttech.com/api/v1` de `docs/06-api-spec.md`):

| Método | Ruta | Auth requerida |
|---|---|---|
| POST | `/api/v1/auth/register` | No |
| POST | `/api/v1/auth/verify-email` | No |
| POST | `/api/v1/auth/login` | No |
| POST | `/api/v1/auth/refresh` | No (usa refresh token) |
| POST | `/api/v1/auth/logout` | Sí (Bearer access token) |
| POST | `/api/v1/auth/forgot-password` | No |
| POST | `/api/v1/auth/reset-password` | No |
| POST | `/api/v1/auth/google` | No |
| GET | `/api/v1/auth/me` | Sí (Bearer access token) |

Todo el router tiene un rate limit de 10 req/min por IP (`app/core/rate_limit.py`,
usando `faro-redis`), según `docs/07-security.md`.

## 7. Dependencias nuevas (`requirements.txt`)

```
email-validator==2.2.0      # validación de EmailStr en Pydantic
argon2-cffi==23.1.0         # hashing de password (Argon2id)
pyjwt==2.10.1                # JWT (access tokens)
google-auth==2.37.0          # verificación de Google ID Token
requests==2.32.3             # dependencia transitiva de google-auth (transport HTTP)
python-multipart==0.0.20     # requerido por OAuth2PasswordBearer (Swagger "Authorize")
```

## 8. Variables de entorno nuevas (`.env.example`)

```
JWT_SECRET_KEY=changeme_generate_a_long_random_secret   # openssl rand -hex 64
JWT_ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=15
REFRESH_TOKEN_EXPIRE_DAYS=30
EMAIL_VERIFICATION_TOKEN_EXPIRE_HOURS=24
PASSWORD_RESET_TOKEN_EXPIRE_MINUTES=15
AUTH_RATE_LIMIT_PER_MINUTE=10
GOOGLE_CLIENT_ID=
EMAIL_VERIFICATION_URL_BASE=https://api.faro.kvnttech.com/api/v1/auth/verify-email
PASSWORD_RESET_URL_BASE=https://api.faro.kvnttech.com/api/v1/auth/reset-password
```

`JWT_SECRET_KEY` es la única realmente crítica en producción — generarla con
`openssl rand -hex 64` y nunca reusar el valor de ejemplo.

## 9. Flujo completo de autenticación

### Registro + verificación de email

```
Android app                    faro-api                          DB / Redis
    |  POST /auth/register        |                                   |
    |----------------------------->|  crea User (email_verified=false) |
    |                              |  crea EmailVerificationToken      |
    |                              |  (hash del token; TTL 24h)        |
    |                              |  "envía" email (hoy: log)         |
    |<-----------------------------|  201 {message, email_verification_sent}
    |                              |                                   |
    |  usuario abre el link/token  |                                   |
    |  POST /auth/verify-email     |                                   |
    |----------------------------->|  valida hash + TTL + used_at      |
    |                              |  User.email_verified = true       |
    |<-----------------------------|  200 {message}                    |
```

Nota (`docs/13-authentication-design.md` — *Emergency Access Rules*): un
usuario sin verificar SÍ puede loguearse y recibir notificaciones de
emergencia, pero no puede crear círculos, invitar miembros, gestionar
dependientes ni configurar ajustes de emergencia. Esa restricción se
aplicará en los routers de Circles/Dependents/Alert Settings (fuera de
alcance de este sprint) usando el flag `current_user.email_verified` que
ya expone `get_current_user`.

### Login

```
POST /auth/login {email, password}
  → authenticate_user(): verifica Argon2id, chequea is_active
  → issue_token_pair():
      - access_token  (JWT, 15 min, claims: sub, email, type, iat, exp, jti)
      - refresh_token (opaco, 30 días; se persiste solo su SHA-256 en refresh_tokens)
  → 200 {access_token, refresh_token, token_type: "bearer", expires_in: 900}
```

### Uso del access token

```
GET /api/v1/auth/me
Authorization: Bearer <access_token>
  → get_current_user(): decodifica JWT, valida "type": "access", busca User por sub
  → 200 {id, email, full_name, phone, email_verified, phone_verified}
```

### Refresh

```
POST /auth/refresh {refresh_token}
  → busca por hash en refresh_tokens; valida revoked_at IS NULL y expires_at > now()
  → emite un nuevo access_token (el refresh_token NO rota en este MVP)
  → 200 {access_token, token_type, expires_in}
```

### Logout

```
POST /auth/logout  (requiere Bearer access_token)
{refresh_token}
  → marca revoked_at = now() en el refresh_token indicado
  → 200 {message: "Logged out successfully"}
```

### Forgot / Reset password

```
POST /auth/forgot-password {email}
  → SIEMPRE responde 200 con el mismo mensaje genérico (evita enumeración de cuentas)
  → si el email existe: crea PasswordResetToken (TTL 15 min) y "envía" email

POST /auth/reset-password {token, new_password}
  → valida hash + TTL + used_at
  → re-hashea password con Argon2id
  → marca el token como usado
  → revoca TODOS los refresh_tokens activos del usuario (docs/07-security.md:
    "Revocación: ... Cambio de contraseña")
```

### Google Sign-In

```
POST /auth/google {id_token}
  → verify_google_id_token(): valida firma, audience (GOOGLE_CLIENT_ID), email_verified=true
  → sign_in_with_google():
      1. si existe user con ese google_id → lo usa
      2. si no, pero existe user con ese email → LINK (setea google_id, email_verified=true)
      3. si no existe ninguno → crea usuario nuevo
         (phone es NOT NULL UNIQUE en el esquema; Google no lo provee, así
          que se genera un placeholder único "pending:<hex>" — el usuario
          deberá completarlo/verificarlo vía PUT /users/me, fuera de
          alcance de este sprint, sin modificar la base de datos)
  → issue_token_pair()
  → 200 {access_token, refresh_token, token_type, expires_in, is_new_user}
```

### Resumen de expiraciones

| Token | Duración | Almacenamiento |
|---|---|---|
| Access token (JWT) | 15 min | No se persiste (stateless) |
| Refresh token | 30 días | Hash SHA-256 en `refresh_tokens` |
| Email verification token | 24 h | Hash SHA-256 en `email_verification_tokens` |
| Password reset token | 15 min | Hash SHA-256 en `password_reset_tokens` |

---

## 10. Integración futura con Firebase y Android

Esta fase **no** implementa Firebase/FCM (explícitamente fuera de
alcance). Pasos previstos para cuando se aborde:

1. **Device Tokens (ya modelado en `docs/05-database-design.md` como
   `device_tokens`, tabla futura, no creada en este sprint)**: se
   agregará `POST /devices/token` y `DELETE /devices/token` en un router
   nuevo `app/api/devices.py`, protegido con `get_current_user` (ya
   disponible desde esta fase). Se elimina el token en logout y en
   cambio de dispositivo, según `docs/07-security.md`.

2. **Reemplazar el stub de email** (`app/services/email_service.py`) por
   un proveedor real (SES/SendGrid/Postmark) — es el único archivo que
   necesita cambiar; `auth_service.py` ya depende de su interfaz
   (`send_verification_email`, `send_password_reset_email`), no de una
   implementación concreta.

3. **Notificaciones push de emergencia** (Phase futura — Emergency
   Engine + Notifications): usarán `device_tokens` + Firebase Admin SDK
   desde el backend. El `get_current_user` de este módulo ya provee
   identidad para asociar cada token FCM a un `user_id`.

4. **Lado Android (Kotlin / Jetpack Compose)**:
   - Guardar `access_token` en memoria (ViewModel/DataStore cifrado), NO en
     `SharedPreferences` plano.
   - Guardar `refresh_token` en `EncryptedSharedPreferences` o Android
     Keystore.
   - Interceptor HTTP (OkHttp) que:
     - agrega `Authorization: Bearer <access_token>` a cada request,
     - si recibe `401`, llama a `POST /auth/refresh` una vez y reintenta,
     - si el refresh también falla, fuerza logout local y navega a Login.
   - Google Sign-In: usar Credential Manager / Google Identity Services
     de Android para obtener el `id_token`, enviarlo tal cual a
     `POST /auth/google` (la verificación ocurre en el backend, nunca en
     el cliente).
   - Tras `POST /auth/register`, mostrar pantalla "revisa tu correo" y,
     opcionalmente, un deep link `faro://verify-email?token=...` que
     Android intercepte para llamar `POST /auth/verify-email`
     directamente sin salir de la app (requiere configurar el intent
     filter y, más adelante, servir esa misma URL como fallback web).

5. **Firebase Auth vs. Authentication propio**: se decidió (
   `docs/13-authentication-design.md`) NO usar Firebase Auth como IdP
   principal — FARO mantiene su propio JWT/Argon2id. Firebase se reserva
   exclusivamente para FCM (push notifications), no para autenticación.

---

## 11. Qué NO se implementó (fuera de alcance, según el sprint)

- Circles, Pets, Dependents, Emergency Engine, Notifications.
- Firebase / FCM / SMS / WhatsApp.
- Envío real de emails (stub con logging).
- Rotación de refresh tokens en cada `/auth/refresh` (se mantiene el
  mismo refresh token hasta que expire, se revoque, o se resetee el
  password). Documentado aquí como decisión de MVP, ajustable en V2 sin
  cambios de esquema.
- Restricción efectiva de `email_verified=false` sobre endpoints de
  Circles/Dependents/Alert Settings — esos routers no existen todavía;
  `get_current_user` ya expone el campo necesario para aplicarla cuando
  se construyan.
