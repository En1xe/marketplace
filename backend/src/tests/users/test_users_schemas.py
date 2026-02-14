import pytest

from sqlalchemy.ext.asyncio import AsyncSession

from schemas.users import (
    get_user_schema, 
    get_detail_user_schema,
    OwnerDetailUsersSchema,
    OwnerUsersSchema,
    PublicDetailUsersSchema,
    PublicUsersSchema,
    UsersSchema
)

from core.factories.users import create_user_factory
from core.factories.listings import create_listing_factory
from core.factories.reviews import create_review_factory


class TestUsersSchemas:
    
    @pytest.mark.asyncio
    async def test_get_user_schema(
        self,
        db_session: AsyncSession
    ):
        user_1 = await create_user_factory(db_session)
        user_2 = await create_user_factory(db_session)
        
        assert isinstance(
            get_user_schema(
                user_obj=user_1, 
                request_user=user_1
            ),
            OwnerUsersSchema
        )
        assert isinstance(
            get_user_schema(
                user_obj=user_2, 
                request_user=user_1
            ),
            PublicUsersSchema
        )
        
    @pytest.mark.asyncio
    async def test_get_detail_user_schema(
        self,
        db_session: AsyncSession
    ):
        user_1 = await create_user_factory(db_session)
        user_2 = await create_user_factory(db_session)
        
        assert isinstance(
            get_detail_user_schema(
                user_obj=user_1, 
                request_user=user_1
            ),
            OwnerDetailUsersSchema
        )
        assert isinstance(
            get_detail_user_schema(
                user_obj=user_2, 
                request_user=user_1
            ),
            PublicDetailUsersSchema
        )
            
    @pytest.mark.asyncio
    async def test_users_schema(
        self,
        db_session: AsyncSession
    ):
        user_1 = await create_user_factory(db_session)
        user_2 = await create_user_factory(db_session)
        user_3 = await create_user_factory(db_session)
        
        assert UsersSchema.model_validate(user_1).rating == 0
        
        listing = await create_listing_factory(
            db_session,
            publisher_id=user_1.id
        )
        
        rating1, rating2 = 3, 5
        
        review_1 = await create_review_factory(
            db_session,
            author_id=user_2.id,
            seller_id=user_1.id,
            listing_id=listing.id,
            rating=rating1
        )
        
        review_2 = await create_review_factory(
            db_session,
            author_id=user_3.id,
            seller_id=user_1.id,
            listing_id=listing.id,
            rating=rating2
        )
        
        await db_session.refresh(user_1)
        
        assert UsersSchema.model_validate(user_1).rating == round((rating1 + rating2) / 2, 2)
                