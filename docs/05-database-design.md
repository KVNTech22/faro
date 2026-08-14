# FARO - Database Design

## Filosofía

Principios:

- UUID en todas las entidades principales.
- Soft Delete.
- Auditoría básica.
- Timestamps UTC.
- Preparado para crecimiento.
- Preparado para múltiples tipos de emergencia.

---

# Convenciones

Todas las tablas tendrán:

created_at
updated_at

Opcionalmente:

deleted_at

---

# USERS

Representa una persona registrada.

users

id UUID PK

email VARCHAR UNIQUE

phone VARCHAR UNIQUE

password_hash VARCHAR

google_id VARCHAR NULL

first_name VARCHAR

last_name VARCHAR

birth_date DATE NULL

avatar_url VARCHAR NULL

is_active BOOLEAN

created_at
updated_at

---

# MEDICAL PROFILES

Información médica.

medical_profiles

id UUID PK

user_id UUID FK users

blood_type

allergies TEXT

medications TEXT

disabilities TEXT

medical_conditions TEXT

insurance_provider TEXT

insurance_number TEXT

critical_information TEXT

created_at
updated_at

---

# EMERGENCY CONTACTS

Contactos externos.

emergency_contacts

id UUID PK

user_id UUID FK users

name

relationship

phone

email NULL

priority

created_at
updated_at

---

# CIRCLES

Grupos familiares o de confianza.

circles

id UUID PK

name

description

image_url

created_by UUID FK users

created_at
updated_at

---

# CIRCLE MEMBERS

Relación N:N

circle_members

id UUID PK

circle_id UUID FK circles

user_id UUID FK users

role

OWNER
ADMIN
MEMBER

is_priority BOOLEAN

joined_at

created_at
updated_at

---

# DEPENDENTS

Menores o personas dependientes.

dependents

id UUID PK

guardian_user_id UUID FK users

name

birth_date

relationship

medical_notes

created_at
updated_at

---

# PETS

Mascotas.

pets

id UUID PK

name

species

breed

color

birth_date NULL

photo_url NULL

microchip_number NULL

notes TEXT

created_at
updated_at

---

# PET OWNERS

Relación N:N

pet_owners

id UUID PK

pet_id UUID FK pets

user_id UUID FK users

is_primary BOOLEAN

created_at
updated_at

---

# PET STATUS

Estado durante emergencias.

pet_statuses

id UUID PK

pet_id UUID FK pets

emergency_id UUID FK emergencies

status

SAFE
MISSING
INJURED
UNKNOWN

notes

created_at

---

# EARTHQUAKE SOURCES

Fuentes sísmicas.

earthquake_sources

id UUID PK

name

code

is_active

created_at

Ejemplos:

SGC
USGS
EMSC

---

# EARTHQUAKE EVENTS

Eventos normalizados.

earthquake_events

id UUID PK

source_id UUID FK earthquake_sources

external_event_id

magnitude

depth_km

latitude

longitude

location_name

occurred_at

created_at

INDEX:

external_event_id
occurred_at

---

# USER ALERT SETTINGS

Configuración sísmica.

user_alert_settings

id UUID PK

user_id UUID FK users

minimum_magnitude

country_code

radius_km

created_at
updated_at

notification_magnitude NUMERIC(2,1)

protocol_magnitude NUMERIC(2,1)

auto_protocol_enabled BOOLEAN

---

# DEVICE TOKENS

Firebase.

device_tokens

id UUID PK

user_id UUID FK users

platform

ANDROID

token

last_seen_at

created_at

---

# EMERGENCIES

Evento principal.

emergencies

id UUID PK

type

EARTHQUAKE
MANUAL_SOS
MEDICAL

trigger_user_id NULL

earthquake_event_id NULL

started_at

ended_at NULL

created_at

---

# USER EMERGENCY STATUS

Estado de cada usuario.

user_emergency_status

id UUID PK

emergency_id UUID FK emergencies

user_id UUID FK users

status

SAFE
HELP
UNCONFIRMED
HIGH_RISK

updated_at

---

# USER LOCATIONS

Ubicaciones temporales.

user_locations

id UUID PK

user_id UUID FK users

emergency_id UUID FK emergencies

latitude

longitude

accuracy

captured_at

created_at

INDEX:

user_id
captured_at

---

# OFFLINE QUEUE

Eventos pendientes de sincronizar.

offline_queue

id UUID PK

user_id UUID FK users

action_type

payload JSONB

created_at

processed_at NULL

---

# INVITATIONS

Invitaciones.

invitations

id UUID PK

circle_id UUID FK circles

email NULL

phone NULL

invited_by UUID FK users

status

PENDING
ACCEPTED
EXPIRED

expires_at

created_at

---

# AUDIT LOGS

Auditoría.

audit_logs

id UUID PK

user_id UUID NULL

action

entity_type

entity_id

payload JSONB

created_at

---

# FUTURO (V2)

No implementar todavía.

- WhatsApp Messages
- SMS Messages
- Push Delivery Logs
- Hospitals
- Shelters
- Volunteers

# STATUS CONFIRMATIONS

Registro de confirmaciones realizadas por terceros.

status_confirmations

id UUID PK

emergency_id UUID FK emergencies

confirmed_user_id UUID FK users

confirmed_by_user_id UUID FK users

status

SAFE
HELP

created_at