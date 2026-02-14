import pytest
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from httpx import AsyncClient

from models.listings import ListingFavoriteModel
from models.users import UsersModel
from core.factories.listings import (
    create_listing_factory, 
    create_listing_favorite_factory
)


class TestListingFavoriteRouters:
    
    @pytest.mark.asyncio
    async def test_get_listings(
        self,
        db_session: AsyncSession,
        client: AsyncClient,
        request_user: UsersModel
    ):
        listing_1 = await create_listing_factory(db_session, publisher_id=request_user.id)
        listing_2 = await create_listing_factory(db_session, publisher_id=request_user.id)
        
        await create_listing_favorite_factory(
            db_session,
            user_id=request_user.id,
            listing_id=listing_1.id
        )
        await create_listing_favorite_factory(
            db_session,
            user_id=request_user.id,
            listing_id=listing_2.id
        )
        
        result = await client.get('/listings/favorite')
        content = result.json()
        
        assert result.status_code == 200
        assert isinstance(content, list)
        assert len(content) == 2
        
        listing_data = content[0]
        
        assert 'user_id' in listing_data
        assert 'listing_id' in listing_data
        
    @pytest.mark.asyncio
    async def test_create_listing(
        self,
        db_session: AsyncSession, 
        client: AsyncClient,
        request_user: UsersModel
    ):  
        listing = await create_listing_factory(db_session, publisher_id=request_user.id)
        
        result = await client.post(
            '/listings/favorite', 
            json={
                'listing_id': listing.id
            }
        )
        content = result.json()
        
        assert result.status_code == 200
        assert isinstance(content, dict)
        assert 'user_id' in content
        assert 'listing_id' in content
        
        result = await db_session.execute(select(ListingFavoriteModel))
        assert len(result.scalars().all()) == 1
        
    @pytest.mark.asyncio
    async def test_delete_listing(
        self,
        db_session: AsyncSession, 
        client: AsyncClient,
        request_user: UsersModel
    ):
        listing = await create_listing_factory(db_session, publisher_id=request_user.id)
        
        await create_listing_favorite_factory(
            db_session,
            user_id=request_user.id,
            listing_id=listing.id
        )
        
        result = await client.delete(f'/listings/favorite/{listing.id}')
        
        assert result.status_code == 204
        
        result = await db_session.execute(select(ListingFavoriteModel))
        assert len(result.scalars().all()) == 0
    