from fastapi import Request, Depends
from typing import Annotated

from core.rate_limiter import RateLimiter, get_rate_limiter
from core.exceptions import TooManyRequestsException


def rate_limiter_factory(
    endpoint: str,
    max_requests: int,
    window_seconds: int
):
    """Factory for creating rate limiting dependencies"""
    
    async def dependency(
        request: Request,
        rate_limiter: Annotated[RateLimiter, Depends(get_rate_limiter)]
    ):
        """Dependency that checks the rate limit for a request."""
        
        ip_address = request.client.host
        
        limited = await rate_limiter.is_limited(
            ip_address,
            endpoint,
            max_requests,
            window_seconds
        )
        
        if limited:
            raise TooManyRequestsException
        
    return dependency
