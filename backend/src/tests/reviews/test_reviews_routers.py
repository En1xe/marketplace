import pytest
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from httpx import AsyncClient

from models.reviews import ReviewsModel
from models.users import UsersModel
from core.factories.reviews import create_review_factory
from core.factories.users import create_user_factory
from core.factories.listings import create_listing_factory


class TestReviewRouters:
    
    @pytest.mark.asyncio
    async def test_get_reviews(
        self,
        db_session: AsyncSession,
        client: AsyncClient
    ):
        user_1 = await create_user_factory(db_session)
        user_2 = await create_user_factory(db_session)
        user_3 = await create_user_factory(db_session)
        
        listing = await create_listing_factory(db_session, publisher_id=user_1.id)
        
        await create_review_factory(
            db_session, 
            seller_id=user_1.id,
            author_id=user_2.id,
            listing_id=listing.id
        )
        await create_review_factory(
            db_session, 
            seller_id=user_1.id,
            author_id=user_3.id,
            listing_id=listing.id
        )
        
        result = await client.get('/reviews')
        content = result.json()
        
        assert result.status_code == 200
        assert isinstance(content, list)
        assert len(content) == 2
        
        review_data = content[0]
        
        assert 'text' in review_data
        assert 'author_id' in review_data
        assert 'listing_id' in review_data
        
    @pytest.mark.asyncio
    async def test_get_review(
        self, 
        db_session: AsyncSession,
        client: AsyncClient
    ):  
        user_1 = await create_user_factory(db_session)
        user_2 = await create_user_factory(db_session)
        
        listing = await create_listing_factory(db_session, publisher_id=user_1.id)
        
        review = await create_review_factory(
            db_session, 
            seller_id=user_1.id,
            author_id=user_2.id,
            listing_id=listing.id
        )
        
        result = await client.get(f'/reviews/{review.uuid}')
        content = result.json()
        
        assert result.status_code == 200
        assert isinstance(content, dict)
        assert 'text' in content
        assert 'author_id' in content
        assert 'listing_id' in content
        
    @pytest.mark.asyncio
    async def test_create_review(
        self,
        db_session: AsyncSession, 
        client: AsyncClient,
        request_user: UsersModel
    ):  
        user_1 = await create_user_factory(db_session)
        
        listing = await create_listing_factory(db_session, publisher_id=user_1.id)
        
        result = await client.post(
            '/reviews', 
            json={
                'text': 'text',
                'seller_id': user_1.id,
                'listing_id': listing.id,
                'rating': 5,
            }
        )
        content = result.json()
        
        assert result.status_code == 200
        assert isinstance(content, dict)
        assert 'text' in content
        assert 'author_id' in content
        assert 'listing_id' in content
        
        result = await db_session.execute(select(ReviewsModel))
        assert len(result.scalars().all()) == 1
        
    @pytest.mark.asyncio
    async def test_update_review(
        self, 
        client: AsyncClient,
        db_session: AsyncSession,
        request_user: UsersModel
    ):  
        user_1 = await create_user_factory(db_session)
        
        listing = await create_listing_factory(db_session, publisher_id=user_1.id)
        
        review = await create_review_factory(
            db_session, 
            seller_id=user_1.id,
            author_id=request_user.id,
            listing_id=listing.id
        )
        
        new_review_text = 'new_review_text'
        
        result = await client.patch(
            f'/reviews/{review.uuid}', 
            json={
                'text': new_review_text,
            }
        )
        content = result.json()
        
        assert result.status_code == 200
        assert isinstance(content, dict)
        assert content.get('text') == new_review_text
        
    @pytest.mark.asyncio
    async def test_delete_review(
        self,
        db_session: AsyncSession, 
        client: AsyncClient,
        request_user: UsersModel
    ):
        user_1 = await create_user_factory(db_session)
        
        listing = await create_listing_factory(db_session, publisher_id=user_1.id)
        
        review = await create_review_factory(
            db_session, 
            seller_id=user_1.id,
            author_id=request_user.id,
            listing_id=listing.id
        )
        
        result = await client.delete(f'/reviews/{review.uuid}')
        
        assert result.status_code == 204
        
        result = await db_session.execute(select(ReviewsModel))
        assert len(result.scalars().all()) == 0
    