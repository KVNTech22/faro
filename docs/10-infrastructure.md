# FARO - Infrastructure Design

Version: 1.0

---

# Objetivo

Desplegar FARO en la VPS Contabo existente sin afectar:

- Odoo
- PostgreSQL Odoo
- Otros proyectos
- Otros clientes

La infraestructura FARO será completamente aislada.

---

# Servidor Base

Proveedor:

Contabo

Sistema Operativo:

Ubuntu 24.04 LTS

Recursos:

4 vCPU
8 GB RAM
100 GB SSD

---

# Principio de Aislamiento

FARO tendrá:

- Red Docker propia
- PostgreSQL propio
- Redis propio
- Volúmenes propios
- Backups propios

No compartirá servicios internos con otros proyectos.

---

# Estructura de Directorios

/opt/faro

Dentro:

/opt/faro

backend/
database/
redis/
nginx/
backups/
logs/
docker/

---

# Docker Network

Nombre:

faro-network

Tipo:

bridge

Todos los servicios FARO vivirán aquí.

---

# Contenedores

## faro-api

Tecnología:

FastAPI

Puerto interno:

8000

Red:

faro-network

---

## faro-postgres

Tecnología:

PostgreSQL 16

Puerto interno:

5432

Red:

faro-network

Volumen:

faro-postgres-data

---

## faro-redis

Tecnología:

Redis

Puerto interno:

6379

Red:

faro-network

Volumen:

faro-redis-data

---

## faro-nginx

Tecnología:

Nginx

Responsabilidades:

- Reverse Proxy
- SSL
- Headers Seguridad

Red:

faro-network

---

# Dominios

Producción:

api.faro.kvnttech.com

---

Futuro:

admin.faro.kvnttech.com

status.faro.kvnttech.com

---

# Cloudflare

Modo:

Proxied

SSL:

Full Strict

---

Activar:

WAF

Bot Protection

Rate Limiting

DDoS Protection

Always HTTPS

---

# PostgreSQL

Base:

faro_db

Usuario:

faro_user

Contraseña:

Generada aleatoriamente

---

No compartir:

- Usuarios
- Schemas
- Bases

Con Odoo.

---

# Redis

Uso:

- Caché
- Colas
- Rate Limiting
- Jobs

Persistencia:

Sí

AOF activado

---

# Firebase

Proyecto:

FARO Production

Servicios:

Authentication
Cloud Messaging

---

# Backups

Ubicación:

/opt/faro/backups

---

## PostgreSQL

Backup diario

03:00 AM

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

# Logs

Ubicación:

/opt/faro/logs

---

Separados por servicio:

api.log

nginx.log

postgres.log

redis.log

---

# Variables de Entorno

Archivo:

.env

Nunca subir a GitHub.

---

Variables mínimas:

DATABASE_URL

REDIS_URL

JWT_SECRET

JWT_REFRESH_SECRET

AES_SECRET

FIREBASE_CREDENTIALS

SMTP_HOST

SMTP_PORT

SMTP_USER

SMTP_PASSWORD

---

# Seguridad Docker

No exponer:

5432

6379

a Internet.

---

Solo exponer:

443

80

---

# Recursos Esperados MVP

Usuarios:

50-100

---

Círculos:

20-30

---

Notificaciones:

< 1000 por día

---

Consumo estimado:

RAM:

1.5 - 2 GB

CPU:

< 1 vCPU promedio

---

# Monitoreo Futuro

V1

Agregar:

- Uptime Kuma
- Grafana
- Prometheus

---

# Recuperación

Objetivo:

RTO: 4 horas

RPO: 24 horas

---

# Estado Actual

Infraestructura:

Diseñada

Implementación:

Pendiente

Próxima Fase:

Backend Development