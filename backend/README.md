# FARO — Foundation Layer

Capa de infraestructura base (FastAPI + PostgreSQL 16 + Redis + Docker +
Alembic). Sin endpoints de negocio, sin autenticación, sin modelos
funcionales. Ver `ESTRUCTURA.md` para el árbol completo.

## Instrucciones — Ubuntu 24.04

### 1. Requisitos previos

```bash
sudo apt update && sudo apt upgrade -y

# Docker Engine + Compose plugin
sudo apt install -y ca-certificates curl gnupg
sudo install -m 0755 -d /etc/apt/keyrings
curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo gpg --dearmor -o /etc/apt/keyrings/docker.gpg
sudo chmod a+r /etc/apt/keyrings/docker.gpg

echo \
  "deb [arch=$(dpkg --print-architecture) signed-by=/etc/apt/keyrings/docker.gpg] \
  https://download.docker.com/linux/ubuntu $(. /etc/os-release && echo "$VERSION_CODENAME") stable" | \
  sudo tee /etc/apt/sources.list.d/docker.list > /dev/null

sudo apt update
sudo apt install -y docker-ce docker-ce-cli containerd.io docker-buildx-plugin docker-compose-plugin

# Permitir usar docker sin sudo (requiere cerrar sesión y volver a entrar)
sudo usermod -aG docker $USER
```

### 2. Clonar / copiar el proyecto

```bash
cd ~
# copiar la carpeta faro-backend/ aquí, o clonar el repo correspondiente
cd faro-backend
```

### 3. Configurar variables de entorno

```bash
cp .env.example .env
nano .env   # completar POSTGRES_PASSWORD y REDIS_PASSWORD con valores reales
```

### 4. Levantar la infraestructura

```bash
docker compose up -d --build
docker compose ps
```

Deberías ver `faro-api`, `faro-postgres` y `faro-redis` en estado `Up`
(o `healthy`).

### 5. Verificar

```bash
curl http://localhost:8000/health
```

Respuesta esperada:

```json
{"service":"faro-api","status":"ok","database":"ok","redis":"ok"}
```

### 6. Alembic (migraciones)

El entorno de Alembic ya está configurado (`alembic.ini`, `alembic/env.py`)
y apunta a la base de datos vía las variables del `.env`. Por ahora
`app/db/base.py` no tiene modelos, así que no hay nada que migrar todavía.

Cuando existan modelos (fase siguiente), desde dentro del contenedor:

```bash
docker compose exec faro-api alembic revision --autogenerate -m "mensaje"
docker compose exec faro-api alembic upgrade head
```

O localmente, con un entorno virtual apuntando a `localhost` en el `.env`:

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
alembic upgrade head
```

### 7. Logs y apagado

```bash
docker compose logs -f faro-api
docker compose down          # detiene contenedores, conserva volúmenes
docker compose down -v       # detiene y borra volúmenes (datos de DB/Redis)
```

## Qué NO incluye esta capa

- Endpoints de negocio (alertas, círculos, dependientes, mascotas, perfil
  médico, ubicación, confirmación grupal).
- Autenticación / autorización (JWT, OAuth, roles OWNER/ADMIN/MEMBER).
- Modelos de base de datos funcionales.
- Cambios a la arquitectura definida en `docs/03-architecture.md`.

Todo eso corresponde a fases posteriores del roadmap (`docs/08-roadmap.md`,
`docs/11-development-phases.md`).
