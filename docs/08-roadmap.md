# FARO - Product Roadmap

Version: 1.0

---

# Visión

FARO será una plataforma de coordinación familiar para emergencias, diseñada inicialmente para eventos sísmicos y SOS manuales, con capacidad de expansión futura a otros tipos de emergencia.

Objetivo principal:

Permitir que familias, amigos y grupos de confianza puedan verificar rápidamente el estado de sus integrantes durante una emergencia real.

---

# MVP (Minimum Viable Product)

Objetivo:

Validar el funcionamiento completo del sistema en un entorno real con usuarios reales.

Estado:

Primera versión funcional.

---

## Infraestructura

- VPS Contabo
- Docker
- PostgreSQL
- Redis
- FastAPI
- Firebase Cloud Messaging
- Cloudflare

---

## Usuarios

- Registro por correo
- Login por correo
- Google Sign-In
- Perfil de usuario
- Foto de perfil
- Teléfono obligatorio

---

## Perfil Médico

- Tipo de sangre
- Alergias
- Medicamentos
- Discapacidades
- Información crítica

---

## Círculos

- Crear círculo
- Editar círculo
- Eliminar círculo
- Invitación por correo
- Invitación por teléfono
- Roles
- Contacto principal

---

## Dependientes

- Registro de menores
- Registro de personas dependientes
- Asociación responsable ↔ dependiente

---

## Mascotas

- Registro de mascotas
- Múltiples responsables
- Foto
- Estado durante emergencia

---

## Alertas Sísmicas

Fuentes:

- SGC
- USGS
- EMSC

Configuración:

- Magnitud mínima de alerta
- Magnitud mínima de protocolo
- Radio configurable

---

## Emergencias

- Protocolo automático
- SOS manual
- Confirmación individual
- Confirmación grupal
- Escalamiento automático

Estados:

- SAFE
- HELP
- UNCONFIRMED
- HIGH_RISK

---

## Ubicación

- Ubicación temporal
- Ubicación durante emergencias
- Caché offline
- Reenvío automático

---

## Contacto rápido

- Llamar
- WhatsApp
- SMS
- Correo

---

## Navegación

- Abrir Google Maps
- Navegar hacia usuario

---

## Seguridad

- JWT
- Refresh Tokens
- AES-256
- Auditoría
- Backups

---

# Criterios de Finalización MVP

Backend:

✓ API funcionando

✓ PostgreSQL funcionando

✓ Firebase funcionando

✓ Docker funcionando

---

Android:

✓ APK instalable

✓ Login

✓ Círculos

✓ Emergencias

✓ Ubicación

✓ Notificaciones Push

---

Pruebas:

✓ 5 usuarios reales

✓ 2 círculos distintos

✓ 1 simulacro completo

---

# V1

Objetivo:

Preparar FARO para uso continuo.

---

## Funcionalidades

- Historial de emergencias
- Dashboard mejorado
- Mejoras UX
- Gestión avanzada de perfiles
- Historial de ubicaciones temporales
- Gestión avanzada de mascotas

---

## Seguridad

- MFA
- Gestión de dispositivos
- Alertas de acceso

---

## Operación

- Monitoreo
- Métricas
- Logs avanzados

---

# V1.5

Objetivo:

Mejorar coordinación y recuperación post-evento.

---

## RF-038

Código silencioso de emergencia.

Ejemplo:

Usuario marca:

SAFE

Pero internamente:

HELP

---

## Coordinación avanzada

- Personas desaparecidas
- Mascotas desaparecidas
- Seguimiento de búsqueda

---

## Recuperación

- Centro de información familiar
- Estado de recursos básicos
- Información comunitaria

---

# V2

Objetivo:

Expandir FARO a una plataforma integral de emergencias.

---

## Nuevos canales

- WhatsApp Business API
- SMS automático
- Correo automático

---

## Nuevos tipos de emergencia

- Incendios
- Inundaciones
- Emergencias médicas
- Accidentes

---

## iOS

- Aplicación nativa
- Publicación App Store

---

## IA

- Resumen automático de situación
- Priorización de alertas
- Clasificación de incidentes

---

# Fuera de Alcance Actual

No desarrollar durante MVP:

- Chat interno
- Videollamadas
- Redes sociales
- Marketplace
- Foro comunitario
- IA conversacional
- Streaming de video

---

# Métricas de Éxito

MVP:

- 10 usuarios activos
- 3 simulacros exitosos
- 95% entrega de notificaciones push

---

V1:

- 50 usuarios activos
- 10 círculos activos
- 99% disponibilidad backend

---

V2:

- Publicación Google Play
- Publicación App Store
- Más de 100 usuarios activos

---

# Estado Actual

Fase:

PLANNING

Estado:

Arquitectura completada

Documentación completada

Desarrollo pendiente

Próximo paso:

10-infrastructure.md
Backend Setup