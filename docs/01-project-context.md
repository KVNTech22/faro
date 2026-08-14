# FARO - Project Context

## Visión

FARO es una aplicación Android enfocada en la coordinación de personas durante emergencias.

Permite que familiares, amigos y grupos de confianza conozcan rápidamente el estado de sus miembros después de un evento crítico.

Inicialmente estará orientada a eventos sísmicos en Colombia.

La arquitectura debe permitir futuras expansiones hacia:

- Inundaciones
- Incendios
- Emergencias médicas
- SOS manuales

---

## Problema

Durante una emergencia:

- Las líneas telefónicas colapsan.
- Los mensajes pueden retrasarse.
- Las familias desconocen el estado de sus miembros.

FARO centraliza:

- Confirmaciones de estado.
- Ubicación.
- Información médica.
- Contactos de emergencia.

---

## Objetivos

### Principal

Reducir el tiempo necesario para saber quién está bien y quién necesita ayuda.

### Secundarios

- Compartir ubicación.
- Compartir ficha médica.
- Gestionar grupos familiares.
- Operar con conectividad limitada.

---

## Público objetivo

Grupos pequeños:

- Familias
- Parejas
- Amigos
- Vecinos

Escala inicial:

50-100 usuarios.

---

## Infraestructura

Backend:

- FastAPI

Base de datos:

- PostgreSQL

Cache y colas:

- Redis

Push:

- Firebase Cloud Messaging

Servidor:

- VPS Contabo Ubuntu 24.04

---

## Dominio

api.faro.kvnttech.com

---

## Restricciones

- Bajo consumo de batería.
- Bajo consumo de datos.
- Compatible con Google Play.
- Sin rastreo permanente.