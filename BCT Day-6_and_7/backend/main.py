from fastapi import FastAPI, Request, Response
from fastapi.middleware.cors import CORSMiddleware
from starlette.middleware.base import BaseHTTPMiddleware
from contextlib import asynccontextmanager
import os
import time
from datetime import datetime, timezone

from slowapi import _rate_limit_exceeded_handler
from slowapi.errors import RateLimitExceeded
from backend.limiter import limiter

from backend import models
from backend.database import engine, SessionLocal
from backend.routers import users, assets, networks, dashboard, search, discovery, websockets
from backend.routers import assessment as assessment_router
from backend.assessment import seed_plugins
from backend.logger import api_logger
from backend.discovery.manager import manager

# Create all tables
models.Base.metadata.create_all(bind=engine)

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup – record boot time for uptime calculation
    app.state.start_time = time.time()
    api_logger.info("Starting BlackFalcon API...")
    await manager.start()
    api_logger.info(f"Discovery Manager started with {manager.num_workers} workers.")
    seed_plugins(SessionLocal)
    api_logger.info("Assessment plugins seeded.")
    yield
    # Graceful Shutdown – stop accepting jobs and drain workers
    api_logger.info("Graceful shutdown initiated – draining workers...")
    await manager.stop()
    api_logger.info("BlackFalcon API shutdown complete.")

app = FastAPI(title="BlackFalcon API", version="1.0.0", lifespan=lifespan)
app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)

# Secure Headers Middleware
class SecurityHeadersMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        response = await call_next(request)
        response.headers["X-Content-Type-Options"] = "nosniff"
        response.headers["X-Frame-Options"] = "DENY"
        response.headers["X-XSS-Protection"] = "1; mode=block"
        response.headers["Strict-Transport-Security"] = "max-age=31536000; includeSubDomains"
        return response

app.add_middleware(SecurityHeadersMiddleware)

# CORS middleware for frontend communication
FRONTEND_URL = os.getenv("FRONTEND_URL", "http://localhost:3000")
app.add_middleware(
    CORSMiddleware,
    allow_origins=[FRONTEND_URL],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(users.router)
app.include_router(assets.router)
app.include_router(networks.router)
app.include_router(dashboard.router)
app.include_router(search.router)
app.include_router(discovery.router)
app.include_router(websockets.router)
app.include_router(assessment_router.router)

@app.get("/")
def read_root():
    return {"message": "Welcome to the BlackFalcon API", "version": "1.0.0"}


@app.get("/health", tags=["ops"])
def health_check():
    """
    Kubernetes liveness probe.
    Returns 200 if the API process is running and responsive.
    """
    return {"status": "ok", "timestamp": datetime.now(timezone.utc).isoformat()}


@app.get("/ready", tags=["ops"])
def readiness_check(request: Request):
    """
    Kubernetes readiness probe.
    Returns 200 only if the discovery manager is running and the DB is reachable.
    """
    from backend.database import SessionLocal as _SL
    # Quick DB ping
    try:
        db = _SL()
        db.execute(models.User.__table__.select().limit(1))
        db.close()
        db_ok = True
    except Exception:
        db_ok = False

    workers_ok = manager.num_workers > 0
    uptime = round(time.time() - request.app.state.start_time, 1)

    payload = {
        "status": "ready" if db_ok and workers_ok else "degraded",
        "database": "ok" if db_ok else "error",
        "discovery_workers": manager.num_workers,
        "uptime_seconds": uptime,
    }
    status_code = 200 if payload["status"] == "ready" else 503
    return Response(
        content=__import__("json").dumps(payload),
        media_type="application/json",
        status_code=status_code,
    )
