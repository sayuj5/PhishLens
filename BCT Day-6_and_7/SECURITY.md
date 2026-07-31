# Security Policy

## Supported Versions

| Version | Supported |
|---------|-----------|
| 1.0.x   | ✅        |

---

## Reporting a Vulnerability

**Please do NOT file public GitHub issues for security vulnerabilities.**

If you discover a security vulnerability in BlackFalcon, please report it responsibly:

1. **Email**: Send a detailed report to `security@yourproject.local` (replace with your actual contact)
2. **Subject**: `[SECURITY] BlackFalcon - Brief description`
3. **Include**:
   - Description of the vulnerability
   - Steps to reproduce
   - Potential impact
   - Any suggested mitigations

We will acknowledge receipt within **48 hours** and aim to provide a fix or mitigation plan within **7 days** of confirmation.

---

## Security Design Notes

BlackFalcon includes several security controls by default:

- **Authentication**: All API endpoints require a valid JWT bearer token
- **Password Hashing**: bcrypt with automatic salt via `passlib`
- **Rate Limiting**: Login endpoint limited to 5 requests/minute/IP via `slowapi`
- **CORS**: Restricted to the configured `FRONTEND_URL` — no wildcard `*` in production
- **Security Headers**: HSTS, X-Frame-Options: DENY, X-Content-Type-Options: nosniff, X-XSS-Protection
- **SQL Injection**: All queries use SQLAlchemy ORM — no raw SQL string interpolation
- **Input Validation**: All request payloads validated through Pydantic v2 schemas

---

## ⚠️ Authorised Use Disclaimer

BlackFalcon is designed **exclusively** for use on networks and systems that you own or have **explicit written permission** to assess. Using this tool against systems without authorisation is:

- Illegal in most jurisdictions
- A violation of this project's intended purpose

The authors accept **no liability** for unauthorised or malicious use.
