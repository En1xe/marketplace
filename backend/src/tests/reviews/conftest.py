from pytest_asyncio import fixture  
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import text

from api.dependencies import rate_limiter_get_listings
from main import app


@fixture(autouse=True)
async def clean_up_listings(db_session: AsyncSession):
    yield
    
    await db_session.execute(text('DELETE from reviews'))
    await db_session.commit()
