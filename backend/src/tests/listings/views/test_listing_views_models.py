import pytest
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import IntegrityError

from core.factories.listings import (
    create_listing_factory, 
    create_listing_view_factory
)
from core.factories.users import create_user_factory


class TestListingsModel:
        
    @pytest.mark.asyncio
    async def test_unique_views_listing_constraint(
        self,
        db_session: AsyncSession  
    ):
        user_1 = await create_user_factory(db_session)
        user_2 = await create_user_factory(db_session)
        
        listing = await create_listing_factory(db_session, publisher_id=user_1.id)
        
        await create_listing_view_factory(
            db_session,
            listing_id=listing.id,
            viewer_id=user_1.id
        )
        
        with pytest.raises(IntegrityError):
            await create_listing_view_factory(
                db_session,
                listing_id=listing.id,
                viewer_id=user_1.id
            )
        
        await db_session.rollback()
        