# Contributing to BlackFalcon

Thank you for your interest in contributing! BlackFalcon is an open-source project and we welcome contributions of all kinds: code, documentation, bug reports, and feature suggestions.

---

## 🚦 Before You Start

1. **Check existing issues** — your idea or bug may already be tracked.
2. **Open an issue first** for significant changes so we can discuss the approach before you invest time writing code.
3. **Read the Security Policy** in [SECURITY.md](SECURITY.md) — security issues must never be filed as public issues.

---

## 🔧 Development Setup

### Prerequisites

- Python 3.12+
- Node.js 20+
- Git

### Clone and Install

```bash
git clone https://github.com/yourusername/blackfalcon.git
cd blackfalcon/"BCT Day-6_and_7"

# Backend
cd backend
python -m venv venv && venv\Scripts\activate
pip install -r requirements.txt

# Frontend
cd ../frontend
npm install --legacy-peer-deps
```

### Running Tests

```bash
# Backend tests
backend\venv\Scripts\python.exe -m pytest backend/ -v --ignore=backend/venv

# Frontend type-check
cd frontend && npx tsc --noEmit
```

---

## 🌿 Branch Naming

| Type | Example |
|------|---------|
| Feature | `feature/add-csv-export` |
| Bug fix | `fix/login-rate-limit` |
| Documentation | `docs/update-deployment-guide` |
| Refactor | `refactor/discovery-manager` |

---

## 📝 Commit Messages

Follow the [Conventional Commits](https://www.conventionalcommits.org/) specification:

```
feat(assessment): add CVE lookup to banner plugin
fix(auth): resolve token expiry edge case
docs(readme): add Docker setup screenshots
test(plugins): add edge case for excessive ports
```

---

## 🔌 Writing a New Assessment Plugin

Adding a vulnerability check is intentionally simple. See the full guide: [docs/PLUGIN_AUTHORING.md](docs/PLUGIN_AUTHORING.md).

### Checklist

- [ ] Plugin placed in `backend/assessment/plugins/checks/`
- [ ] Subclasses `BasePlugin`
- [ ] Has a unique `PLUGIN_ID`
- [ ] `run()` is `async`
- [ ] Returns `List[FindingData]` (never raises)
- [ ] Unit tests in `backend/test_assessment.py`

---

## ✅ Pull Request Checklist

Before opening a PR, verify:

- [ ] Code follows existing style conventions
- [ ] New functions have docstrings
- [ ] Tests pass: `pytest backend/ -v --ignore=backend/venv`
- [ ] TypeScript type-check passes: `npx tsc --noEmit`
- [ ] No `TODO` or `FIXME` comments left in code
- [ ] Relevant docs updated if you changed behaviour
- [ ] `CHANGELOG.md` updated under `[Unreleased]`

---

## 🏛 Code of Conduct

This project adheres to the [Contributor Covenant Code of Conduct](CODE_OF_CONDUCT.md). By participating, you are expected to uphold this standard.
