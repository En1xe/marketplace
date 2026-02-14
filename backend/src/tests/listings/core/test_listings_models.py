import pytest
from sqlalchemy.ext.asyncio import AsyncSession

from core.factories.listings import create_listing_factory
from core.factories.users import create_user_factory


class TestListingsModel:
    
    @pytest.mark.asyncio
    async def test_listing_get_users_id(
        self,
        db_session: AsyncSession  
    ):
        user = await create_user_factory(db_session)
        
        listing = await create_listing_factory(db_session, publisher_id=user.id)
        
        assert listing.get_users_id() == [listing.publisher_id]
        