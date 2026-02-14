import pytest
from sqlalchemy.ext.asyncio import AsyncSession

from repositories.listings import ListingsRepository
from core.factories.listings import create_listing_factory
from core.factories.users import create_user_factory


class TestListingsRepository:
    
    repository = ListingsRepository()
    
    @pytest.mark.asyncio
    async def test_listings_get_all(
        self,
        db_session: AsyncSession,
    ):
        user_1 = await create_user_factory(db_session)
        user_2 = await create_user_factory(db_session)

        await create_listing_factory(
            db_session,
            publisher_id=user_1.id,
            is_active=False
        )
        await create_listing_factory(
            db_session,
            publisher_id=user_1.id,
            price=2000,
            is_active=True
        )
        await create_listing_factory(
            db_session,
            publisher_id=user_1.id,
            price=3000,
            is_active=True
        )
        await create_listing_factory(
            db_session,
            publisher_id=user_2.id,
            price=3000,
            is_active=True
        )
        await create_listing_factory(
            db_session,
            publisher_id=user_1.id,
            price=3000,
            is_active=False
        )
        await create_listing_factory(
            db_session,
            publisher_id=user_1.id,
            price=4000,
            is_active=False
        )
        
        result = await self.repository.get_all(
            db_session,
            filters={
                'min_price': 2001,
                'max_price': 3001,
                'is_active': True,
                'publisher_id': user_1.id
            }
        )

        assert len(result) == 1
        
        result = await self.repository.get_all(
            db_session,
            filters={}
        )

        assert len(result) == 6