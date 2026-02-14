import pytest

from sqlalchemy.ext.asyncio import AsyncSession

from schemas.listings import ListingsSchema
from core.factories.users import create_user_factory
from core.factories.listings import (
    create_listing_factory, 
    create_listing_view_factory
)
from utils.listings import get_listing_schema_dict


class TestListingsSchemas:
    
    @pytest.mark.asyncio
    async def test_listing_schema(
        self,
        db_session: AsyncSession
    ):
        user_1 = await create_user_factory(db_session)
        user_2 = await create_user_factory(db_session)
        user_3 = await create_user_factory(db_session)
        user_4 = await create_user_factory(db_session)
        
        listing = await create_listing_factory(db_session, publisher_id=user_1.id)
        
        await create_listing_view_factory(
            db_session,
            listing_id=listing.id, 
            viewer_id=user_2.id
        )
        await create_listing_view_factory(
            db_session,
            listing_id=listing.id, 
            viewer_id=user_3.id
        )
        await create_listing_view_factory(
            db_session,
            listing_id=listing.id, 
            viewer_id=user_4.id
        )
        
        await db_session.refresh(listing)
        result = ListingsSchema.model_validate(get_listing_schema_dict(listing))
        
        assert result.viewers_id == [user_2.id, user_3.id, user_4.id]