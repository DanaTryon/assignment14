import pytest

# Rename fixture so it does NOT conflict with pytest-base-url
@pytest.fixture
def server_url(fastapi_server):
    return fastapi_server.rstrip("/")

import uuid

def login(page, server_url, password="SecurePass123!"):
    # Generate a unique username for each test
    username = f"user_{uuid.uuid4().hex[:8]}"

    # Register the user
    page.goto(f"{server_url}/register")
    page.fill("#username", username)
    page.fill("#email", f"{username}@example.com")
    page.fill("#first_name", "Test")
    page.fill("#last_name", "User")
    page.fill("#password", password)
    page.fill("#confirm_password", password)
    page.get_by_role("button", name="Create Account").click()
    page.wait_for_url("**/login")

    # Login
    page.goto(f"{server_url}/login")
    page.fill("#username", username)
    page.fill("#password", password)
    page.get_by_role("button", name="Sign in").click()
    page.wait_for_url("**/dashboard")
    assert page.url.endswith("/dashboard")

@pytest.mark.playwright
def test_calculator(page, server_url):
    login(page, server_url)
    page.get_by_label("Operation Type").select_option("addition")
    page.get_by_label("Numbers (comma-separated)").fill("2,2")
    page.get_by_role("button", name="Calculate").click()
    page.wait_for_selector("#successAlert:not(.hidden)")
    assert "Calculation complete" in page.text_content("#successMessage")

@pytest.mark.playwright
def test_logout_user(page, server_url):
    login(page, server_url)
    page.once("dialog", lambda dialog: dialog.accept())
    page.click("#layoutLogoutBtn")
    page.wait_for_url("**/login")
    assert page.url.endswith("/login")