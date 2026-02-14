from functools import lru_cache
from redis.asyncio import Redis
from time import time
from random import randint

from .databases.redis import get_rate_limiter_redis


class RateLimiter:
    """Redis-based rate limiter"""
    
    def __init__(self, redis: Redis) -> None:
        self._redis = redis
        
    async def is_limited(
        self,
        ip_address: str,
        endpoint: str,
        max_requests: int,
        window_seconds: int
    ):
        """Checks whether the request limit for an 
           IP-endpoint pair has been exceeded
        """
        
        key = f'rate_limiter:{endpoint}:{ip_address}'
        
        current_time_ms = time() * 1000
        window_start_ms = current_time_ms - window_seconds * 1000
        
        current_request = f'{current_time_ms}-{randint(1, 100000)}'
        
        async with self._redis.pipeline() as pipe:
            await pipe.zremrangebyscore(key, 0, window_start_ms)
            
            await pipe.zcard(key)
            
            await pipe.zadd(key, {current_request: current_time_ms})
            await pipe.expire(key, window_seconds)
            
            res = await pipe.execute()
            
        _, current_count, _, _ = res
        return current_count >= max_requests
    
    
@lru_cache
def get_rate_limiter():
    return RateLimiter(get_rate_limiter_redis())