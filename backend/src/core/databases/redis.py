from functools import lru_cache
from redis.asyncio import Redis


@lru_cache
def get_rate_limiter_redis() -> Redis:
    return Redis(host='localhost', port=6379, db=2)


@lru_cache
def get_cache_redis() -> Redis:
    return Redis(host='localhost', port=6379, db=1)
