import pytest
from pydantic import ValidationError
from app.schemas.user import UserCreate, PasswordUpdate

def base_user_kwargs():
    return {
        "first_name": "Dana",
        "last_name": "Tryon",
        "email": "dana@example.com",
        "username": "danatryon",
    }

# --- UserCreate password strength validators ---

def test_password_too_short():
    with pytest.raises(ValidationError) as exc:
        UserCreate(**base_user_kwargs(), password="Ab1!", confirm_password="Ab1!")
    assert "at least 8 characters" in str(exc.value)

def test_password_missing_uppercase():
    with pytest.raises(ValidationError) as exc:
        UserCreate(**base_user_kwargs(), password="lowercase1!", confirm_password="lowercase1!")
    assert "uppercase" in str(exc.value)

def test_password_missing_lowercase():
    with pytest.raises(ValidationError) as exc:
        UserCreate(**base_user_kwargs(), password="UPPERCASE1!", confirm_password="UPPERCASE1!")
    assert "lowercase" in str(exc.value)

def test_password_missing_digit():
    with pytest.raises(ValidationError) as exc:
        UserCreate(**base_user_kwargs(), password="NoDigits!", confirm_password="NoDigits!")
    assert "digit" in str(exc.value)

def test_password_missing_special_char():
    with pytest.raises(ValidationError) as exc:
        UserCreate(**base_user_kwargs(), password="ValidPass123", confirm_password="ValidPass123")
    assert "special character" in str(exc.value)

def test_password_mismatch():
    with pytest.raises(ValidationError) as exc:
        UserCreate(**base_user_kwargs(), password="ValidPass123!", confirm_password="DifferentPass123!")
    assert "Passwords do not match" in str(exc.value)

# --- PasswordUpdate validators ---

def test_password_update_mismatch():
    with pytest.raises(ValidationError) as exc:
        PasswordUpdate(current_password="OldPass123!", new_password="NewPass123!", confirm_new_password="WrongPass123!")
    assert "confirmation do not match" in str(exc.value)

def test_password_update_same_as_current():
    with pytest.raises(ValidationError) as exc:
        PasswordUpdate(current_password="SamePass123!", new_password="SamePass123!", confirm_new_password="SamePass123!")
    assert "different from current" in str(exc.value)
