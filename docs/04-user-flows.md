# FARO - User Flows

## Flujo 1 - Sismo

Proveedor

↓

Worker

↓

FastAPI

↓

Firebase

↓

Android

↓

Usuario responde

- Estoy bien
- Necesito ayuda

---

## Flujo 2 - SOS Manual

Usuario

↓

SOS

↓

Obtención de ubicación

↓

Notificación a círculos prioritarios

↓

Seguimiento temporal

---

## Flujo 3 - Sin conexión

Usuario pulsa:

Necesito ayuda

↓

Sin internet

↓

Guardar localmente

↓

WorkManager

↓

Reconexión

↓

Envío automático

---

## Flujo 4 - Escalamiento

0 minutos

Notificación

↓

5 minutos

SIN_CONFIRMAR

↓

15 minutos

RIESGO_ALTO

↓

30 minutos

Reenvío

---

## Flujo 5 - Emergencia médica

Usuario:

AYUDA

↓

Miembros autorizados

↓

Acceso a:

- Ficha médica
- Contactos
- Ubicación

---

## Flujo 6 - Mascota

Usuario registra mascota.

Durante una emergencia:

- Nombre
- Foto
- Especie
- Información relevante

puede consultarse junto a la ficha familiar.