import pytest
from sqlalchemy.orm import Session
from app.models.user import User

def test_user_init_with_hashed_password():
    user = User(
        first_name="Dana",
        last_name="Tryon",
        email="dana@example.com",
        username="danatryon",
        hashed_password="hashed123"
    )
    assert user.password == "hashed123"

def test_register_short_password(db_session: Session):
    with pytest.raises(ValueError) as exc:
        User.register(db_session, {
            "first_name": "Dana",
            "last_name": "Tryon",
            "email": "short@example.com",
            "username": "shortuser",
            "password": "123"  # too short
        })
    assert "at least 6 characters" in str(exc.value)

def test_register_duplicate_user(db_session: Session, test_user):
    with pytest.raises(ValueError) as exc:
        User.register(db_session, {
            "first_name": "Dana",
            "last_name": "Tryon",
            "email": test_user.email,  # duplicate email
            "username": "newuser",
            "password": "ValidPass123!"
        })
    assert "already exists" in str(exc.value)

def test_verify_token_sub_none(monkeypatch):
    from jose import jwt
    def fake_decode(token, key, algorithms):
        return {}  # no "sub"
    monkeypatch.setattr(jwt, "decode", fake_decode)
    assert User.verify_token("fake") is None

def test_verify_token_invalid_uuid(monkeypatch):
    from jose import jwt
    def fake_decode(token, key, algorithms):
        return {"sub": "not-a-uuid"}
    monkeypatch.setattr(jwt, "decode", fake_decode)
    assert User.verify_token("fake") is None

def test_register_password_too_short(db_session: Session):
    data = {
        "first_name": "Dana",
        "last_name": "Tryon",
        "email": "shortpass@example.com",
        "username": "shortpassuser",
        "password": "123",  # length 3
    }
    with pytest.raises(ValueError) as exc:
        User.register(db_session, data)
    assert "at least 6 characters" in str(exc.value)

def test_register_duplicate_email(db_session: Session, test_user):
    data = {
        "first_name": "Dana",
        "last_name": "Tryon",
        "email": test_user.email,  # duplicate email
        "username": "newuser",
        "password": "ValidPass123!"
    }
    with pytest.raises(ValueError) as exc:
        User.register(db_session, data)
    assert "already exists" in str(exc.value)

def test_register_duplicate_username(db_session: Session, test_user):
    data = {
        "first_name": "Dana",
        "last_name": "Tryon",
        "email": "unique@example.com",
        "username": test_user.username,  # duplicate username
        "password": "ValidPass123!"
    }
    with pytest.raises(ValueError) as exc:
        User.register(db_session, data)
    assert "already exists" in str(exc.value)
