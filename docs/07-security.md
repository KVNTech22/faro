# FARO - Security Specification

Version: 1.0 MVP

---

# Objetivos

Proteger:

- Información personal.
- Datos médicos.
- Datos de menores.
- Ubicaciones.
- Tokens de acceso.
- Datos de emergencia.

Principios:

- Privacy by Design.
- Least Privilege.
- Encryption by Default.
- Auditability.
- Secure Backups.

---

# Authentication

## JWT Access Token

Duración:

15 minutos

Contenido:

- user_id
- email
- role

---

## Refresh Token

Duración:

30 días

Almacenado:

- Hash en base de datos
- Nunca en texto plano

---

## Revocación

Se invalidan cuando:

- Logout
- Cambio de contraseña
- Cuenta desactivada

---

# Password Policy

Mínimo:

8 caracteres

Recomendado:

- Mayúscula
- Minúscula
- Número

Hash:

Argon2id

Nunca:

MD5
SHA1
SHA256 simple

---

# Encryption

## Datos sensibles

Cifrado AES-256-GCM

Aplicar a:

medical_profiles

- allergies
- medications
- disabilities
- medical_conditions
- critical_information

---

emergency_contacts

- phone
- email

---

dependents

- medical_notes

---

critical_information

Todo el contenido

---

# Encryption Keys

Variables de entorno

Nunca:

- GitHub
- Código fuente
- APK

---

# Authorization

Roles:

OWNER
ADMIN
MEMBER

---

# Circle Permissions

OWNER

- Todo

ADMIN

- Gestionar miembros
- Gestionar emergencias

MEMBER

- Participar
- Confirmar estado

---

# Sensitive Data Access

Información médica:

Solo visible para:

- Propietario
- Personas autorizadas
- Situaciones de emergencia

---

Información de menores:

Solo responsables autorizados.

---

# Location Privacy

Ubicación NO permanente.

Solo se captura:

- Emergencia activa
- SOS activo

---

Frecuencia:

Cada 2 minutos

Duración:

10 minutos

---

Retención

Ubicaciones:

90 días máximo

Luego:

Eliminación automática

---

# Audit Logs

Registrar:

- Login
- Logout
- Cambio de contraseña
- Cambio de rol
- Acceso médico
- Emergencias
- Confirmaciones

---

# Rate Limiting

Cloudflare

+

Backend

---

Límites iniciales:

Auth:

10 requests/min

API:

60 requests/min

SOS:

20 requests/min

---

# Device Security

Firebase Token:

- Asociado a usuario
- Revocable

Eliminar token cuando:

- Logout
- Cambio dispositivo

---

# Backup Policy

PostgreSQL

Backup:

Diario

Retención:

30 días

---

Backup semanal

Retención:

6 meses

---

Backup mensual

Retención:

1 año

---

# Disaster Recovery

Objetivo:

Recuperar servicio en menos de 4 horas.

RPO:

24 horas

---

# Infrastructure Security

Cloudflare

Activar:

- SSL Full Strict
- WAF
- Bot Protection
- Rate Limiting

---

Backend

- HTTPS obligatorio
- HTTP redireccionado

---

Docker

- Contenedores aislados
- Redes privadas
- Secrets por variables entorno

---

# Logging

No registrar:

- Contraseñas
- Tokens
- Información médica

Sí registrar:

- IDs
- Eventos
- Estados

---

# Compliance

Preparado para:

- Habeas Data (Colombia)
- GDPR básico
- Google Play Data Safety

---

# Incident Response

Ante acceso sospechoso:

- Invalidar sesiones
- Registrar auditoría
- Notificar usuario

---

# Future Security (V2)

- MFA
- Passkeys
- WebAuthn
- Device Trust
- Security Dashboard