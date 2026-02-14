import pytest
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from models.reviews import ReviewsModel
from utils.reviews import create_test_review_data
from core.factories.reviews import create_review_factory
from core.factories.listings import create_listing_factory
from core.factories.users import create_user_factory
from schemas.reviews import (
    CreateReviewSchema,
    UpdateReviewSchema
)

from services.reviews import ReviewsService
from repositories.reviews import ReviewsRepository


class TestReviewService:
    
    service = ReviewsService(ReviewsRepository())
    
    @pytest.mark.asyncio
    async def test_get_all_reviews(
        self,
        db_session: AsyncSession
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
            
        result = await self.service.get_all_reviews(db_session)
            
        assert len(result) == 2

    @pytest.mark.asyncio
    async def test_get_one_review(
        self,
        db_session: AsyncSession
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
        
        result = await self.service.get_one_review(
            db_session, 
            review_uuid=review.uuid
        )
        
        assert review.uuid == result.uuid
        
    @pytest.mark.asyncio
    async def test_add_one_review(
        self,
        db_session: AsyncSession
    ):
        user_1 = await create_user_factory(db_session)
        user_2 = await create_user_factory(db_session)
        
        listing = await create_listing_factory(db_session, publisher_id=user_1.id)
        
        data = create_test_review_data(
            seller_id=user_1.id,
            author_id=user_2.id,
            listing_id=listing.id
        )
        
        review = await self.service.add_one_review(
            db_session,
            CreateReviewSchema.model_validate(data),
            author=user_2
        )
        
        assert isinstance(review, ReviewsModel) 
        
        
    @pytest.mark.asyncio
    async def test_update_one_review(
        self,
        db_session: AsyncSession
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
        
        new_review_text = 'new_review_text'
        new_data = {
            'text': new_review_text
        }
        
        new_review = await self.service.update_one_review(
            db_session,
            UpdateReviewSchema.model_validate(new_data),
            review.uuid,
            request_user=user_2
        )
        
        assert isinstance(review, ReviewsModel)
        assert review.id == new_review.id
        assert new_review.text == new_review_text     
        
    @pytest.mark.asyncio
    async def test_delete_one_review(
        self,
        db_session: AsyncSession
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
        
        await self.service.delete_one_review(
            db_session,
            review.uuid,
            request_user=user_2
        )
        
        result = await db_session.execute(select(ReviewsModel))
        
        assert len(result.scalars().all()) == 0
        