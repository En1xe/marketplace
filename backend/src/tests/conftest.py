import pytest
import logging
from pytest_asyncio import fixture  
from httpx import AsyncClient, ASGITransport
from sqlalchemy.ext.asyncio import (
    AsyncSession, 
    create_async_engine, 
    async_sessionmaker, 
    AsyncEngine
)
from sqlalchemy.pool import StaticPool
from typing import AsyncGenerator

from core.factories.users import create_user_factory
from core.databases.sql import Base, get_db
from api.dependencies import (
    get_current_user, 
    get_current_admin_user, 
    get_uploaded_image
)
from main import app


@fixture(scope='session')
async def test_engine():
    engine = create_async_engine(
        url='sqlite+aiosqlite:///:memory:',
        connect_args={
            "check_same_thread": False
        },
        poolclass=StaticPool
    )
    
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)
        
    yield engine
    
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        
    await engine.dispose()


@fixture(scope='session')
async def session_maker(test_engine: AsyncEngine):
    return async_sessionmaker(
        test_engine,
        expire_on_commit=False
    )


@fixture(scope='function')
async def db_session(session_maker) -> AsyncGenerator[AsyncSession, None]:
    async with session_maker() as session:
        yield session
        
        
@fixture(scope='function')
async def client(db_session: AsyncSession) -> AsyncGenerator[AsyncClient, None]:
    async def override_get_db():
        yield db_session
        
    app.dependency_overrides[get_db] = override_get_db
    
    async with AsyncClient(
        transport=ASGITransport(app=app),
        base_url="http://testserver",
    ) as async_client:
        yield async_client
        
    app.dependency_overrides.clear()
    
    
@fixture
async def request_user(db_session: AsyncSession):
    user = await create_user_factory(db_session)
    
    async def override_get_current_user():
        return user
    
    app.dependency_overrides[get_current_user] = override_get_current_user
    
    yield user
    
    app.dependency_overrides.pop(get_current_user, None)
    
@fixture
async def request_admin_user(db_session: AsyncSession):
    user = await create_user_factory(db_session, is_admin=True)
    
    async def override_get_current_admin_user():
        return user
    
    app.dependency_overrides[get_current_admin_user] = override_get_current_admin_user
    
    yield user
    
    app.dependency_overrides.pop(get_current_admin_user, None)
    
@fixture
async def mock_uploaded_image():
    image_data = {
        'obj': None,
        'name': 'name',
        'type': 'image'
    }
    
    async def override_get_uploaded_image():
        return image_data
    
    app.dependency_overrides[get_uploaded_image] = override_get_uploaded_image
    
    yield image_data
    
    app.dependency_overrides.pop(get_uploaded_image, None)


@pytest.fixture(scope='session')
def disable_logging():
    logging.getLogger().setLevel(logging.CRITICAL)