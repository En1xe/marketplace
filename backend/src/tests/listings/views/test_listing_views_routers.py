import pytest
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from httpx import AsyncClient

from models.listings import ListingViewsModel
from models.users import UsersModel
from core.factories.listings import (
    create_listing_factory, 
    create_listing_view_factory
)


class TestListingViewsRouters:
    
    @pytest.mark.asyncio
    async def test_get_listings(
        self,
        db_session: AsyncSession,
        client: AsyncClient,
        request_user: UsersModel
    ):
        listing_1 = await create_listing_factory(db_session, publisher_id=request_user.id)
        listing_2 = await create_listing_factory(db_session, publisher_id=request_user.id)
        
        await create_listing_view_factory(
            db_session,
            viewer_id=request_user.id,
            listing_id=listing_1.id
        )
        await create_listing_view_factory(
            db_session,
            viewer_id=request_user.id,
            listing_id=listing_2.id
        )
        
        result = await client.get('/listings/views')
        content = result.json()
        
        assert result.status_code == 200
        assert isinstance(content, list)
        assert len(content) == 2
        
        listing_data = content[0]
        
        assert 'viewer_id' in listing_data
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
            '/listings/views', 
            json={
                'listing_id': listing.id
            }
        )
        content = result.json()
        
        assert result.status_code == 200
        assert isinstance(content, dict)
        assert 'viewer_id' in content
        assert 'listing_id' in content
        
        result = await db_session.execute(select(ListingViewsModel))
        assert len(result.scalars().all()) == 1
    