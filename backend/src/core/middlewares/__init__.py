from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from ..config import settings
from .auth import AuthMiddleware
from .logging import RequestLoggingMiddleware


def register_middlewares(app: FastAPI) -> None:
    """Registers middlewares for the FastAPI application"""
    
    frontend_url = f'http://{settings.HOST_NAME}'
    
    app.add_middleware(
        CORSMiddleware,
        allow_origins=[frontend_url],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )
    
    app.add_middleware(AuthMiddleware)
    app.add_middleware(RequestLoggingMiddleware)
    