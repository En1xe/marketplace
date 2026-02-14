import pytest
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import IntegrityError

from core.factories.reviews import create_review_factory
from core.factories.listings import create_listing_factory
from core.factories.users import create_user_factory


class TestReviewsModel:
    
    @pytest.mark.asyncio
    async def test_unique_author_seller_constraint(
        self,
        db_session: AsyncSession  
    ):
        user_1 = await create_user_factory(db_session)
        user_2 = await create_user_factory(db_session)
        
        listing = await create_listing_factory(db_session, publisher_id=user_1.id)
        
        await create_review_factory(
            db_session, 
            seller_id=user_1.id,
            author_id=user_2.id,
            listing_id=listing.id
        )
        
        with pytest.raises(IntegrityError):
            await create_review_factory(
                db_session, 
                seller_id=user_1.id,
                author_id=user_2.id,
                listing_id=listing.id
            )
            
        await db_session.rollback()
            
    @pytest.mark.asyncio
    async def test_check_rating_range(
        self,
        db_session: AsyncSession  
    ):
        user_1 = await create_user_factory(db_session)
        user_2 = await create_user_factory(db_session)
        
        listing = await create_listing_factory(db_session, publisher_id=user_1.id)
      
        with pytest.raises(IntegrityError):  
            await create_review_factory(
                db_session, 
                seller_id=user_1.id,
                author_id=user_2.id,
                listing_id=listing.id,
                rating=10
            )

        await db_session.rollback()
