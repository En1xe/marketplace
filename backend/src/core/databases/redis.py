from functools import lru_cache
from redis.asyncio import Redis

from ..config import settings

@lru_cache
def get_rate_limiter_redis() -> Redis:
    return Redis(
        host=settings.REDIS_HOST, 
        port=settings.REDIS_PORT, 
        db=settings.REDIS_RATE_LIMITER_DB
    )


@lru_cache
def get_cache_redis() -> Redis:
    return Redis(
        host=settings.REDIS_HOST, 
        port=settings.REDIS_PORT, 
        db=settings.REDIS_CACHE_DB
    )
