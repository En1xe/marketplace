import pytest
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from httpx import AsyncClient

from models.listings import ListingsModel
from models.users import UsersModel
from core.factories.listings import create_listing_factory
from core.factories.users import create_user_factory


class TestListingRouters:
    
    @pytest.mark.asyncio
    async def test_get_listings(
        self,
        db_session: AsyncSession,
        client: AsyncClient,
        mock_rate_limiting_get_listings,
    ):
        user = await create_user_factory(db_session)
        await create_listing_factory(db_session, publisher_id=user.id)
        await create_listing_factory(db_session, publisher_id=user.id)
        
        result = await client.get('/listings')
        content = result.json()
        
        assert result.status_code == 200
        assert isinstance(content, list)
        assert len(content) == 2
        
        listing_data = content[0]
        
        assert 'title' in listing_data
        assert 'description' in listing_data
        assert 'publisher_id' in listing_data
        
    @pytest.mark.asyncio
    async def test_get_listing(
        self, 
        db_session: AsyncSession,
        client: AsyncClient
    ):  
        user = await create_user_factory(db_session)
        listing = await create_listing_factory(db_session, publisher_id=user.id)
        
        result = await client.get(f'/listings/{listing.uuid}')
        content = result.json()
        
        assert result.status_code == 200
        assert isinstance(content, dict)
        assert 'title' in content
        assert 'description' in content
        assert 'publisher_id' in content
        
    @pytest.mark.asyncio
    async def test_create_listing(
        self,
        db_session: AsyncSession, 
        client: AsyncClient,
        request_user: UsersModel
    ):  
        result = await client.post(
            '/listings', 
            json={
                'title': 'title',
                'description': 'description',
                'is_active': True,
                'price': 1000,
                'is_price_negotiable': False
            }
        )
        content = result.json()
        
        assert result.status_code == 200
        assert isinstance(content, dict)
        assert 'title' in content
        assert 'description' in content
        assert 'price' in content
        
        result = await db_session.execute(select(ListingsModel))
        assert len(result.scalars().all()) == 1
        
    @pytest.mark.asyncio
    async def test_update_listing(
        self, 
        client: AsyncClient,
        db_session: AsyncSession,
        request_user: UsersModel
    ):  
        listing = await create_listing_factory(db_session, publisher_id=request_user.id)
        
        new_listing_title = 'new_listing_title'
        
        result = await client.patch(
            f'/listings/{listing.uuid}', 
            json={
                'title': new_listing_title,
            }
        )
        content = result.json()
        
        assert result.status_code == 200
        assert isinstance(content, dict)
        assert content.get('title') == new_listing_title
        
    @pytest.mark.asyncio
    async def test_delete_listing(
        self,
        db_session: AsyncSession, 
        client: AsyncClient,
        request_user: UsersModel
    ):
        listing = await create_listing_factory(db_session, publisher_id=request_user.id)
        
        result = await client.delete(f'/listings/{listing.uuid}')
        
        assert result.status_code == 204
        
        result = await db_session.execute(select(ListingsModel))
        assert len(result.scalars().all()) == 0
    