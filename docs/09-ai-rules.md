# FARO - AI Collaboration Rules

Version: 1.0

---

# Objetivo

Permitir el trabajo simultáneo de múltiples modelos de IA sobre el mismo repositorio.

Objetivos:

- Reducir consumo de tokens.
- Mantener consistencia.
- Evitar código duplicado.
- Evitar cambios incompatibles.
- Mantener una arquitectura única.

---

# Documentos Fuente de Verdad

Antes de realizar cualquier cambio, la IA debe revisar:

docs/

01-project-context.md
02-requirements.md
03-architecture.md
04-user-flows.md
05-database-design.md
06-api-spec.md
07-security.md
08-roadmap.md

---

# Prohibiciones

La IA NO puede:

- Inventar endpoints.
- Inventar tablas.
- Inventar roles.
- Modificar arquitectura.
- Cambiar tecnologías.

Sin aprobación explícita.

---

# Tecnologías Congeladas

Frontend:

Android
Kotlin
Jetpack Compose

Backend:

FastAPI

Base de Datos:

PostgreSQL

Cache:

Redis

Push:

Firebase Cloud Messaging

Infraestructura:

Docker
Ubuntu 24.04
Contabo VPS

DNS:

Cloudflare

---

# Gestión de Cambios

Cualquier cambio deberá indicar:

Motivo

Impacto

Archivos afectados

Compatibilidad

---

# Convención de Commits

Formato:

TYPE: descripción

Ejemplos:

feat: add emergency contacts

fix: resolve login validation

docs: update api specification

refactor: improve earthquake service

---

# Convención de Branches

main

Producción estable.

docs

Documentación.

backend

FastAPI.

android

Aplicación Android.

feature/*

Funcionalidades temporales.

---

# Regla de Compatibilidad

Toda implementación debe ser compatible con:

05-database-design.md

06-api-spec.md

07-security.md

---

# Gestión de Tokens

La IA debe responder:

- Directo.
- Sin explicaciones innecesarias.
- Sin tutoriales extensos.

Priorizar:

- Código.
- Decisiones.
- Soluciones.

---

# Context Bootstrap

Si una nueva IA entra al proyecto:

Leer:

01-project-context.md

02-requirements.md

03-architecture.md

05-database-design.md

06-api-spec.md

Resumen esperado:

- Qué es FARO.
- Cómo funciona.
- Base de datos.
- API.
- Infraestructura.

---

# Responsabilidades por IA

## Claude

Responsable principal:

- Arquitectura
- Backend
- FastAPI
- PostgreSQL
- Docker

No modificar:

Android UI

---

## Gemini

Responsable principal:

- Android
- Kotlin
- Jetpack Compose
- Firebase Android

No modificar:

Backend

---

## ChatGPT

Responsable principal:

- Auditoría
- Revisión
- Seguridad
- Consistencia
- QA

Puede revisar cualquier módulo.

---

# Prioridad de Decisiones

1. Documentación
2. Base de datos
3. API
4. Backend
5. Android

Nunca al revés.

---

# Definition of Done

Una tarea está terminada cuando:

- Compila.
- Tiene validaciones.
- Tiene manejo de errores.
- Respeta API.
- Respeta Database Design.
- Respeta Security.

---

# Entrega Obligatoria

Cada cambio debe incluir:

Qué se hizo.

Archivos modificados.

Riesgos.

Siguientes pasos.