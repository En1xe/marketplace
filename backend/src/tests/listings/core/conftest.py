from pytest_asyncio import fixture  
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import text

from api.dependencies import rate_limiter_get_listings
from main import app


@fixture(autouse=True)
async def clean_up_listings(db_session: AsyncSession):
    yield
    
    await db_session.execute(text('DELETE from listings'))
    await db_session.commit()
    
    
@fixture
async def mock_rate_limiting_get_listings():
    async def override_rate_limiter_get_listings():
        return None
    
    app.dependency_overrides[rate_limiter_get_listings] = override_rate_limiter_get_listings
    
    yield
    
    app.dependency_overrides.pop(rate_limiter_get_listings, None)