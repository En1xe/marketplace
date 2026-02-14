import pytest
from sqlalchemy.ext.asyncio import AsyncSession

from core.factories.users import create_user_factory
from core.factories.listings import create_listing_factory
from core.exceptions import (
    ForbiddenException, 
    MethodNotImplementedException
)
from utils.users import *


class TestUtilsUsers:
    
    @pytest.mark.asyncio
    async def test_get_filtered_obj_by_request_user(
        self,
        db_session: AsyncSession
    ):
        user_1 = await create_user_factory(db_session)
        user_2 = await create_user_factory(db_session)
        
        listing_1 = await create_listing_factory(
            db_session, 
            publisher_id=user_1.id
        )
        listing_2 = await create_listing_factory(
            db_session, 
            publisher_id=user_2.id
        )
        listing_3 = await create_listing_factory(
            db_session, 
            publisher_id=user_2.id
        )
        
        assert len(get_filtered_obj_by_request_user(
            objects=[listing_1, listing_2, listing_3],
            request_user=user_1
        )) == 1
        
        assert len(get_filtered_obj_by_request_user(
            objects=[listing_1, listing_2, listing_3],
            request_user=user_2
        )) == 2
        
    @pytest.mark.asyncio
    async def test_verify_if_request_user_is_owner(
        self,
        db_session: AsyncSession
    ):
        user_1 = await create_user_factory(db_session)
        user_2 = await create_user_factory(db_session)
        
        listing_1 = await create_listing_factory(
            db_session, 
            publisher_id=user_1.id
        )
        
        assert not verify_if_request_user_is_owner(
            obj=listing_1,
            request_user=user_2,
            raise_exception=False
        )
        
        with pytest.raises(ForbiddenException):
            verify_if_request_user_is_owner(
                obj=listing_1,
                request_user=user_2
            )
            
        assert verify_if_request_user_is_owner(
            obj=listing_1,
            request_user=user_1
        )
        
        with pytest.raises(MethodNotImplementedException):
            verify_if_request_user_is_owner(
                obj={},
                request_user=user_1
            )