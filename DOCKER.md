# Docker Deployment Guide 🐳

Quick guide for deploying FlowAI Studio using Docker.

---

## Prerequisites

**Required:**
- Docker 20.10+ ([Install Docker](https://docs.docker.com/get-docker/))
- Docker Compose 2.0+

**Verify:**
```bash
docker --version
docker-compose --version
```

---

## Docker Services

**4 Services:**
- Frontend (React + Nginx) - Port 80
- Backend (FastAPI) - Port 8080
- PostgreSQL - Port 5433
- ChromaDB - Port 8000

---

## Dockerfiles

### Frontend (`frontend/Dockerfile`)
```dockerfile
# Build stage
FROM node:20-alpine AS builder
WORKDIR /app
COPY package*.json ./
RUN npm ci
COPY . .
RUN npm run build

# Production stage
FROM nginx:alpine
COPY --from=builder /app/dist /usr/share/nginx/html
COPY nginx.conf /etc/nginx/conf.d/default.conf
EXPOSE 80
CMD ["nginx", "-g", "daemon off;"]
```

### 2. Backend Container

**Image**: Custom build from `backend/Dockerfile`

**Technology**: 
- PyBackend (`backend/Dockerfile`)
# Install system dependencies
RUN apt-get update && apt-get install -y \
    gcc \
    postgresql-client \
    && rm -rf /var/lib/apt/lists/*

# Install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application
COPY . .

# Create necessary directories
RUN mkdir -p /app/uploads /app/chroma_data

EXPOSE 8080

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8080"]
```

### 3. PostgreSQL Container

**Image**: `postgres:15-alpine`

**Features**:
- Alpine-based for smaller size
- Persistent volume for data
- Health check configured
- Automatic initialization

**Configuration**:
- User: postgres
- Password: postgres
- Dvironment

Create `backend/.env`:

```bash
# Required
GEMINI_API_KEY=your_gemini_api_key_here

# Database (use Docker service names)
DATABASE_URL=postgresql://postgres:postgres@postgres:5432/workflow_db

# ChromaDB (use Docker service names)
CHROMA_HOST=chromadb
CHROMA_PORT=8000

# CORS Origins
ALLOWED_ORIGINS=["http://localhost:3000","http://localhost:80","http://localhost"]

# Optional
LLMQuick Setup

### 1. Configure Environment

Create `backend/.env`:
```bash
GEMINI_API_KEY=your_key_here
DATABASE_URL=postgresql://postgres:postgres@postgres:5432/workflow_db
CHROMA_HOST=chromadb
CHROMA_PORT=8000
ALLOWED_ORIGINS=["http://localhost:3000","http://localhost:80","http://localhost"]
```

### 2. Build and Start

```bash
# Build images
docker-compose build

# Start all services
docker-compose up -d

# Initialize database
docker-compose exec backend alembic stamp head
```

### 3. Verify

```bash
docker-compose ps
curl http://localhost:8080/health
```

**Access:**
- Frontend: http://localhost
- API Docs: http://localhost:8080/docs
PORT=8080

# === File Upload Settings ===
UPLOAD_DIR=./uploads
MAX_UPLOAD_SIZE=10485760  # 10MB
```

### Docker Compose Configuration

Key settings in `docker-compose.yml`:

```yaml
version: '3.8'

services:
  # PostgreSQL Database
  postgres:
    image: postgres:15-alpine
    container_name: workflow_postgres
    environment:
      POSTGRES_USER: postgres
      POSTGRES_PASSWORD: postgres
      POSTGRES_DB: workflow_db
    ports:
      - "5433:5432"
    volumes:
      - postgres_data:/var/lib/postgresql/data
    healthcheck:
      test: ["CMD-SHELL", "pg_isready -U postgres"]
      interval: 10s
      timeout: 5s
      retries: 5
    networks:
      - app-network

  # ChromaDB Vector Database
  chromadb:
    image: chromadb/chroma:latest
    container_name: workflow_chromadb
    ports:
      - "8000:8000"
    volumes:
      - chroma_data:/chroma/chroma
    environment:
      - IS_PERSISTENT=TRUE
    networks:
      - app-network

  # Backend API
  backend:
    build:
      context: ./backend

### Execute Commands in Containers

```bash
# Access backend shell
docker-compose exec backend bash

# Run Python commands
docker-compose exec backend python -c "print('Hello')"

# Run database migrations
docker-compose exec backend alembic upgrade head

# Access PostgreSQL
docker-compose exec postgres psql -U postgres -d workflow_db

# Check backend Python version
docker-compose exec backend python --version
```

### Rebuild Services

```bash
# Rebuild all services
docker-compose build

# Rebuild without cache (clean build)
docker-compose build --no-cache

# Rebuild specific service
docker-compose build backend

# Rebuild and restart
docker-compose up -d --build
```

---

## Networking

### Docker Network

All services communicate through a bridge network named `app-network`.

### Service Discovery

Services can reference each other by their service names:
- Backend connects to database: `postgres:5432`
- Backend connects to ChromaDB: `chromadb:8000`
- Frontend proxies to backend: `backend:8080`

### Port Mapping

| Service | Internal Port | Host Port | Purpose |
|---------|--------------|-----------|---------|
| Frontend | 80 | 80 | Web UI |
| Backend | 8080 | 8080 | API |
| PostgreSQL | 5432 | 5433 | Database |
| ChromaDB | 8000 | 8000 | Vector DB |

### CORS Configuration

Frontend can access backend through:
1. **Direct API calls**: `http://localhost:8080/api`
2. **Nginx proxy**: `/api` → `http://backend:8080/api`

Allowed origins are configured in backend `.env`:
```bash
ALLOWED_ORIGINS=["http://localhost:3000","http://localhost:80","http://localhost"]
```

---

## Volumes & Persistence

### Named Volumes

```bash
# List volumes
docker volume ls

# Inspect volume
docker volume inspect fastapiproject_postgres_data

# Remove unused volumes
docker volume prune
```

### Volume Mounts

| Volume | Mount Point | Purpose |
|--------|-------------|---------|
| `postgres_data` | `/var/lib/postgresql/data` | Database persistence |
| `chroma_data` | `/chroma/chroma` | Vector DB storage |
| `./backend/uploads` | `/app/uploads` | Uploaded PDFs |
| `./backend/chroma_data` | `/app/chroma_data` | Local ChromaDB backup |

###Common Commands

```bash
# Start services
docker-compose up -d

# Stop services
docker-compose down

# View logs
docker-compose logs -f

# Rebuild
docker-compose build --no-cache

# Check status
docker-compose ps

# Execute commands
docker-compose exec backend bash
docker-compose exec backend alembic upgrade head

# Check Nginx proxy configuration
docker-compose exec frontend cat /etc/nginx/conf.d/default.conf
```

### Network Issues

#### Services Can't Communicate

```bash
# Check all services on same network
docker network inspect fastapiproject_app-network

# Check service names resolve
docker-compose exec backend ping chromadb
docker-compose exec backend ping postgres

# Recreate network
docker-compose down
docker-compose up -d
```

### Performance Issues

#### High CPU Usage

```bash
# Check resource usage
docker stats

# Limit resources in docker-compose.yml:
services:
  backend:
    deploy:
      resources:
        limits:
          cpus: '2'
          memory: 2G
```

#### Slow Startup

```bash
# Check initialization time
docker-compose logs --timestamps backend | grep "started"

# Common causes:
# 1. Large migrations
# 2. ChromaDB initialization
# 3. Dependency downloads
```

---

## Production Deployment

### Security Best Practices

#### 1. Use Secrets for Sensitive Data

```yaml
# docker-compose.prod.yml
services:
  backend:
    environment:
      - GEMINI_API_KEY_FILE=/run/secrets/gemini_api_key
    secrets:
      - gemini_api_key

secrets:
  gemini_api_key:
    file: ./secrets/gemini_api_key.txt
```

#### 2. Use Non-Root User

```dockerfile
# In Dockerfile
RUN adduser --disabled-password --gecos '' appuser
USER appuser
```

#### 3. Enable HTTPS

```yaml
# Use nginx with SSL
frontend:
  volumes:
    - ./nginx.prod.conf:/etc/nginx/conf.d/default.conf
    - ./certs:/etc/nginx/certs
```

#### 4. Restrict Network Access

```yaml
# Only expose necessary ports
services:
  postgres:
    # Remove ports section to keep internal only
    # ports:
    #   - "5433:5432"
```

### Environment-Specific Configuration

```bash
# Development
docker-compose -f docker-compose.yml up -d

# Production
docker-compose -f docker-compose.yml -f docker-compose.prod.yml up -d
```

### Resource Limits

```yaml
services:
  backend:
    deploy:
**Port in use:**
```bash
# Windows: netstat -ano | findstr :80
# Change port: ports: - "8080:80"
```

**Container not starting:**
```bash
docker-compose logs backend
docker-compose down -v
docker-compose build --no-cache
docker-compose up -d
```

**Database connection failed:**
```bash
docker-compose exec backend alembic stamp head
docker-compose restart backend
```

**Gemini API errors:**
- 429: Quota exceeded - wait or change key
- 401: Check GEMINI_API_KEY in .env

---

For detailed documentation: [README.md](README.md)