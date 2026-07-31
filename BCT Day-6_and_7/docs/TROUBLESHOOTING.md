# Troubleshooting Guide

## Common Issues

### 1. Database Locked Error (SQLite)
If you see `database is locked`, this means multiple concurrent requests are trying to write to the SQLite database simultaneously.
**Solution**: This is a limitation of SQLite. For production, please configure PostgreSQL via the `DATABASE_URL` environment variable.

### 2. WebSocket Disconnections
If real-time updates are not working, check the browser console for WebSocket connection errors.
**Solution**: Ensure your reverse proxy (e.g., Nginx) is configured to support WebSocket upgrades.

### 3. Rate Limit Exceeded
If you are locked out of the login screen with a `429 Too Many Requests` error.
**Solution**: The default limit is 5 requests per minute. Wait 60 seconds and try again.

### 4. CORS Errors
If the frontend cannot connect to the backend and the browser shows CORS policy errors.
**Solution**: Ensure the `FRONTEND_URL` environment variable on the backend matches the exact origin of your frontend (e.g., `http://localhost:3000` without a trailing slash).

## Checking Logs

**Docker**:
```bash
docker-compose logs --tail=100 -f backend
```

**Kubernetes**:
```bash
kubectl logs -l app=blackfalcon,tier=backend -f
```
