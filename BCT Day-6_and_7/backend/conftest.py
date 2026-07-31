"""
Shared pytest fixtures for all BlackFalcon backend tests.
"""
import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from backend.database import Base, get_db
from backend.main import app
from backend import models, auth

# ── In-memory SQLite test database ─────────────────────────
TEST_DATABASE_URL = "sqlite:///./test_blackfalcon.db"

test_engine = create_engine(
    TEST_DATABASE_URL,
    connect_args={"check_same_thread": False},
)
TestSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=test_engine)


def override_get_db():
    db = TestSessionLocal()
    try:
        yield db
    finally:
        db.close()


# ── Fixtures ────────────────────────────────────────────────

@pytest.fixture(scope="session", autouse=True)
def setup_test_db():
    """Create all tables before the test session and drop them after."""
    Base.metadata.create_all(bind=test_engine)
    yield
    Base.metadata.drop_all(bind=test_engine)


@pytest.fixture(scope="function")
def db_session():
    """Provide a clean DB session for every test function."""
    connection = test_engine.connect()
    transaction = connection.begin()
    session = TestSessionLocal(bind=connection)
    yield session
    session.close()
    transaction.rollback()
    connection.close()


@pytest.fixture(scope="session")
def client():
    """FastAPI TestClient that uses the test database."""
    app.dependency_overrides[get_db] = override_get_db
    with TestClient(app) as c:
        yield c
    app.dependency_overrides.clear()


@pytest.fixture(scope="session")
def test_user_token(client):
    """
    Create a test admin user and return a valid JWT access token.
    The user is created once per session.
    """
    db = TestSessionLocal()
    existing = db.query(models.User).filter(models.User.email == "ci@blackfalcon.test").first()
    if not existing:
        hashed = auth.get_password_hash("Test1234!")
        user = models.User(email="ci@blackfalcon.test", hashed_password=hashed, role="admin")
        db.add(user)
        db.commit()
    db.close()

    response = client.post("/token", data={
        "username": "ci@blackfalcon.test",
        "password": "Test1234!",
    })
    assert response.status_code == 200, f"Login failed: {response.text}"
    return response.json()["access_token"]


@pytest.fixture(scope="function")
def auth_headers(test_user_token):
    return {"Authorization": f"Bearer {test_user_token}"}


@pytest.fixture(scope="function")
def sample_network(db_session):
    """Create and return a sample network in the test DB."""
    network = models.Network(cidr="10.0.0.0/24", name="Test LAN", description="Test network")
    db_session.add(network)
    db_session.commit()
    db_session.refresh(network)
    return network


@pytest.fixture(scope="function")
def sample_asset(db_session, sample_network):
    """Create and return a sample asset linked to the test network."""
    asset = models.Asset(
        ip_address="10.0.0.1",
        hostname="test-host",
        vendor="ACME",
        os="Linux",
        network_id=sample_network.id,
    )
    db_session.add(asset)
    db_session.commit()
    db_session.refresh(asset)
    return asset
