# tests/conftest_unit.py
import pytest

@pytest.fixture(autouse=True)
def no_db_seed(monkeypatch):
    """Prevent DB seeding in unit tests."""
    monkeypatch.setattr("tests.conftest.seed_known_user", lambda *a, **k: None)
