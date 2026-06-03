# BloodChain Microservices - Startup Order Documentation

This document outlines the correct order to start the BloodChain microservices and explains the dependencies between them.

## Service Dependencies Overview

```
┌─────────────────────────────────────────────────────────────┐
│                   Infrastructure Layer                       │
│  (PostgreSQL, Redis, Blockchain Node, Message Queue)         │
└─────────────────────────────────────────────────────────────┘
                            │
        ┌───────────────────┼───────────────────┐
        │                   │                   │
        ▼                   ▼                   ▼
┌──────────────────┐  ┌──────────────┐  ┌──────────────┐
│ Blockchain       │  │ Core Services│  │ Support      │
│ Gateway Service  │  │              │  │ Services     │
└──────────────────┘  └──────────────┘  └──────────────┘
        │                   │                   │
        │        ┌──────────┼──────────┐        │
        │        │          │          │        │
        ▼        ▼          ▼          ▼        ▼
    Blood    Hospital   Donor      Rewards   User/Location/
   Tracking  Service    Service    Service   Notifications
   Service
```

## Prerequisites - Start First (Infrastructure)

Before starting any microservices, ensure these components are running:

### 1. PostgreSQL Database
```bash
# Start PostgreSQL (if using Docker)
docker run --name bloodchain-postgres \
  -e POSTGRES_DB=bloodchain \
  -e POSTGRES_USER=postgres \
  -e POSTGRES_PASSWORD=postgres \
  -p 5432:5432 \
  -d postgres:15
```

**Purpose**: Central database for all services (donor data, hospital records, blood inventory)

### 2. Redis Cache & Message Broker
```bash
# Start Redis (if using Docker)
docker run --name bloodchain-redis \
  -p 6379:6379 \
  -d redis:7-alpine
```

**Purpose**: 
- Caching layer for all services
- Message broker for Celery async tasks (notifications)
- Session storage for authentication

### 3. Blockchain Node (Hardhat/Local Ethereum)
```bash
# In blockchain/ directory
npm install
npx hardhat node
```

**Purpose**: Local blockchain for testing smart contracts (BloodUnit.sol, Rewards.sol)

## Service Startup Order

### Phase 1: Core Gateway Service (Must Start First)

#### 1. **Blockchain Gateway Service** (Port 8009)
```bash
cd services/blockchain-gateway
pip install -r requirements.txt
python manage.py migrate
python manage.py runserver 0.0.0.0:8009
```

**Dependencies**: PostgreSQL, Redis, Blockchain Node
**Purpose**: Mediates all blockchain interactions, smart contract deployments
**Critical For**: All other services that need blockchain interaction
**Endpoints**: 
- `/api/blockchain/submit-transaction`
- `/api/blockchain/query-status`
- `/api/blockchain/contracts`

---

### Phase 2: Core Domain Services (Can Start in Any Order)

These services are independent after the Blockchain Gateway is running:

#### 2. **Hospital Service** (Port 8001)
```bash
cd services/hospital-service
pip install -r requirements.txt
python manage.py migrate
python manage.py runserver 0.0.0.0:8001
```

**Dependencies**: PostgreSQL, Redis, Blockchain Gateway
**Purpose**: Manages hospital profiles, blood requests, inventory
**Key Tables**: hospitals, blood_requests, inventory
**Features**:
- Hospital registration and management
- Blood request creation and tracking
- Blood inventory management

#### 3. **Donor Service** (Port 8002)
```bash
cd services/donor-service
pip install -r requirements.txt
python manage.py migrate
python manage.py runserver 0.0.0.0:8002
```

**Dependencies**: PostgreSQL, Redis, Blockchain Gateway
**Purpose**: Manages donor profiles, donation history, donor verification
**Key Tables**: donors, donations, donor_medical_records
**Features**:
- Donor registration and KYC
- Donation history tracking
- Eligibility verification

#### 4. **Blood Tracking Service** (Port 8003)
```bash
cd services/blood-tracking-service
pip install -r requirements.txt
python manage.py migrate
python manage.py runserver 0.0.0.0:8003
```

**Dependencies**: PostgreSQL, Redis, Blockchain Gateway
**Purpose**: Tracks blood units from donation to transfusion
**Key Tables**: blood_units, tracking_events, chain_of_custody
**Features**:
- Blood unit lifecycle management
- Immutable tracking on blockchain
- Chain of custody verification

#### 5. **Rewards Service** (Port 8004)
```bash
cd services/rewards-service
pip install -r requirements.txt
python manage.py migrate
python manage.py runserver 0.0.0.0:8004
```

**Dependencies**: PostgreSQL, Redis, Blockchain Gateway
**Purpose**: Manages reward tokens for donors and blood drives
**Key Collections** (MongoDB): rewards, transactions
**Features**:
- Reward token distribution
- Token balance management
- Transaction history

---

### Phase 3: Support Services

