from uuid import uuid4
from fastapi import Request, FastAPI
from typing import Callable, Awaitable
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.responses import Response

from core.logging import get_logger


logger = get_logger(__name__)
        
class RequestLoggingMiddleware(BaseHTTPMiddleware):
    
    def __init__(self, app: FastAPI) -> None:
        super().__init__(app)
    
    async def dispatch(
        self, 
        request: Request, 
        call_next: Callable[[Request], Awaitable[Response]]
    ) -> Response:
        request_id = str(uuid4())
        
        logger.info('Request received: id=%s, path=%s', request_id, request.url.path)
        
        try:
            response = await call_next(request) 

            logger.info(
                'Response received: method=%s, path=%s, status_code=%s', 
                request.method, 
                request.url.path, 
                response.status_code
            )
            return response
        except Exception as error:
            logger.error(
                'Unhandled exception: method=%s, path=%s, exception=%s', 
                request.method, 
                request.url.path, 
                type(error).__name__
            )
            raise

        