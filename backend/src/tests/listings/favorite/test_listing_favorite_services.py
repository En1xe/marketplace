import pytest
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from models.listings import ListingFavoriteModel
from schemas.listings import CreateListingFavoriteSchema
from utils.listings import create_test_listing_favorite_data
from core.factories.listings import (
    create_listing_factory, 
    create_listing_favorite_factory
)
from core.factories.users import create_user_factory

from services.listings.favorite import ListingFavoriteService
from repositories.listings import ListingFavoriteRepository


class TestListingFavoriteService:
    
    service = ListingFavoriteService(ListingFavoriteRepository())
    
    @pytest.mark.asyncio
    async def test_get_all_listing_favorite(
        self,
        db_session: AsyncSession
    ):
        user = await create_user_factory(db_session)
        listing_1 = await create_listing_factory(db_session, publisher_id=user.id)
        listing_2 = await create_listing_factory(db_session, publisher_id=user.id)
        
        await create_listing_favorite_factory(
            db_session,
            user_id=user.id,
            listing_id=listing_1.id
        )
        await create_listing_favorite_factory(
            db_session,
            user_id=user.id,
            listing_id=listing_2.id
        )
            
        result = await self.service.get_all_listing_favorite(
            db_session,
            request_user=user,
            listing_id=None
        )
            
        assert len(result) == 2
        
    @pytest.mark.asyncio
    async def test_get_all_listing_favorite_with_filters(
        self,
        db_session: AsyncSession
    ):
        user = await create_user_factory(db_session)
        listing_1 = await create_listing_factory(db_session, publisher_id=user.id)
        listing_2 = await create_listing_factory(db_session, publisher_id=user.id)
        
        await create_listing_favorite_factory(
            db_session,
            user_id=user.id,
            listing_id=listing_1.id
        )
        await create_listing_favorite_factory(
            db_session,
            user_id=user.id,
            listing_id=listing_2.id
        )
            
        result = await self.service.get_all_listing_favorite(
            db_session,
            request_user=user,
            listing_id=listing_1.id
        )
            
        assert len(result) == 1
        
    @pytest.mark.asyncio
    async def test_add_one_listing(
        self,
        db_session: AsyncSession
    ):
        user = await create_user_factory(db_session)
        listing = await create_listing_factory(db_session, publisher_id=user.id)
        data = create_test_listing_favorite_data(
            user_id=user.id,
            listing_id=listing.id
        )
        del data['user_id']
        
        listing = await self.service.add_one_listing_favorite(
            db_session,
            CreateListingFavoriteSchema.model_validate(data),
            request_user=user
        )
        
        assert isinstance(listing, ListingFavoriteModel)    
        
    @pytest.mark.asyncio
    async def test_delete_one_listing(
        self,
        db_session: AsyncSession
    ):
        user = await create_user_factory(db_session)
        listing = await create_listing_factory(db_session, publisher_id=user.id)
        
        await create_listing_favorite_factory(
            db_session,
            user_id=user.id,
            listing_id=listing.id
        )
        
        await self.service.delete_one_listing_favorite(
            db_session,
            listing.id,
            request_user=user
        )
        
        result = await db_session.execute(select(ListingFavoriteModel))
        
        assert len(result.scalars().all()) == 0
        