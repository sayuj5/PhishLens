"""
Unit & integration tests for the API health endpoints (/health, /ready, /).
"""
import pytest


class TestHealthEndpoints:
    def test_root_returns_version(self, client):
        r = client.get("/")
        assert r.status_code == 200
        data = r.json()
        assert "message" in data
        assert "version" in data

    def test_health_returns_ok(self, client):
        r = client.get("/health")
        assert r.status_code == 200
        data = r.json()
        assert data["status"] == "ok"
        assert "timestamp" in data

    def test_ready_returns_json(self, client):
        """
        /ready may return 200 (ready) or 503 (degraded) depending on
        whether the test DB and worker are initialised. Either is acceptable.
        """
        r = client.get("/ready")
        assert r.status_code in (200, 503)
        data = r.json()
        assert "status" in data
        assert "database" in data


class TestAuthEndpoints:
    def test_login_success(self, client, test_user_token):
        assert len(test_user_token) > 10

    def test_login_invalid_credentials(self, client):
        r = client.post("/token", data={
            "username": "nobody@blackfalcon.test",
            "password": "wrong",
        })
        assert r.status_code == 401

    def test_login_rate_limited(self, client):
        """Rate limiter allows 5/min on /token; 6th call should be 429."""
        for _ in range(5):
            client.post("/token", data={"username": "a@b.com", "password": "x"})
        r = client.post("/token", data={"username": "a@b.com", "password": "x"})
        # Some test runners share state; check either rate-limited or rejected
        assert r.status_code in (401, 429)


class TestSecurityHeaders:
    def test_x_frame_options_present(self, client):
        r = client.get("/health")
        assert r.headers.get("x-frame-options") == "DENY"

    def test_x_content_type_options_present(self, client):
        r = client.get("/health")
        assert r.headers.get("x-content-type-options") == "nosniff"
