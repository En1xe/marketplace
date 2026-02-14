from contextlib import asynccontextmanager

from fastapi import FastAPI

from fastapi_cache import FastAPICache
from fastapi_cache.backends.redis import RedisBackend

from .databases.redis import get_cache_redis
from .handlers import register_exception_handlers
from api.routers import main_router
from .middlewares import register_middlewares


@asynccontextmanager
async def lifespan(app: FastAPI):
    redis = get_cache_redis()
    FastAPICache.init(RedisBackend(redis), prefix="fastapi-cache")
    
    yield
    

def create_application() -> FastAPI:
    """Creates and configures a FastAPI application"""
    
    app = FastAPI(
        title='Marketplace',
        version='0.1.0',
        lifespan=lifespan
    )
    
    register_exception_handlers(app)
    register_middlewares(app)
    
    app.include_router(main_router)
    
    return app