# tests/unit/test_redis.py

import pytest
from unittest.mock import AsyncMock, patch
import app.auth.redis as redis_utils


#@pytest.mark.asyncio
#async def test_get_redis_initializes(monkeypatch):
#    fake_redis = AsyncMock()

#    def fake_from_url(url, *args, **kwargs):
#        return fake_redis

    # Patch Redis.from_url (correct for your new implementation)
#    monkeypatch.setattr("app.auth.redis.redis", "from_url", fake_from_url)

    # Reset module-level cache
#    redis_utils.redis_client = None

#    client = await redis_utils.get_redis()

#    assert client is fake_redis
#    assert redis_utils.redis_client is fake_redis


@pytest.mark.asyncio
async def test_add_to_blacklist(monkeypatch):
    mock_redis = AsyncMock()
    monkeypatch.setattr(redis_utils, "get_redis", AsyncMock(return_value=mock_redis))

    jti = "test-jti"
    exp = 60

    await redis_utils.add_to_blacklist(jti, exp)

    mock_redis.set.assert_awaited_once_with(f"blacklist:{jti}", "1", ex=exp)


@pytest.mark.asyncio
async def test_is_blacklisted_true(monkeypatch):
    mock_redis = AsyncMock()
    mock_redis.exists.return_value = 1

    monkeypatch.setattr(redis_utils, "get_redis", AsyncMock(return_value=mock_redis))

    result = await redis_utils.is_blacklisted("test-jti")

    mock_redis.exists.assert_awaited_once_with("blacklist:test-jti")
    assert result is True


@pytest.mark.asyncio
async def test_is_blacklisted_false(monkeypatch):
    mock_redis = AsyncMock()
    mock_redis.exists.return_value = 0

    monkeypatch.setattr(redis_utils, "get_redis", AsyncMock(return_value=mock_redis))

    result = await redis_utils.is_blacklisted("test-jti")

    mock_redis.exists.assert_awaited_once_with("blacklist:test-jti")
    assert result is False