import pytest
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from models.listings import ListingViewsModel
from schemas.listings import CreateListingViewsSchema
from utils.listings import create_test_listing_view_data
from core.factories.listings import (
    create_listing_factory, 
    create_listing_view_factory
)
from core.factories.users import create_user_factory

from services.listings.views import ListingViewsService
from repositories.listings import ListingViewsRepository


class TestListingViewsService:
    
    service = ListingViewsService(ListingViewsRepository())
    
    @pytest.mark.asyncio
    async def test_get_all_listing_favorite(
        self,
        db_session: AsyncSession
    ):
        user = await create_user_factory(db_session)
        listing_1 = await create_listing_factory(db_session, publisher_id=user.id)
        listing_2 = await create_listing_factory(db_session, publisher_id=user.id)
        
        await create_listing_view_factory(
            db_session,
            viewer_id=user.id,
            listing_id=listing_1.id
        )
        await create_listing_view_factory(
            db_session,
            viewer_id=user.id,
            listing_id=listing_2.id
        )
            
        result = await self.service.get_all_listing_views(db_session)
            
        assert len(result) == 2
        
    @pytest.mark.asyncio
    async def test_add_one_listing(
        self,
        db_session: AsyncSession
    ):
        user = await create_user_factory(db_session)
        listing = await create_listing_factory(db_session, publisher_id=user.id)
        data = create_test_listing_view_data(
            viewer_id=user.id,
            listing_id=listing.id
        )
        del data['viewer_id']
        
        listing = await self.service.add_one_listing_view(
            db_session,
            CreateListingViewsSchema.model_validate(data),
            request_user=user
        )
        
        assert isinstance(listing, ListingViewsModel)    
        