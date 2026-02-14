import pytest
from io import BytesIO
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from models.users import UsersModel
from utils.users import create_test_user_data
from core.factories.users import create_user_factory
from core.exceptions import UnauthorizedException
from core.clients.s3_client import S3Client
from schemas.users import (
    CreateUsersSchema,
    UpdateUsersSchema
)

from services.users import UsersService
from repositories.users import UsersRepository


class TestUserService:
    
    service = UsersService(UsersRepository())
    s3_client = S3Client()
    
    @pytest.mark.asyncio
    async def test_get_all_users(
        self,
        db_session: AsyncSession
    ):
        user_1 = await create_user_factory(db_session)
        user_2 = await create_user_factory(db_session)
            
        result = await self.service.get_all_users(db_session)
            
        assert len(result) == 2
        
        
    @pytest.mark.asyncio
    async def test_get_one_by_field(
        self,
        db_session: AsyncSession
    ):
        user_1 = await create_user_factory(db_session)
        
        result = await self.service.get_one_by_field(
            db_session,
            uuid=user_1.uuid
        )
        
        assert user_1.uuid == result.uuid
        
    @pytest.mark.asyncio
    async def test_get_one_by_token(
        self,
        db_session: AsyncSession
    ):
        user_1 = await create_user_factory(db_session)
        
        result = await self.service.get_one_by_token(
            user=user_1
        )
        
        assert isinstance(result, UsersModel)
        
        with pytest.raises(UnauthorizedException):
            result = await self.service.get_one_by_token(
                user=None
            )
        
    @pytest.mark.asyncio
    async def test_get_or_create_one_oauth_user(
        self,
        db_session: AsyncSession
    ):
        data = create_test_user_data()

        user = await self.service.get_or_create_one_oauth_user(
            db_session,
            data
        )
        
        assert isinstance(user, UsersModel)
        assert user.is_oauth == True
        
        await self.service.get_or_create_one_oauth_user(
            db_session,
            data
        )
        
        result = await db_session.execute(select(UsersModel))
        
        assert len(result.scalars().all()) == 1
        
        
    @pytest.mark.asyncio
    async def test_add_one_user(
        self,
        db_session: AsyncSession
    ):
        data = create_test_user_data()
        
        user = await self.service.add_one_user(
            db_session,
            CreateUsersSchema.model_validate(data)
        )
        
        assert isinstance(user, UsersModel) 
        
        
    @pytest.mark.asyncio
    async def test_update_one_user(
        self,
        db_session: AsyncSession
    ):
        user_1 = await create_user_factory(db_session)
        
        new_user_name = 'new_user_name'
        new_data = {
            'username': new_user_name
        }
        
        new_user = await self.service.update_one_user(
            db_session,
            UpdateUsersSchema.model_validate(new_data),
            user_1.uuid,
            request_user=user_1
        )
        
        assert user_1.email == new_user.email
        assert new_user.username == new_user_name
        
        
    @pytest.mark.asyncio
    async def test_update_one_user_within_recovery(
        self,
        db_session: AsyncSession
    ):
        user_1 = await create_user_factory(db_session)
        
        new_user_name = 'new_user_name'
        new_data = {
            'username': new_user_name
        }
        
        new_user = await self.service.update_one_user_within_recovery(
            db_session,
            UpdateUsersSchema.model_validate(new_data),
            user_1.uuid
        )
        
        assert user_1.email == new_user.email
        assert new_user.username == new_user_name
        
        
    @pytest.mark.asyncio
    async def test_delete_one_user(
        self,
        db_session: AsyncSession
    ):
        user_1 = await create_user_factory(db_session)
        
        new_user = await self.service.delete_one_user(
            db_session,
            user_1.uuid,
            request_user=user_1
        )
        
        result = await db_session.execute(select(UsersModel))
        
        assert len(result.scalars().all()) == 0
        
    @pytest.mark.asyncio
    async def test_upload_one_user_avatar(
        self,
        db_session: AsyncSession,
        mocker
    ):
        user = await create_user_factory(db_session)
        img_path = 'url_to_img'
        
        mock_get_compressed_image = mocker.AsyncMock()
        mock_get_compressed_image.return_value = BytesIO()
        mock_get_compressed_image = mocker.patch('services.users.get_compressed_image')
        
        mock_upload_file = mocker.AsyncMock()
        mock_upload_file = mocker.patch.object(self.s3_client, 'upload_file')
        mock_upload_file.return_value = img_path
        
        updated_user = await self.service.upload_one_user_avatar(
            session=db_session,
            s3_client=self.s3_client,
            user_uuid=user.uuid,    
            image={
                'obj': None,
                'name': ''
            },
            request_user=user
        )
        
        assert updated_user.avatar == img_path
        
        mock_get_compressed_image.assert_awaited_once()
        mock_upload_file.assert_awaited_once()
        