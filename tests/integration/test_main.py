# tests/integration/test_main.py
import pytest
from fastapi.testclient import TestClient
from app.main import app
from app.models import calculation 
from app.models.user import User

client = TestClient(app)

def test_health_endpoint():
    """Verify the /health endpoint returns status ok"""
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "ok"}

def test_index_page():
    """Verify the index page renders HTML"""
    response = client.get("/")
    assert response.status_code == 200
    assert "text/html" in response.headers["content-type"]
    assert "<html" in response.text.lower()

def test_login_page():
    """Verify the login page renders HTML"""
    response = client.get("/login")
    assert response.status_code == 200
    assert "text/html" in response.headers["content-type"]
    assert "login" in response.text.lower()

def test_register_page():
    """Verify the register page renders HTML"""
    response = client.get("/register")
    assert response.status_code == 200
    assert "text/html" in response.headers["content-type"]
    assert "register" in response.text.lower()

def test_dashboard_page():
    """Verify the dashboard page renders HTML"""
    response = client.get("/dashboard")
    assert response.status_code == 200
    assert "text/html" in response.headers["content-type"]
    assert "dashboard" in response.text.lower()

def test_register_and_login_flow(db_session=None):
    # Register a new user
    payload = {
        "first_name": "Test",
        "last_name": "User",
        "email": "testuser@example.com",
        "username": "testuser",
        "password": "SecurePass123!",
        "confirm_password": "SecurePass123!"
    }
    response = client.post("/auth/register", json=payload)
    assert response.status_code == 201
    data = response.json()
    assert data["username"] == "testuser"

    # Login with JSON
    login_payload = {"username": "testuser", "password": "SecurePass123!"}
    response = client.post("/auth/login", json=login_payload)
    assert response.status_code == 200
    token_data = response.json()
    assert "access_token" in token_data

def test_login_form_flow():
    # Register user first
    payload = {
        "first_name": "Form",
        "last_name": "User",
        "email": "formuser@example.com",
        "username": "formuser",
        "password": "SecurePass123!",
        "confirm_password": "SecurePass123!"
    }
    client.post("/auth/register", json=payload)

    # Login with form data
    response = client.post(
        "/auth/token",
        data={"username": "formuser", "password": "SecurePass123!"},
        headers={"Content-Type": "application/x-www-form-urlencoded"}
    )
    assert response.status_code == 200
    assert "access_token" in response.json()

def test_calculation_crud_flow():
    # Register + login
    payload = {
        "first_name": "Calc",
        "last_name": "User",
        "email": "calcuser@example.com",
        "username": "calcuser",
        "password": "SecurePass123!",
        "confirm_password": "SecurePass123!"
    }
    client.post("/auth/register", json=payload)
    login_payload = {"username": "calcuser", "password": "SecurePass123!"}
    token = client.post("/auth/login", json=login_payload).json()["access_token"]
    headers = {"Authorization": f"Bearer {token}"}

    # Create calculation
    calc_payload = {"type": "addition", "inputs": [1, 2]}
    response = client.post("/calculations", json=calc_payload, headers=headers)
    assert response.status_code == 201
    calc_id = response.json()["id"]

    # List calculations
    response = client.get("/calculations", headers=headers)
    assert response.status_code == 200
    assert len(response.json()) >= 1

    # Get calculation
    response = client.get(f"/calculations/{calc_id}", headers=headers)
    assert response.status_code == 200
    assert response.json()["result"] == 3

    # Update calculation
    update_payload = {"inputs": [5, 7]}
    response = client.put(f"/calculations/{calc_id}", json=update_payload, headers=headers)
    assert response.status_code == 200
    assert response.json()["result"] == 12

    # Delete calculation
    response = client.delete(f"/calculations/{calc_id}", headers=headers)
    assert response.status_code == 204

# ---------------------------
# Negative Auth Tests
# ---------------------------

def test_register_with_mismatched_passwords():
    payload = {
        "first_name": "Bad",
        "last_name": "User",
        "email": "baduser@example.com",
        "username": "baduser",
        "password": "SecurePass123!",
        "confirm_password": "DifferentPass456!"
    }
    response = client.post("/auth/register", json=payload)
    # Should fail validation before hitting DB
    assert response.status_code == 422

def test_login_with_wrong_password():
    # Register a valid user
    payload = {
        "first_name": "Wrong",
        "last_name": "Password",
        "email": "wrongpass@example.com",
        "username": "wrongpass",
        "password": "SecurePass123!",
        "confirm_password": "SecurePass123!"
    }
    client.post("/auth/register", json=payload)

    # Attempt login with wrong password
    login_payload = {"username": "wrongpass", "password": "BadPass!"}
    response = client.post("/auth/login", json=login_payload)
    assert response.status_code == 401
    assert response.json()["detail"] == "Invalid username or password"

