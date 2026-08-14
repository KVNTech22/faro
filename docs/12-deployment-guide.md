# FARO - Deployment Guide

Version: 1.0

---

# Entornos

development

local

staging

production

---

# Development

Windows + VSCode

Repositorio:

GitHub

---

# Production

Servidor:

Contabo Ubuntu 24.04

Ruta:

/opt/faro

---

# Docker Services

faro-api

faro-postgres

faro-redis

faro-nginx

---

# Deployment Flow

1. Push GitHub

2. Pull VPS

3. Build Containers

4. Run Migrations

5. Restart Services

---

# Rollback

Mantener siempre:

- Última imagen estable
- Último backup DB

---

# Health Checks

API

GET /health

---

# Backup Verification

Semanal:

- Restaurar backup prueba
- Verificar integridad

---

# Monitoring

Inicial:

Docker Logs

Futuro:

Grafana
Prometheus
Uptime Kuma