from fastapi import Request, FastAPI
from typing import Callable, Awaitable
from fastapi.security import HTTPBearer
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.responses import Response

from api.dependencies import get_auth_service
from core.databases.sql import SessionLocal

        
class AuthMiddleware(BaseHTTPMiddleware):
    """Middleware for user authorization using JWT token"""
    
    def __init__(self, app: FastAPI) -> None:
        super().__init__(app)
        self.http_bearer = HTTPBearer(auto_error=False)
        self.auth_service = get_auth_service()
    
    async def dispatch(
        self, 
        request: Request, 
        call_next: Callable[[Request], Awaitable[Response]]
    ) -> Response:
        """Fetch user data from JWT token"""
        
        try:
            async with SessionLocal() as session:
                credentials = await self.http_bearer(request)
                access_token = credentials.credentials

                data = await self.auth_service.verify_token(
                    session, 
                    access_token
                )

                request.state.user = data['user']
        except:
            request.state.user = None

        return await call_next(request) 
