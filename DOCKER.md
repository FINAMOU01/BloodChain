# Docker Setup Guide for BloodChain

This guide provides instructions for building and running all 9 BloodChain services using Docker.

## 📋 Table of Contents

- [Prerequisites](#prerequisites)
- [Quick Start](#quick-start)
- [Service Overview](#service-overview)
- [Environment Variables](#environment-variables)
- [Building & Running](#building--running)
- [Troubleshooting](#troubleshooting)
- [Next Steps](#next-steps)

---

## Prerequisites

- **Docker**: v20.10+ ([Install](https://docs.docker.com/install/))
- **Docker Compose**: v2.0+ ([Install](https://docs.docker.com/compose/install/))
- **Git** (to clone the project)
- **4GB+ RAM** (minimum for local development)
- **Disk Space**: 10GB+ recommended

## Quick Start

### 1. Clone & Navigate

```bash
git clone <repository-url>
cd BloodChain
```

### 2. Setup Environment Variables

```bash
# Copy the example .env file
cp .env.example .env

# Edit with your values
code .env  # or use your preferred editor
```

**Key variables to set:**
```env
DEBUG=True
SECRET_KEY=your-unique-secret-key-here
DB_USER=postgres
DB_PASSWORD=your-secure-password
WEB3_PROVIDER_URI=https://sepolia.infura.io/v3/YOUR-PROJECT-ID
PRIVATE_KEY=your_wallet_private_key
```

### 3. Build & Start All Services

```bash
# Build all images
docker-compose build

# Start all services
docker-compose up -d

# View logs
docker-compose logs -f
```

### 4. Verify Services Are Running

```bash
# Check service status
docker-compose ps

# Test a service
curl http://localhost:8001/api/donors/  # Donor service
```

---

## Service Overview

| Service | Port | Type | Database |
|---------|------|------|----------|
| **Donor Service** | 8001 | Django REST API | PostgreSQL |
| **Hospital Service** | 8002 | Django REST API | PostgreSQL |
| **Blood Tracking Service** | 8003 | Django REST API | PostgreSQL |
| **Notifications Service** | 8004 | Django + Celery | PostgreSQL + Redis |
| **Blockchain Gateway** | 8005 | Web3 API | Redis |
| **Data Warehouse** | 8006 | Analytics Service | PostgreSQL |
| **Location Service** | 8007 | Geolocation API | PostgreSQL |
| **Rewards Service** | 8008 | Reward Management | PostgreSQL |
| **User Management** | 8009 | Authentication | PostgreSQL |
| **Nginx Proxy** | 80, 443 | Reverse Proxy | N/A |

### Infrastructure Services

- **PostgreSQL** (Port 5432) - Main database for all services
- **Redis** (Port 6379) - Message broker and cache

---

## Environment Variables

### Global Configuration

```env
# Django Settings
DEBUG=False                  # Set to True for development only
SECRET_KEY=your_secret_key   # Generate with: python -c 'from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())'

# Database
DB_HOST=postgres
DB_PORT=5432
DB_USER=postgres
DB_PASSWORD=postgres
DB_NAME=bloodchain

# Redis
REDIS_URL=redis://redis:6379/0

# Blockchain
WEB3_PROVIDER_URI=https://sepolia.infura.io/v3/YOUR-PROJECT-ID
PRIVATE_KEY=your_wallet_private_key
CONTRACT_ADDRESS=0x...

# Allowed Hosts
ALLOWED_HOSTS=localhost,127.0.0.1,.example.com
```

**Note:** Each service uses a different Redis database number to avoid conflicts:
- Donor Service: DB 1
- Hospital Service: DB 2
- Blood Tracking: DB 3
- Notifications: DB 4
- Blockchain Gateway: DB 5
- Data Warehouse: DB 6
- Location Service: DB 7
- Rewards Service: DB 8
- User Management: DB 0

---

## Building & Running

### Build Specific Service

```bash
# Build a single service
docker-compose build donor-service

# Build with no cache
docker-compose build --no-cache donor-service
```

### Run Specific Service

```bash
# Start only donor and hospital services
docker-compose up -d donor-service hospital-service

# Stop a specific service
docker-compose stop blood-tracking-service

# Remove a service container
docker-compose rm blood-tracking-service
```

### View Logs

```bash
# View logs for all services
docker-compose logs -f

# View logs for a specific service
docker-compose logs -f donor-service

# View last 100 lines
docker-compose logs --tail=100 donor-service
```

### Execute Commands in Container

```bash
# Open a bash shell in a service
docker-compose exec donor-service bash

# Run Django migrations
docker-compose exec donor-service python manage.py migrate

# Create superuser
docker-compose exec user-management python manage.py createsuperuser

# Collect static files
docker-compose exec blood-tracking-service python manage.py collectstatic --noinput
```

### Clean Up

```bash
# Stop all services
docker-compose down

# Remove all containers, networks, and volumes
docker-compose down -v

# Remove all images
docker-compose down -v --rmi all
```

---

## Troubleshooting

### Services Won't Start

**Check service health:**
```bash
docker-compose ps
docker-compose logs <service-name>
```

**Common issues:**

1. **Port Already in Use**
   ```bash
   # Change port mapping in docker-compose.yml
   # Or kill the process using the port
   lsof -i :8001  # Find process on port 8001
   ```

2. **Database Connection Failed**
   ```bash
   # Ensure PostgreSQL is healthy
   docker-compose logs postgres
   
   # Recreate database
   docker-compose down -v
   docker-compose up -d postgres
   sleep 10  # Wait for DB to initialize
   docker-compose up -d
   ```

3. **Memory Issues**
   ```bash
   # Increase Docker memory limit
   # In Docker Desktop: Settings > Resources > Memory
   ```

### Django Migration Issues

```bash
# Reset migrations (development only!)
docker-compose exec <service> python manage.py migrate <app> zero

# Re-run migrations
docker-compose exec <service> python manage.py migrate
```

### Redis Connection Issues

```bash
# Test Redis connection
docker-compose exec redis redis-cli ping

# Clear Redis cache
docker-compose exec redis redis-cli FLUSHALL
```

---

## Production Deployment

### Before Deployment

1. **Set `DEBUG=False`** in `.env`
2. **Generate strong `SECRET_KEY`:**
   ```bash
   python -c 'from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())'
   ```
3. **Configure secure database credentials**
4. **Set proper `ALLOWED_HOSTS`**
5. **Enable HTTPS** in Nginx configuration
6. **Configure environment-specific settings**

### Docker Image Optimization

All Dockerfiles use **multi-stage builds** to reduce image size:
- Build stage: Installs dependencies
- Runtime stage: Contains only runtime files

### Monitoring & Logging

The infrastructure already includes:
- **Nginx** - Reverse proxy and load balancer
- **Health checks** - Enabled on all services
- **Docker logs** - Accessible via `docker-compose logs`

---

## Next Steps

### 1. Database Initialization

```bash
# Run migrations for all services
docker-compose exec blood-tracking-service python manage.py migrate
docker-compose exec donor-service python manage.py migrate
docker-compose exec hospital-service python manage.py migrate
docker-compose exec notifications-service python manage.py migrate
docker-compose exec user-management python manage.py migrate
```

### 2. Create Superusers

```bash
docker-compose exec user-management python manage.py createsuperuser
```

### 3. Load Seed Data

```bash
# If you have seed data scripts
docker-compose exec donor-service python manage.py loaddata initial_data.json
```

### 4. Test Services

```bash
# Test each service endpoint
curl http://localhost:8001/api/  # Donor Service
curl http://localhost:8002/api/  # Hospital Service
curl http://localhost:8003/api/  # Blood Tracking
```

### 5. Configure Nginx

Edit `infra/nginx/bloodchain.conf` to add service routes and restart:
```bash
docker-compose restart nginx
```

---

## Additional Resources

- [Docker Documentation](https://docs.docker.com/)
- [Docker Compose Reference](https://docs.docker.com/compose/compose-file/)
- [Django Deployment Guide](https://docs.djangoproject.com/en/stable/howto/deployment/checklist/)
- [PostgreSQL Docker Hub](https://hub.docker.com/_/postgres/)
- [Redis Docker Hub](https://hub.docker.com/_/redis/)

---

## Support

For issues or questions:
1. Check the logs: `docker-compose logs <service>`
2. Review the Troubleshooting section above
3. Consult project documentation
4. Open an issue in the repository

---

**Last Updated:** May 15, 2026
