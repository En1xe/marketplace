import pytest
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import IntegrityError

from core.factories.users import create_user_factory


class TestUsersModel:
    
    @pytest.mark.asyncio
    async def test_email_field(
        self,
        db_session: AsyncSession    
    ):
        user = await create_user_factory(db_session, email='user0@mail.com')

        with pytest.raises(IntegrityError):
            user = await create_user_factory(db_session, email='user0@mail.com')
            
        await db_session.rollback()
        
    @pytest.mark.asyncio
    async def test_users_get_users_id(
        self,
        db_session: AsyncSession  
    ):
        user = await create_user_factory(db_session)
        
        assert user.get_users_id() == [user.id]
        