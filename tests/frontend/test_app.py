import pytest

BASE_URL = "http://localhost:8000"

# --- Helper function ---
def login(page, username="johndoe", password="SecurePass123!"):
    """Perform login and wait for dashboard redirect."""
    page.goto(f"{BASE_URL}/login")
    page.fill("#username", username)
    page.fill("#password", password)
    page.click("button[type='submit']")
    page.wait_for_url("**/dashboard")
    assert page.url.endswith("/dashboard")

# --- Tests ---

@pytest.mark.playwright
def test_register_user(page):
    page.goto(f"{BASE_URL}/register")
    page.fill("#username", "uniqueuser123")
    page.fill("#email", "uniqueuser123@example.com")
    page.fill("#first_name", "John")
    page.fill("#last_name", "Doe")
    page.fill("#password", "SecurePass123!")
    page.fill("#confirm_password", "SecurePass123!")
    page.click("button[type='submit']")
    page.wait_for_url("**/login")
    assert page.url.endswith("/login")

@pytest.mark.playwright
def test_login_user(page):
    login(page)  # use helper
    # Assert welcome message is visible
    assert "Welcome, johndoe!" in page.text_content("#layoutUserWelcome")

@pytest.mark.playwright
def test_calculator(page):
    login(page)  # ensure logged in
    # Select operation type
    page.select_option("#calcType", "addition")
    # Fill in inputs
    page.fill("#calcInputs", "2,2")
    # Submit calculation
    page.click("button[type='submit']")
    # Wait for success alert
    page.wait_for_selector("#successAlert")
    success_text = page.text_content("#successMessage")
    assert "Calculation complete" in success_text

@pytest.mark.playwright
def test_logout_user(page):
    login(page)  # ensure logged in

    # Accept the confirm dialog triggered by logout
    page.once("dialog", lambda dialog: dialog.accept())

    # Click logout button
    page.click("#layoutLogoutBtn")

    # Now wait for redirect
    page.wait_for_url("**/login")
    assert page.url.endswith("/login")

