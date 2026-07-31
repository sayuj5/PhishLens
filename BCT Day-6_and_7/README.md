<div align="center">

<img src="docs/assets/banner.png" alt="BlackFalcon Banner" width="100%" />

# 🦅 BlackFalcon

### Enterprise Vulnerability Management Platform

[![CI](https://github.com/yourusername/blackfalcon/actions/workflows/ci.yml/badge.svg)](https://github.com/yourusername/blackfalcon/actions/workflows/ci.yml)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python 3.12](https://img.shields.io/badge/python-3.12-blue.svg)](https://www.python.org/downloads/)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.111-009688.svg)](https://fastapi.tiangolo.com)
[![Next.js](https://img.shields.io/badge/Next.js-16-black.svg)](https://nextjs.org)
[![TypeScript](https://img.shields.io/badge/TypeScript-5-blue.svg)](https://www.typescriptlang.org)

**BlackFalcon is a production-ready, open-source enterprise vulnerability management platform built for authorised defensive security assessments.**

[Live Demo](#) · [Documentation](docs/) · [Report a Bug](https://github.com/yourusername/blackfalcon/issues) · [Request a Feature](https://github.com/yourusername/blackfalcon/issues)

</div>

---

> **⚠️ Authorised Use Only**: BlackFalcon is designed exclusively for **authorised** defensive security assessments on networks and systems you own or have explicit written permission to test. Unauthorised use against third-party systems is illegal and unethical. The authors accept no liability for misuse.

---

## 📋 Table of Contents

- [Overview](#-overview)
- [Key Features](#-key-features)
- [Architecture](#-architecture)
- [Technology Stack](#-technology-stack)
- [Screenshots](#-screenshots)
- [Quick Start](#-quick-start)
- [Docker Setup](#-docker-setup)
- [API Documentation](#-api-documentation)
- [Folder Structure](#-folder-structure)
- [Configuration](#️-configuration)
- [Roadmap](#️-roadmap)
- [Contributing](#-contributing)
- [Security](#-security)
- [License](#-license)

---

## 🌟 Overview

BlackFalcon is a full-stack enterprise vulnerability management platform that enables security teams to:

- **Discover** authorised network assets through automated, configurable scans
- **Inventory** hosts, services, and open ports in a centralised database
- **Assess** inventoried assets using a modular, plug-in driven vulnerability engine
- **Track** security findings through a full lifecycle (open → acknowledged → resolved)
- **Visualise** risk posture through a real-time executive dashboard
- **Report** findings and risk scores to stakeholders

Built as a portfolio project demonstrating proficiency in full-stack development, API design, asynchronous architecture, security engineering, and DevOps.

---

## ✨ Key Features

| Feature | Description |
|---------|-------------|
| 🔍 **Asset Discovery** | Asynchronous TCP port scanning with configurable profiles and concurrency |
| 📦 **Asset Inventory** | Deduplicated host database with service fingerprinting and banner grabbing |
| 🔬 **Vulnerability Assessment** | Plugin-based assessment engine with 4 built-in checks (ports, services, banners, firewall) |
| 📊 **Executive Dashboard** | Real-time KPI cards, risk trends, and severity distribution charts |
| ⚡ **WebSocket Updates** | Live scan progress and finding notifications pushed to the browser |
| 🔑 **JWT Authentication** | Secure token-based auth with role support (admin / analyst) |
| 🚦 **Rate Limiting** | Built-in brute-force protection on auth endpoints (5 req/min) |
| 🔒 **Security Headers** | HSTS, X-Frame-Options, X-Content-Type-Options automatically set |
| 🐳 **Docker Ready** | Multi-stage Dockerfiles + Docker Compose for one-command deployment |
| ☸️ **Kubernetes Ready** | Production manifests with liveness/readiness probes |
| 🔌 **Plugin System** | Write a new vulnerability check in under 20 lines of Python |
| 📝 **Audit Trail** | Full finding history with status changes and analyst notes |

---

## 🏗 Architecture

```
┌───────────────────────────────────────────────────────────────┐
│                    Next.js 16 Frontend                        │
│  Dashboard · Assets · Discovery · Findings · Risk · Settings  │
└────────────────────────┬──────────────────────────────────────┘
                         │ REST + WebSocket
┌────────────────────────▼──────────────────────────────────────┐
│                    FastAPI Backend                            │
│  Routers · Auth · Schemas · Middleware · Rate Limiting        │
├──────────────────┬────────────────────┬───────────────────────┤
│  Discovery       │  Assessment        │  WebSocket            │
│  Engine          │  Engine            │  Manager              │
│  ┌────────────┐  │  ┌──────────────┐  │                       │
│  │ Manager    │  │  │ Plugin       │  │                       │
│  │ Workers    │  │  │ Registry     │  │                       │
│  │ Scheduler  │  │  │ open_ports   │  │                       │
│  │ Providers  │  │  │ services     │  │                       │
│  └────────────┘  │  │ banners      │  │                       │
│                  │  │ firewall     │  │                       │
│                  │  └──────────────┘  │                       │
└──────────────────┴────────────────────┴───────────────────────┘
                         │
┌────────────────────────▼──────────────────────────────────────┐
│              SQLAlchemy ORM + SQLite / PostgreSQL             │
│  Users · Networks · Assets · Ports · Services · Findings      │
└───────────────────────────────────────────────────────────────┘
```

For a detailed architecture guide with Mermaid diagrams and ER diagram, see [docs/ARCHITECTURE.md](docs/ARCHITECTURE.md).

---

## 🛠 Technology Stack

### Backend
| Technology | Version | Purpose |
|-----------|---------|---------|
| Python | 3.12 | Core language |
| FastAPI | 0.111 | REST API framework |
| SQLAlchemy | 2.0 | ORM and database abstraction |
| Pydantic | v2 | Data validation and schemas |
| python-jose | 3.3 | JWT token management |
| passlib[bcrypt] | 1.7 | Password hashing |
| slowapi | 0.1.9 | Rate limiting |
| uvicorn | 0.30 | ASGI server |
| alembic | 1.13 | Database migrations |
| pytest | 8.2 | Testing framework |

### Frontend
| Technology | Version | Purpose |
|-----------|---------|---------|
| Next.js | 16 | React framework with App Router |
| React | 19 | UI library |
| TypeScript | 5 | Type safety |
| TailwindCSS | 4 | Utility-first CSS |
| @tanstack/react-query | 5 | Data fetching and cache |
| Recharts | 2 | Charting library |
| Framer Motion | 11 | Animations |
| Lucide React | 0.300 | Icon set |
| Axios | 1.6 | HTTP client |

### DevOps
| Technology | Purpose |
|-----------|---------|
| Docker | Containerisation |
| Docker Compose | Local deployment |
| Kubernetes | Production orchestration |
| GitHub Actions | CI/CD automation |

---

## 📸 Screenshots

> Screenshots coming soon. Run the project and visit `http://localhost:3000` to explore.

| Dashboard | Asset Inventory | Vulnerability Findings |
|-----------|-----------------|----------------------|
| *(screenshot)* | *(screenshot)* | *(screenshot)* |

| Discovery Engine | Risk Analytics | Assessment Jobs |
|-----------------|----------------|-----------------|
| *(screenshot)* | *(screenshot)* | *(screenshot)* |

---

## 🚀 Quick Start

### Prerequisites

- Python 3.12+
- Node.js 20+
- Git

### 1. Clone the repository

```bash
git clone https://github.com/yourusername/blackfalcon.git
cd blackfalcon/"BCT Day-6_and_7"
```

### 2. Backend setup

```bash
cd backend

# Create and activate a virtual environment
python -m venv venv
venv\Scripts\activate        # Windows
# source venv/bin/activate   # Linux/macOS

# Install dependencies
pip install -r requirements.txt

# Start the API server
uvicorn backend.main:app --reload
```

The API will be available at `http://localhost:8000`.  
Swagger docs: `http://localhost:8000/docs`

### 3. Frontend setup

```bash
cd frontend

# Install dependencies
npm install --legacy-peer-deps

# Start the development server
npm run dev
```

The dashboard will be available at `http://localhost:3000`.

### 4. Create your first admin user

```bash
# While the backend is running, POST to the register endpoint:
curl -X POST http://localhost:8000/users/register \
  -H "Content-Type: application/json" \
  -d '{"email": "admin@blackfalcon.local", "password": "Str0ngP@ss!"}'
```

### 5. Seed demonstration data

```bash
cd backend
python seed_demo.py
```

---

## 🐳 Docker Setup

The fastest way to run the full stack:

```bash
# Clone and enter the project directory
git clone https://github.com/yourusername/blackfalcon.git
cd blackfalcon/"BCT Day-6_and_7"

# Build and start all services
docker-compose up -d --build

# View logs
docker-compose logs -f
```

| Service | URL |
|---------|-----|
| Frontend Dashboard | http://localhost:3000 |
| Backend API | http://localhost:8000 |
| API Docs (Swagger) | http://localhost:8000/docs |

---

## 📡 API Documentation

The API is fully documented via OpenAPI/Swagger:

- **Interactive Docs**: `http://localhost:8000/docs`
- **ReDoc**: `http://localhost:8000/redoc`

### Key Endpoint Groups

| Prefix | Description |
|--------|-------------|
| `POST /token` | Authenticate and obtain a JWT token |
| `GET/POST /api/assets` | Asset inventory management |
| `GET/POST /api/networks` | Network CIDR management |
| `GET/POST /api/discovery` | Discovery job control |
| `GET/POST /api/assessment/jobs` | Vulnerability assessment jobs |
| `GET /api/assessment/findings` | Security findings with filters |
| `PATCH /api/assessment/findings/{id}` | Update finding status |
| `GET /api/assessment/risk-summary` | Risk analytics |
| `GET /health` | Liveness probe |
| `GET /ready` | Readiness probe |

---

## 📁 Folder Structure

```
blackfalcon/
├── .github/
│   ├── workflows/
│   │   ├── ci.yml              # PR tests and build validation
│   │   └── release.yml         # Docker image publish on tag
│   ├── ISSUE_TEMPLATE/
│   │   ├── bug_report.yml
│   │   └── feature_request.yml
│   └── PULL_REQUEST_TEMPLATE.md
├── backend/
│   ├── assessment/             # Phase 4: Vulnerability Assessment Engine
│   │   ├── plugins/
│   │   │   ├── checks/         # Assessment plugin implementations
│   │   │   ├── base.py         # BasePlugin abstract class
│   │   │   └── registry.py     # Auto-discovery plugin registry
│   │   ├── engine.py           # Async assessment runner
│   │   └── __init__.py
│   ├── discovery/              # Phase 3: Asset Discovery Engine
│   │   ├── providers/          # TCP, future cloud providers
│   │   ├── manager.py          # Worker pool manager
│   │   ├── scheduler.py        # Job scheduling
│   │   └── worker.py           # Discovery worker
│   ├── routers/                # FastAPI route handlers
│   ├── auth.py                 # JWT authentication
│   ├── database.py             # SQLAlchemy engine + session
│   ├── limiter.py              # Rate limiter singleton
│   ├── logger.py               # Structured logger configuration
│   ├── main.py                 # FastAPI app, middleware, lifespan
│   ├── models.py               # SQLAlchemy ORM models
│   ├── schemas.py              # Pydantic request/response schemas
│   ├── seed_demo.py            # Demo data seeder
│   ├── conftest.py             # Shared pytest fixtures
│   ├── test_main.py            # API health + auth + security tests
│   ├── test_assessment.py      # Plugin unit + assessment API tests
│   ├── test_discovery.py       # Discovery engine tests
│   └── requirements.txt
├── frontend/
│   ├── src/
│   │   ├── app/                # Next.js App Router pages
│   │   │   ├── dashboard/      # Executive dashboard
│   │   │   ├── assets/         # Asset inventory
│   │   │   ├── networks/       # Network management
│   │   │   ├── discovery/      # Discovery jobs
│   │   │   ├── vulnerabilities/# Findings list + detail
│   │   │   ├── assessment/     # Assessment job launcher
│   │   │   ├── risk/           # Risk analytics
│   │   │   ├── activity/       # Audit activity log
│   │   │   ├── health/         # System health page
│   │   │   └── settings/       # User settings
│   │   ├── components/         # Reusable React components
│   │   ├── contexts/           # React context providers
│   │   ├── hooks/              # Custom React hooks
│   │   └── lib/                # API client + utilities
│   ├── Dockerfile
│   └── package.json
├── docs/
│   ├── ARCHITECTURE.md         # System architecture + Mermaid diagrams
│   ├── DEPLOYMENT.md           # Docker and Kubernetes deployment
│   ├── PLUGIN_AUTHORING.md     # Guide to writing new assessment plugins
│   ├── USER_GUIDE.md           # End-user documentation
│   ├── ADMIN_GUIDE.md          # Administrator documentation
│   └── TROUBLESHOOTING.md      # Common issues and fixes
├── k8s/
│   ├── backend-deployment.yaml
│   ├── frontend-deployment.yaml
│   └── configmap.yaml
├── .github/
├── docker-compose.yml
├── README.md
├── CONTRIBUTING.md
├── CHANGELOG.md
├── CODE_OF_CONDUCT.md
├── SECURITY.md
└── LICENSE
```

---

## ⚙️ Configuration

All configuration is managed via environment variables.

| Variable | Default | Description |
|----------|---------|-------------|
| `DATABASE_URL` | `sqlite:///./blackfalcon.db` | SQLAlchemy connection string |
| `SECRET_KEY` | `supersecretkey_change_me_in_production` | JWT signing key — **must be changed** |
| `FRONTEND_URL` | `http://localhost:3000` | Allowed CORS origin |
| `NEXT_PUBLIC_API_URL` | `http://localhost:8000` | Backend URL used by the frontend |

> **Production Note**: Always set `SECRET_KEY` from a secure secret manager and replace the SQLite database with PostgreSQL.

---

## 🛣️ Roadmap

Future enhancements (not implemented, community contributions welcome):

- [ ] **PostgreSQL support** — Production database with proper migrations via Alembic
- [ ] **CVE Integration** — Map findings to NVD CVE database entries
- [ ] **Reporting Engine** — PDF / CSV export of assessment reports
- [ ] **Notification System** — Email / Slack / Teams alerts for critical findings
- [ ] **Multi-tenancy** — Isolated workspaces for different teams or clients
- [ ] **RBAC** — Granular role-based access control
- [ ] **Cloud Inventory Providers** — AWS, Azure, GCP asset discovery
- [ ] **Prometheus Metrics** — Grafana observability integration
- [ ] **SIEM Integration** — Forward events to Splunk / Elastic SIEM

---

## 🤝 Contributing

Contributions are welcome! Please read our [CONTRIBUTING.md](CONTRIBUTING.md) before submitting a PR.

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/my-feature`)
3. Commit your changes (`git commit -m 'Add my feature'`)
4. Push the branch (`git push origin feature/my-feature`)
5. Open a Pull Request

---

## 🔒 Security

If you discover a security vulnerability, please **do not** open a public issue. See [SECURITY.md](SECURITY.md) for our responsible disclosure policy.

---

## 📄 License

This project is licensed under the **MIT License** — see [LICENSE](LICENSE) for details.

---

## 👏 Credits

Built by **Sayuj** as part of the BCT (Cyber Security) Portfolio Programme.

Special thanks to:
- The [FastAPI](https://fastapi.tiangolo.com/) team
- The [Next.js](https://nextjs.org/) team
- The open-source security community

---

<div align="center">
Made with ❤️ for the security community.<br/>
⭐ Star this repo if you found it useful!
</div>
