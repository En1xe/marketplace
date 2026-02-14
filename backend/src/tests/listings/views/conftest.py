from pytest_asyncio import fixture  
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import text


@fixture(autouse=True)
async def clean_up_listings(db_session: AsyncSession):
    yield
    
    await db_session.execute(text('DELETE from listing_views'))
    await db_session.commit()
