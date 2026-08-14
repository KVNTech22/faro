# FARO - Requirements

## Usuarios

RF-001 Registro por:

- Correo y contraseña
- Google Sign-In

RF-002 Datos obligatorios:

- Nombre
- Correo
- Teléfono

RF-003 Perfil médico:

- Tipo de sangre
- Alergias
- Medicamentos
- Discapacidades
- Condiciones médicas
- Contactos de emergencia

---

## Círculos

RF-004 Un usuario puede pertenecer a múltiples círculos.

RF-005 Cualquier usuario puede crear círculos.

RF-006 Roles:

- OWNER
- ADMIN
- MEMBER

RF-007 Círculos prioritarios configurables.

---

## Emergencias

RF-008 Recepción de eventos sísmicos.

RF-009 Confirmación rápida:

- Estoy bien
- Necesito ayuda

RF-010 SOS manual.

RF-011 Historial.

RF-012 Dashboard familiar.

---

## Estados

- BIEN
- AYUDA
- SIN_CONFIRMAR
- INCOMUNICADO
- RIESGO_ALTO

---

## Escalamiento

5 minutos:

SIN_CONFIRMAR

15 minutos:

RIESGO_ALTO

30 minutos:

Reenvío de alerta

---

## Offline

RF-013 Almacenar eventos localmente.

RF-014 Reintentar automáticamente.

---

## Ubicación

RF-015 Solo durante emergencias.

RF-016 Seguimiento temporal:

- Cada 2 minutos
- Durante 10 minutos

---

## Ficha médica

RF-017 Visible únicamente durante emergencias activas.

---

## Filtros sísmicos

RF-018 Magnitud mínima configurable.

Mínimo:

2.0

RF-019 Alcance configurable:

- País
- Radio personalizado

---

## Contactos externos

RF-020 Contactos de confianza sin cuenta FARO.

---

## Menores

RF-021 Relación responsable-dependiente.

---

## Mascotas

RF-022 Registro de mascotas.

Ficha independiente.