#### 6. **Notifications Service** (Port 8005)
```bash
cd services/notifications-service
pip install -r requirements.txt
python manage.py migrate

# Start Django application
python manage.py runserver 0.0.0.0:8005

# In another terminal, start Celery worker
celery -A config worker -l info
```

**Dependencies**: PostgreSQL, Redis, Core Services
**Purpose**: Sends notifications to hospitals and donors
**Key Features**:
- Emergency blood alerts
- Donation reminders
- Reward notifications
- Email and push notifications

**Important**: Celery worker must be running for async task processing

#### 7. **User Management Service** (Port 8006)
```bash
cd services/user-management
pip install -r requirements.txt
python manage.py migrate
python manage.py runserver 0.0.0.0:8006
```

**Dependencies**: PostgreSQL, Redis
**Purpose**: Centralized user authentication and authorization
**Features**:
- User registration
- JWT token generation
- Role-based access control

#### 8. **Location Service** (Port 8007)
```bash
cd services/location-service
pip install -r requirements.txt
python manage.py migrate
python manage.py runserver 0.0.0.0:8007
```

**Dependencies**: PostgreSQL, Redis
**Purpose**: Manages geographic locations of hospitals, blood banks, donors
**Features**:
- Geolocation queries
- Nearest facility lookup
- Location-based blood drive coordination

#### 9. **Data Warehouse Service** (Port 8008)
```bash
cd services/data-warehouse
pip install -r requirements.txt
python manage.py migrate
python manage.py runserver 0.0.0.0:8008
```

**Dependencies**: PostgreSQL, Redis
**Purpose**: Aggregates data from all services for analytics and reporting
**Features**:
- Data aggregation pipelines
- Analytics queries
- Historical data retention

---

## Docker Compose Quick Start

For development and testing, use Docker Compose to start all services:

```bash
# From project root
docker-compose up -d

# View logs
docker-compose logs -f

# Stop all services
docker-compose down
```

---

## Startup Verification Checklist

After starting all services, verify:

- [ ] PostgreSQL is accepting connections on port 5432
- [ ] Redis is available on port 6379
- [ ] Blockchain node is running on http://localhost:8545
- [ ] Blockchain Gateway responds: `curl http://localhost:8009/api/health`
- [ ] Hospital Service responds: `curl http://localhost:8001/api/health`
- [ ] Donor Service responds: `curl http://localhost:8002/api/health`
- [ ] Blood Tracking Service responds: `curl http://localhost:8003/api/health`
- [ ] Rewards Service responds: `curl http://localhost:8004/api/health`
- [ ] Notifications Service responds: `curl http://localhost:8005/api/health`
- [ ] User Management Service responds: `curl http://localhost:8006/api/health`
- [ ] Location Service responds: `curl http://localhost:8007/api/health`
- [ ] Data Warehouse responds: `curl http://localhost:8008/api/health`

---

## Inter-Service Communication

Services communicate via:

1. **REST APIs** (HTTP): Synchronous calls between services
2. **Redis Message Queue** (Celery): Asynchronous task processing
3. **Direct Database Access**: Read-only access to shared PostgreSQL
4. **Blockchain Gateway**: All blockchain operations through this service

### Important: Never Call Services Directly

Instead of direct service-to-service calls:

```python
# ❌ Don't do this:
response = requests.get('http://donor-service:8002/api/donors/1')

# ✅ Do this:
# Use service API clients or Django ORM through shared models
from donors.models import Donor
donor = Donor.objects.get(id=1)
```

---

## Troubleshooting Startup Issues

### Service won't start - "Connection refused"
- Ensure PostgreSQL is running and accessible
- Ensure Redis is running on port 6379
- Check `.env` file has correct database credentials

### Blockchain Gateway failures
- Verify blockchain node is running on port 8545
- Check blockchain wallet has sufficient funds
- Review smart contract deployment status

### Celery tasks not processing
- Ensure Redis is running (broker)
- Verify Celery worker is running for Notifications Service
- Check Celery logs for errors

### Database migration errors
- Run migrations in order: `python manage.py migrate`
- Check for pending migrations: `python manage.py showmigrations`

---

## Environment Variables

Ensure `.env` file exists with required variables (see `.env.example`):

```bash
cp .env.example .env
# Edit .env with your actual values
```

---

## Production Deployment

For production:

1. Use Docker Compose or Kubernetes
2. Set `DEBUG=False` in environment
3. Use actual database, not SQLite
4. Use environment-appropriate blockchain network
5. Set strong `SECRET_KEY` and `JWT_SECRET`
6. Use external email service (not console backend)
7. Enable HTTPS/TLS
8. Set up monitoring and alerting (Prometheus, Grafana)

---

## References

- [API Documentation](./api/API_DOCS.md)
- [Blockchain Documentation](../blockchain/README.md)
- [Docker Setup](../DOCKER.md)
- [Infrastructure Setup](../infra/setup/README.md)
