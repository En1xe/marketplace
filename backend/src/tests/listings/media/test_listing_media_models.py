import pytest
from sqlalchemy.ext.asyncio import AsyncSession

from core.factories.listings import (
    create_listing_factory, 
    create_listing_media_factory
)
from core.factories.users import create_user_factory


class TestListingMediaModel:
    
    @pytest.mark.asyncio
    async def test_get_users_id(
        self,
        db_session: AsyncSession  
    ):
        user = await create_user_factory(db_session)
        
        listing = await create_listing_factory(db_session, publisher_id=user.id)
        
        listing_media = await create_listing_media_factory(
            db_session,
            listing_id=listing.id
        )
        
        assert listing_media.get_users_id() == [listing_media.listing.publisher_id]
        