from datetime import datetime
from sqlalchemy.ext.asyncio import AsyncSession
from typing import Any

from services.users import UsersService
from utils.auth import (
    verify_password, 
    decode_jwt, 
    get_access_token,
    get_refresh_token
)
from schemas.auth import (
    AuthenticateUserSchema, 
    CreateAccessTokenSchema, 
    CreateRefreshTokenSchema
)
from schemas.users import OwnerUsersSchema
from core.exceptions import (
    InvalidPasswordException,
    InvalidTokenException,
    ObjectExpiredException
)
from core.logging import get_logger


logger = get_logger(__name__)

class AuthService:
    """Service for authentication and working with JWT tokens"""
    
    def __init__(self, users_service: UsersService) -> None:
        self.users_service = users_service
    
    async def get_validated_user(
            self,
            session: AsyncSession,
            data: AuthenticateUserSchema
    ) -> OwnerUsersSchema:
        """Validates email and password, returns user data"""
        logger.info('Getting validated user by email and password')
        
        user = await self.users_service.get_one_by_field(
            session, 
            email=data.email
        )
        logger.info("User found: %s", user.id)
        
        if not verify_password(data.password, user.password):
            logger.info("Given password is incorrect")
            raise InvalidPasswordException
        
        logger.info("User was retrieved and validated successfully")
        return OwnerUsersSchema.model_validate(user)
    
    def get_auth_tokens_by_user(
        self,
        user: OwnerUsersSchema
    ):
        """Generates JWT tokens for user"""
        logger.info("Generating JWT token by user data")
        
        access_token = get_access_token(
            CreateAccessTokenSchema(
                email=user.email,
                id=user.id
            )
        )
        logger.info("Access token created successfully")
        refresh_token = get_refresh_token(
            CreateRefreshTokenSchema(
                email=user.email
            )
        )
        logger.info("Refresh token created successfully")

        return {
            'access': access_token,
            'refresh': refresh_token
        }
    
    async def get_auth_tokens_by_email_and_password(
        self,
        session: AsyncSession,
        data: AuthenticateUserSchema
    ) -> dict[str, str]:
        """Full circle of authentication by email and password"""
        logger.info('Getting JWT token by user model')
        
        user = await self.get_validated_user(session, data)
        return self.get_auth_tokens_by_user(user)
    
    async def verify_token(
        self,
        session: AsyncSession,
        access_token: str
    ) -> dict[str, Any]:
        """Validates the JWT token"""
        logger.info('Verifying JWT token')
        
        decoded_token = decode_jwt(access_token)
        
        email = decoded_token.get('email')
        expire_time = decoded_token.get('exp')
        
        user = await self.users_service.get_one_by_field(
            session, 
            email=email
        )

        if expire_time < datetime.now().timestamp():
            logger.error('Access token is expired')
            raise ObjectExpiredException(
                object_name='token', 
                status_code=401
            )
        
        logger.info("Verified successfully")
        return {'success': True, 'user': user}
    
    async def get_access_token_by_refresh(
        self,
        session: AsyncSession,
        refresh_token: str | None
    ) -> str:
        """Updates the access token using the refresh token"""
        logger.info("Generating access token by refresh token")
        
        if not refresh_token:
            logger.error("Refresh token was not found")
            raise InvalidTokenException
        
        decoded_token = decode_jwt(refresh_token)
    
        email = decoded_token.get('sub')

        user = await self.users_service.get_one_by_field(
            session, 
            email=email
        )
        
        access_token = get_access_token(user)
        logger.info("Access token was created successfully")
        return access_token
    