# app/auth/redis.py

import redis.asyncio as redis  # this defines redis.from_url
from redis.asyncio import Redis
from app.core.config import get_settings

settings = get_settings()

redis_client: Redis | None = None


async def get_redis() -> Redis:
    global redis_client

    if redis_client is None:
        # this now works because redis.from_url exists
        redis_client = redis.from_url(
            settings.REDIS_URL or "redis://localhost:6379",
            decode_responses=True
        )

    return redis_client


async def add_to_blacklist(jti: str, exp: int):
    client = await get_redis()
    await client.set(f"blacklist:{jti}", "1", ex=exp)


async def is_blacklisted(jti: str) -> bool:
    client = await get_redis()
    return await client.exists(f"blacklist:{jti}") == 1