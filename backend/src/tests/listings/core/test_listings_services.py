import pytest
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from models.listings import ListingsModel
from utils.listings import create_test_listing_data
from core.factories.listings import create_listing_factory
from core.factories.users import create_user_factory
from schemas.listings import (
    CreateListingsSchema,
    UpdateListingsSchema
)

from services.listings.core import ListingsService
from repositories.listings import ListingsRepository


class TestListingService:
    
    service = ListingsService(ListingsRepository())
    
    @pytest.mark.asyncio
    async def test_get_all_listings(
        self,
        db_session: AsyncSession
    ):
        user = await create_user_factory(db_session)
        await create_listing_factory(db_session, publisher_id=user.id)
        await create_listing_factory(db_session, publisher_id=user.id)
            
        result = await self.service.get_all_listings(
            db_session,
            is_active=None,
            max_price=None,
            min_price=None,
            publisher_id=None
        )
            
        assert len(result) == 2
        
    @pytest.mark.asyncio
    async def test_get_all_listings_with_filters(
        self,
        db_session: AsyncSession
    ):
        user_1 = await create_user_factory(db_session)
        user_2 = await create_user_factory(db_session)
        
        await create_listing_factory(
            db_session, 
            publisher_id=user_1.id,
            price=2000
        )
        await create_listing_factory(
            db_session, 
            publisher_id=user_1.id,
            price=3000
        )
        await create_listing_factory(
            db_session, 
            publisher_id=user_2.id,
            price=3000,
        )
            
        result = await self.service.get_all_listings(
            db_session,
            is_active=True,
            max_price=3001,
            min_price=2001,
            publisher_id=user_1.id
        )
            
        assert len(result) == 1
        
    @pytest.mark.asyncio
    async def test_get_listing_by_uuid(
        self,
        db_session: AsyncSession
    ):
        user = await create_user_factory(db_session)
        listing_1 = await create_listing_factory(db_session, publisher_id=user.id)
        
        result = await self.service.get_listing_by_uuid(
            db_session,
            listing_uuid=listing_1.uuid
        )
        
        assert listing_1.uuid == result.uuid
        
    @pytest.mark.asyncio
    async def test_get_listing_by_id(
        self,
        db_session: AsyncSession
    ):
        user = await create_user_factory(db_session)
        listing_1 = await create_listing_factory(db_session, publisher_id=user.id)
        
        result = await self.service.get_listing_by_id(
            db_session,
            listing_id=listing_1.id
        )
        
        assert listing_1.id == result.id
        
    @pytest.mark.asyncio
    async def test_add_one_listing(
        self,
        db_session: AsyncSession
    ):
        user = await create_user_factory(db_session)
        data = create_test_listing_data(publisher_id=user.id)
        del data['publisher_id']
        
        listing = await self.service.add_one_listing(
            db_session,
            CreateListingsSchema.model_validate(data),
            publisher=user
        )
        
        assert isinstance(listing, ListingsModel) 
        
        
    @pytest.mark.asyncio
    async def test_update_one_listing(
        self,
        db_session: AsyncSession
    ):
        user = await create_user_factory(db_session)
        listing = await create_listing_factory(db_session, publisher_id=user.id)
        
        new_listing_title = 'new_listing_title'
        new_data = {
            'title': new_listing_title
        }
        
        new_listing = await self.service.update_one_listing(
            db_session,
            UpdateListingsSchema.model_validate(new_data),
            listing.uuid,
            request_user=user
        )
        
        assert isinstance(listing, ListingsModel)
        assert listing.id == new_listing.id
        assert new_listing.title == new_listing_title     
        
    @pytest.mark.asyncio
    async def test_delete_one_listing(
        self,
        db_session: AsyncSession
    ):
        user = await create_user_factory(db_session)
        listing = await create_listing_factory(db_session, publisher_id=user.id)
        
        await self.service.delete_one_listing(
            db_session,
            listing.uuid,
            request_user=user
        )
        
        result = await db_session.execute(select(ListingsModel))
        
        assert len(result.scalars().all()) == 0
        