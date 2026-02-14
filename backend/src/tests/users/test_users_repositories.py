import pytest
from sqlalchemy.ext.asyncio import AsyncSession

from repositories.users import UsersRepository
from models.users import UsersModel
from utils.auth import verify_password
from core.exceptions import DuplicateEntryFoundException
from core.factories.users import create_user_factory


class TestUsersRepository:
    
    repository = UsersRepository()
    
    @pytest.mark.asyncio
    async def test_add_one(
        self,
        db_session: AsyncSession,
    ):
        password = '12345678'
        user_data = {
            'username': 'user',
            'password': password,
            'email': 'mail@mail.com',
            'avatar': None,
        }
        
        user = await self.repository.add_one(
            db_session, 
            user_data
        )

        assert isinstance(user, UsersModel)
        assert verify_password(password, user.password)
        
        with pytest.raises(DuplicateEntryFoundException):
            user = await self.repository.add_one(
                db_session, 
                user_data
            )
        
        await db_session.rollback()
            
    @pytest.mark.asyncio
    async def test_update_one(
        self,
        db_session: AsyncSession
    ):
        user_1 = await create_user_factory(db_session, email='user0@mail.com')
        user_2 = await create_user_factory(db_session, email='user1@mail.com')
        
        new_password = '12345678'
        new_user_data = {
            'username': 'new_user',
            'password': new_password
        }
        
        updated_user = await self.repository.update_one(
            db_session,
            new_user_data,
            uuid=user_2.uuid,
            request_user=user_2
        )
        
        assert isinstance(updated_user, UsersModel) 
        assert updated_user.username == 'new_user'
        assert verify_password(new_password, updated_user.password)
        
        with pytest.raises(DuplicateEntryFoundException):
            user = await self.repository.update_one(
                db_session, 
                {
                    'email': 'user0@mail.com'
                },
                uuid=updated_user.uuid,
                request_user=updated_user
            )
        
        await db_session.rollback()
            
    @pytest.mark.asyncio
    async def test_update_one_without_user_validation(
        self,
        db_session: AsyncSession
    ):    
        user_1 = await create_user_factory(db_session, email='user0@mail.com')
        user_2 = await create_user_factory(db_session, email='user1@mail.com')
        
        new_password = '12345678'
        new_user_data = {
            'username': 'new_user',
            'password': new_password
        }
        
        updated_user = await self.repository.update_one_without_user_validation(
            db_session,
            new_user_data,
            uuid=user_2.uuid
        )
        
        assert isinstance(updated_user, UsersModel) 
        assert updated_user.username == 'new_user'
        assert verify_password(new_password, updated_user.password)
        
        with pytest.raises(DuplicateEntryFoundException):
            user = await self.repository.update_one_without_user_validation(
                db_session, 
                {
                    'email': 'user0@mail.com'
                },
                uuid=updated_user.uuid
            )
            
        await db_session.rollback()
  