def test_login_with_nonexistent_user():
    login_payload = {"username": "ghostuser", "password": "NoPass123!"}
    response = client.post("/auth/login", json=login_payload)
    assert response.status_code == 401

# ---------------------------
# Negative Calculation Tests
# ---------------------------

def test_get_calculation_invalid_id(auth_headers):
    # Try to fetch with a non-UUID string
    response = client.get("/calculations/not-a-uuid", headers=auth_headers)
    assert response.status_code == 400
    assert response.json()["detail"] == "Invalid calculation id format."

def test_get_calculation_not_found(auth_headers):
    # Use a valid UUID that doesn't exist
    import uuid
    fake_id = str(uuid.uuid4())
    response = client.get(f"/calculations/{fake_id}", headers=auth_headers)
    assert response.status_code == 404
    assert response.json()["detail"] == "Calculation not found."

def test_update_calculation_not_found(auth_headers):
    import uuid
    fake_id = str(uuid.uuid4())
    update_payload = {"inputs": [1, 2]}
    response = client.put(f"/calculations/{fake_id}", json=update_payload, headers=auth_headers)
    assert response.status_code == 404

def test_delete_calculation_not_found(auth_headers):
    import uuid
    fake_id = str(uuid.uuid4())
    response = client.delete(f"/calculations/{fake_id}", headers=auth_headers)
    assert response.status_code == 404

# ---------------------------
# Helper Fixture
# ---------------------------

@pytest.fixture
def auth_headers():
    """Registers and logs in a user, returns Authorization headers."""
    payload = {
        "first_name": "Calc",
        "last_name": "Tester",
        "email": "calctester@example.com",
        "username": "calctester",
        "password": "SecurePass123!",
        "confirm_password": "SecurePass123!"
    }
    client.post("/auth/register", json=payload)
    login_payload = {"username": "calctester", "password": "SecurePass123!"}
    token = client.post("/auth/login", json=login_payload).json()["access_token"]
    return {"Authorization": f"Bearer {token}"}

# tests/integration/test_main_lifespan.py
from fastapi.testclient import TestClient
from app.main import app

def test_lifespan_runs_and_creates_tables(capfd):
    # Using context manager triggers lifespan startup/shutdown
    with TestClient(app) as client:
        # Call a simple endpoint to ensure app is running
        response = client.get("/health")
        assert response.status_code == 200
        assert response.json() == {"status": "ok"}

    # Capture stdout to verify lifespan messages
    out, _ = capfd.readouterr()
    assert "Creating tables..." in out
    assert "Tables created successfully!" in out

def test_login_form_invalid_credentials():
    # Try logging in with a user that doesn't exist
    response = client.post(
        "/auth/token",
        data={"username": "ghostuser", "password": "WrongPass123!"},
        headers={"Content-Type": "application/x-www-form-urlencoded"}
    )
    assert response.status_code == 401
    body = response.json()
    assert body["detail"] == "Invalid username or password"
    assert response.headers["WWW-Authenticate"] == "Bearer"

def test_create_calculation_forced_valueerror(auth_headers, monkeypatch):
    # Patch Calculation.create to always raise ValueError
    def fake_create(*args, **kwargs):
        raise ValueError("Forced error for coverage")

    monkeypatch.setattr(calculation.Calculation, "create", fake_create)

    payload = {"type": "addition", "inputs": [1, 2]}
    response = client.post("/calculations", json=payload, headers=auth_headers)
    assert response.status_code == 400
    assert response.json()["detail"] == "Forced error for coverage"

def test_update_calculation_invalid_id(auth_headers):
    # Use a clearly invalid UUID string
    bad_id = "not-a-valid-uuid"
    update_payload = {"inputs": [1, 2]}
    response = client.put(f"/calculations/{bad_id}", json=update_payload, headers=auth_headers)
    assert response.status_code == 400
    assert response.json()["detail"] == "Invalid calculation id format."

def test_delete_calculation_invalid_id(auth_headers):
    # Use a clearly invalid UUID string
    bad_id = "not-a-valid-uuid"
    response = client.delete(f"/calculations/{bad_id}", headers=auth_headers)
    assert response.status_code == 400
    assert response.json()["detail"] == "Invalid calculation id format."

def test_login_json_force_none(monkeypatch):
    from app.models.user import User

    def fake_authenticate(db, username, password):
        return None

    monkeypatch.setattr(User, "authenticate", fake_authenticate)

    payload = {"username": "validuser", "password": "ValidPass123!"}
    response = client.post("/auth/login", json=payload)
    assert response.status_code == 401
    assert response.json()["detail"] == "Invalid username or password"



