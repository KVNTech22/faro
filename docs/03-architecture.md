# FARO - Architecture

## Arquitectura General

Android

↓

Firebase

↓

FastAPI

↓

PostgreSQL
Redis
Workers

↓

Fuentes Sísmicas

---

## Android

Responsabilidades:

- Login
- Círculos
- Emergencias
- Ubicación
- Perfil médico
- Mascotas

---

## FastAPI

Responsabilidades:

- Autenticación
- Usuarios
- Círculos
- Eventos
- Historial

---

## PostgreSQL

Persistencia principal.

---

## Redis

- Cache
- Temporizadores
- Colas

---

## Workers

- Consulta de proveedores sísmicos
- Escalamiento
- Reenvíos

---

## Firebase

Canales:

- earthquake
- sos
- circle

---

## Seguridad

- HTTPS
- JWT
- Refresh Token
- Cloudflare
- Rate Limiting

## Responsabilidades

- Llamadas rápidas
- Integración WhatsApp
- Navegación Google Maps
- Confirmación grupal