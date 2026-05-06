# BloodChain 🩸⛓️

**BloodChain** is a decentralized, microservices-based platform designed to manage and track blood donations with high transparency, security, and real-time efficiency. By combining the power of **Blockchain (Ethereum)** for immutability and **Microservices** for scalability, BloodChain ensures a reliable supply chain for life-saving blood units.

---

## 🏗️ Architecture Overview

The system follows a **Hybrid Microservices Architecture**:
- **Synchronous Communication:** REST APIs for immediate actions (Auth, Eligibility check).
- **Asynchronous Communication:** Redis Streams for background processes (Notifications, Rewards, Data Archiving).
- **Infrastructure:** Orchestrated via **K3s (Kubernetes)** and automated through **Jenkins CI/CD**.

---

## 📂 Project Structure

```text
bloodchain/                    ← Root Repository
├── services/                  ← Microservices Layer (Independent Django Projects)
│   ├── user-management/       ← Identity & RBAC (PostgreSQL)
│   ├── donor-service/         ← Eligibility & Medical History (PostgreSQL)
│   ├── hospital-service/      ← Inventory & Blood Requests (PostgreSQL)
│   ├── blood-tracking-service/← Lifecycle & Blockchain Interface (PostgreSQL)
│   ├── notifications-service/ ← Multi-channel Alerts (Redis)
│   ├── rewards-service/       ← Gamification & Health Benefits (MongoDB)
│   ├── location-service/      ← Geospatial Intelligence (PostGIS)
│   ├── blockchain-gateway/    ← Web3 Transaction Management (Redis)
│   └── data-warehouse/        ← Analytical Reporting (ClickHouse)
│
├── infra/                     ← DevOps & Infrastructure [Finamou]
│   ├── nginx/                 ← API Gateway Configuration
│   ├── ansible/               ← Server Provisioning
│   ├── jenkins/               ← CI/CD Pipeline Definitions
│   ├── k3s/                   ← Kubernetes Manifests (Deployments, Services, Policies)
│   └── monitoring/            ← Prometheus & Grafana Dashboards
│
├── blockchain/                ← Smart Contracts & Web3 [Tenguh]
│   ├── contracts/             ← Solidity Contracts (BloodUnit.sol, Rewards.sol)
│   ├── scripts/               ← Deployment & Interaction Scripts
│   └── hardhat.config.js      ← Hardhat Configuration
│
├── templates/                 ← Global HTML Templates [Finamou]
├── static/                    ← Global Assets (CSS, JS, Images) [Finamou]
├── docs/                      ← Project Documentation & Reports
├── docker-compose.yml         ← Local Development Orchestration
└── README.md                  ← You are here
```

---

## 🛠️ Technology Stack

| Component | Technology |
| :--- | :--- |
| **Backend** | Python / Django Rest Framework |
| **Frontend** | Django Templates / Leaflet.js / Tailwind CSS |
| **Blockchain** | Ethereum / Solidity / Hardhat / Web3.py |
| **Databases** | PostgreSQL, PostGIS, MongoDB, Redis, ClickHouse |
| **DevOps** | Docker, K3s (Kubernetes), Jenkins, Nginx, Ansible |
| **Monitoring** | Prometheus, Loki, Grafana |

---

## 🚀 Getting Started (Local Development)

### 1. Prerequisites
- Docker & Docker Compose
- Python 3.11+
- Node.js (for Hardhat)

### 2. Installation
```bash
# Clone the repository
git clone https://github.com/your-repo/bloodchain.git
cd bloodchain

# Launch all services
docker-compose up --build
```

### 3. Smart Contracts
```bash
cd blockchain
npm install
npx hardhat compile
npx hardhat test
```

---

## 🤝 Collaboration Workflow

- **Tenguh (Backend/Blockchain):** Focuses on the `services/` and `blockchain/` directories. Each service is an independent Django project.
- **Finamou (Frontend/DevOps):** Focuses on `infra/`, `templates/`, `static/`, and the CI/CD pipeline.

---

## 📜 License
This project is developed for academic purposes as part of the BloodChain Healthcare Initiative.
