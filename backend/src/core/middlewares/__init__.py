from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from .auth import AuthMiddleware
from .logging import RequestLoggingMiddleware

def register_middlewares(app: FastAPI) -> None:
    """Registers middlewares for the FastAPI application"""
    
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["http://localhost:5173"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )
    
    app.add_middleware(AuthMiddleware)
    app.add_middleware(RequestLoggingMiddleware)
    