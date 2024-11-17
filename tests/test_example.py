from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_read_root():
    response = client.get("/gateway")
    assert response.status_code == 200
    assert response.json() == {"message": "SSO Gateway API is running."}

def test_home_json():
    """Test home page JSON output."""
    response = client.get("/gateway", headers={"Accept": "application/json"})
    assert response.status_code == 200
    data = response.json()
    assert "title" in data
    assert "version" in data
    assert "description" in data
    assert data["title"] == "SSO Gateway"
    assert "version" in data