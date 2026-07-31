# Changelog

All notable changes to BlackFalcon will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

---

## [Unreleased]

---

## [1.0.0] — 2026-07-30

### 🎉 Initial Public Release

#### Added – Phase 1: Foundation
- FastAPI backend with SQLAlchemy ORM and SQLite database
- JWT-based authentication (login, token refresh)
- User registration and role system (admin / analyst)
- Core data models: `User`, `Network`, `Asset`, `Port`, `Service`, `Tag`
- Alembic configured for future schema migrations

#### Added – Phase 2 & 3: Asset Discovery Engine
- Asynchronous TCP discovery engine with configurable worker pool
- Discovery Manager, Scheduler, Worker, and Queue components
- TCP provider for host and service detection with banner grabbing
- Scan profiles: configurable concurrency, timeout, port lists
- Scan scopes: CIDR target management
- Asset inventory with deduplication (IP, MAC, hostname)
- Full audit history for asset changes (port opened, service changed)
- WebSocket server broadcasting real-time discovery events

#### Added – Phase 3C: Enterprise Dashboard
- Executive dashboard with live KPI cards (total assets, online/offline, scans)
- Risk trend chart (Recharts)
- Severity distribution doughnut chart
- Asset distribution bar chart
- Top-risk assets table
- System health page
- Activity log page
- Asset inventory page with search and filter
- Network management page
- Discovery jobs page with real-time progress

#### Added – Phase 3D: Production Discovery Engine
- Provider abstraction layer for pluggable discovery backends
- TCP service discovery provider with version detection
- Network inventory pipeline with deduplication

#### Added – Phase 4: Vulnerability Assessment Framework
- Modular plugin architecture with `BasePlugin` abstract class and `FindingData` dataclass
- Auto-discovery plugin registry (zero-registration, just drop a file)
- Assessment Engine with async, semaphore-bounded plugin execution
- Plugin: **High-Risk Open Ports** (23 known risky services)
- Plugin: **Unencrypted/Default Services** (10 plaintext protocols)
- Plugin: **Outdated Service Banners** (regex version comparison for 10 services)
- Plugin: **Excessive Open Ports / Missing Firewall** (configurable thresholds)
- Vulnerability findings lifecycle: open → acknowledged → resolved → false_positive
- Finding history with analyst notes
- Risk score calculation and per-asset risk snapshots
- Assessment policies for controlling which plugins run
- Frontend: Vulnerabilities list, Finding detail, Assessment jobs, Risk analytics pages

#### Added – Production Hardening
- `slowapi` rate limiting (5 req/min on login)
- Strict CORS configuration (env-driven, no wildcard in production)
- `SecurityHeadersMiddleware`: HSTS, X-Frame-Options, X-Content-Type-Options, X-XSS-Protection
- `/health` (liveness) and `/ready` (readiness) Kubernetes probes
- Graceful shutdown with worker drain
- Centralised `limiter.py` singleton

#### Added – CI/CD & DevOps
- Multi-stage `Dockerfile` for backend (Python 3.12-slim + nmap)
- Multi-stage `Dockerfile` for frontend (Next.js standalone)
- `docker-compose.yml` for one-command local deployment
- Kubernetes manifests: `backend-deployment.yaml`, `frontend-deployment.yaml`, `configmap.yaml`
- GitHub Actions CI pipeline: pytest + TypeScript check + Docker build
- GitHub Actions release pipeline: push images to GHCR on git tag

#### Added – Testing
- `conftest.py` with shared in-memory SQLite fixtures
- 15 plugin unit tests covering all 4 assessment plugins
- 7 assessment API integration tests
- Health/ready endpoint tests
- Auth and rate-limiting tests
- Security header assertion tests

#### Added – Documentation
- `docs/ARCHITECTURE.md` — system design + Mermaid + ER diagrams
- `docs/DEPLOYMENT.md` — Docker and Kubernetes deployment guide
- `docs/PLUGIN_AUTHORING.md` — guide to writing new assessment plugins
- `docs/USER_GUIDE.md` — end-user documentation
- `docs/ADMIN_GUIDE.md` — administrator guide
- `docs/TROUBLESHOOTING.md` — common issues and fixes
- `README.md`, `CONTRIBUTING.md`, `CHANGELOG.md`, `LICENSE`, `SECURITY.md`, `CODE_OF_CONDUCT.md`

---

[Unreleased]: https://github.com/yourusername/blackfalcon/compare/v1.0.0...HEAD
[1.0.0]: https://github.com/yourusername/blackfalcon/releases/tag/v1.0.0
