from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from backend.main import app
from backend.database import Base, get_db
from backend.models import Network, Asset

# Use a clean test database
SQLALCHEMY_DATABASE_URL = "sqlite:///./test_api.db"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Drop and recreate tables for clean state
Base.metadata.drop_all(bind=engine)
Base.metadata.create_all(bind=engine)

def override_get_db():
    try:
        db = TestingSessionLocal()
        yield db
    finally:
        db.close()

app.dependency_overrides[get_db] = override_get_db

client = TestClient(app)

# Helper function to get token (assuming user created in fixture or first test)
def get_auth_token():
    # Attempt to login or create user then login
    response = client.post("/users/", json={"email": "api@test.com", "password": "password", "role": "admin"})
    login = client.post("/token", data={"username": "api@test.com", "password": "password"})
    return login.json().get("access_token")

def test_dashboard_stats():
    token = get_auth_token()
    headers = {"Authorization": f"Bearer {token}"}
    
    response = client.get("/api/dashboard/", headers=headers)
    assert response.status_code == 200
    data = response.json()
    assert "total_assets" in data
    assert "online_hosts" in data

def test_create_network():
    token = get_auth_token()
    headers = {"Authorization": f"Bearer {token}"}
    
    response = client.post(
        "/api/networks/",
        json={"cidr": "192.168.1.0/24", "name": "Office Network"},
        headers=headers
    )
    assert response.status_code == 200
    assert response.json()["cidr"] == "192.168.1.0/24"

def test_create_asset():
    token = get_auth_token()
    headers = {"Authorization": f"Bearer {token}"}
    
    response = client.post(
        "/api/assets/",
        json={"ip_address": "192.168.1.10", "hostname": "test-host", "os": "Linux"},
        headers=headers
    )
    assert response.status_code == 200
    assert response.json()["ip_address"] == "192.168.1.10"
