from typing import Any
from sqlalchemy.ext.asyncio import AsyncSession
from uuid import UUID

from core.clients.s3_client import S3Client
from repositories.users import UsersRepository
from models.users import UsersModel
from schemas.users import (
    CreateUsersSchema, 
    CreateOAuthUsersSchema, 
    UpdateUsersSchema
)
from utils.files import get_compressed_image
from core.exceptions import (
    NoObjectWasFoundException, 
    UnauthorizedException
)
from core.logging import get_logger


logger = get_logger(__name__)


class UsersService:
    def __init__(self, users_repo: UsersRepository):
        self.users_repo = users_repo

    async def get_all_users(
        self, 
        session: AsyncSession, 
    ) -> list[UsersModel]:
        logger.info('Getting all users')
        
        users = await self.users_repo.get_all(session)
        logger.info('Retrieved %s users', len(users))
        
        return users
    
    async def get_one_by_field(
        self,
        session: AsyncSession,
        **kwargs
    ) -> UsersModel:
        logger.info('Getting a user by field')
        
        user = await self.users_repo.get_one(
            session,
            **kwargs
        )
        logger.info('User found: %s', user.id)
        
        return user
        
    async def get_one_by_token(
        self,
        user: UsersModel | None
    ):
        logger.info('Validating a user from token')
        
        if not user:
            logger.error('Unauthorized access')
            raise UnauthorizedException
            
        logger.info('User validated from token: %s', user.id)
        return user
        
    async def get_or_create_one_oauth_user(
        self, 
        session: AsyncSession, 
        data: dict,
    ) -> UsersModel:
        logger.info('Creating or getting oauth user')
        user_data = CreateOAuthUsersSchema.model_validate(data)
        
        try:
            user = await self.get_one_by_field(
                session, 
                email=user_data.email
            )
        except NoObjectWasFoundException:
            data['is_oauth'] = True
            
            user = await self.users_repo.add_one(
                session,
                data
            )
            
        return user
    
    async def add_one_user(
        self, 
        session: AsyncSession, 
        data: CreateUsersSchema
    ) -> UsersModel:
        logger.info('Creating a user')
        
        user_data = data.model_dump()
        user = await self.users_repo.add_one(
            session,
            user_data
        )
        
        logger.info('User created: %s', user.id)
        
        return user
    
    async def update_one_user(
        self, 
        session: AsyncSession,
        data: UpdateUsersSchema, 
        user_uuid: UUID,
        **kwargs
    ) -> UsersModel:
        logger.info('Updating the user')
        
        user_data = data.model_dump(exclude_unset=True)
        user = await self.users_repo.update_one(
            session, 
            user_data, 
            uuid=user_uuid, 
            **kwargs
        )
        
        logger.info('User updated: %s', user.id)
        
        return user
        
    async def update_one_user_within_recovery(
        self, 
        session: AsyncSession,
        data: UpdateUsersSchema, 
        user_uuid: UUID,
        **kwargs
    ) -> UsersModel:
        """Update a user, excluding access right checking 
           within recovery circle
        """
        logger.info('Updating the user within recovery')
        
        user_data = data.model_dump(exclude_unset=True)
        user = await self.users_repo.update_one_without_user_validation(
            session, 
            user_data, 
            uuid=user_uuid, 
            **kwargs
        )
        
        logger.info('User updated: %s', user.id)
        
        return user
        
    async def delete_one_user(
        self,
        session: AsyncSession,
        user_uuid: UUID,
        **kwargs
    ) -> UsersModel:
        logger.info('Deleting the user')
        
        user = await self.users_repo.delete_one(
            session, 
            uuid=user_uuid, 
            **kwargs
        )
        
        logger.info('User deleted: %s', user.id)
        
        return user
    
    async def upload_one_user_avatar(
        self,
        session: AsyncSession,
        s3_client: S3Client,
        user_uuid: UUID,
        image: dict[str, Any],
        **kwargs
    ) -> UsersModel:
        """Uploads an user avatar to S3 storage"""
        logger.info('Uploading user avatar')
        
        user = await self.users_repo.get_one_with_validation(
            session, 
            uuid=user_uuid,
            **kwargs
        )
        
        compressed_img = await get_compressed_image(image['obj'])
        url_to_img = await s3_client.upload_file(
            file=compressed_img,
            file_name=image['name']
        )
        logger.info('Image was uploaded: %s', image['name'])
        
        user = await self.users_repo.update_one(
            session, 
            {'avatar': url_to_img},
            uuid=user_uuid,
            **kwargs
        )
        
        logger.info('User updated: %s', user.id)
        
        return user
