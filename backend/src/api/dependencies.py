import asyncio
from typing import Annotated

from fastapi import Depends, Request, UploadFile, File
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlalchemy.ext.asyncio import AsyncSession

from core.databases.sql import get_db
from core.factories.rate_limiter import rate_limiter_factory
from core.exceptions import (
    UnauthorizedException, 
    ForbiddenException
)
from core.logging import get_logger

from utils.files import get_image_data, get_media_file_data

from models.users import UsersModel

from core.clients.s3_client import S3Client

from services.auth import AuthService
from services.listings.core import ListingsService
from services.listings.favorite import ListingFavoriteService
from services.listings.views import ListingViewsService
from services.listings.media import ListingMediaService
from services.users import UsersService
from services.verification_codes import VerificationCodesService
from services.chats.core import ChatsService
from services.chats.messages import ChatMessagesService
from services.chats.participants import ChatParticipantsService
from services.oauth.github import GithubOAuthService
from services.reviews import ReviewsService

from repositories.users import UsersRepository
from repositories.listings import *
from repositories.verification_codes import VerificationCodesRepository
from repositories.chats import *
from repositories.reviews import ReviewsRepository


logger = get_logger(__name__)

http_bearer = HTTPBearer()

rate_limiter_get_listings = rate_limiter_factory('get_listings', 5, 5)


def get_auth_service() -> AuthService:
    return AuthService(UsersService(UsersRepository()))


def get_users_service() -> UsersService:
    return UsersService(UsersRepository())


def get_listings_service() -> ListingsService:
    return ListingsService(ListingsRepository())


def get_listing_views_service() -> ListingViewsService:
    return ListingViewsService(ListingViewsRepository())


def get_listing_favorite_service() -> ListingFavoriteService:
    return ListingFavoriteService(ListingFavoriteRepository())


def get_listing_media_service() -> ListingMediaService:
    return ListingMediaService(
        ListingMediaRepository(), 
        ListingsRepository()
    )


def get_verification_codes_service() -> VerificationCodesService:
    return VerificationCodesService(VerificationCodesRepository())


def get_chats_service() -> ChatsService:
    return ChatsService(
        chats_repo=ChatsRepository(),
        chat_participants_repo=ChatParticipantsRepository(),
        listings_repo=ListingsRepository()
    )


def get_chat_messages_service() -> ChatMessagesService:
    return ChatMessagesService(
        chat_messages_repo=ChatMessagesRepository(),
        chats_repo=ChatsRepository()
    )


def get_chat_participants_service() -> ChatParticipantsService:
    return ChatParticipantsService(ChatParticipantsRepository())


def get_github_oauth_service() -> GithubOAuthService:
    return GithubOAuthService()


def get_reviews_service() -> ReviewsService:
    return ReviewsService(ReviewsRepository())


def get_current_user(
    request: Request
) -> UsersModel | None:
    return request.state.user


def get_current_admin_user(
    current_user: UsersModel = Depends(get_current_user)
) -> UsersModel:
    if not current_user:
        logger.error("Unauthorized access")
        raise UnauthorizedException
    
    if not current_user.is_admin:
        logger.error("Request user is not admin")
        raise ForbiddenException
    
    return current_user


def get_s3_client() -> S3Client:
    return S3Client()


async def get_uploaded_image(
    file: UploadFile = File(...)
) -> dict:
    return await get_image_data(file)


async def get_uploaded_media_files(
    files: list[UploadFile] = File(None)
) -> list:
    if not files:
        return []
    
    tasks = [get_media_file_data(file) for file in files]
    
    images = await asyncio.gather(*tasks)
    return images
    


SessionDep = Annotated[AsyncSession, Depends(get_db)]
CredentialsDep = Annotated[HTTPAuthorizationCredentials, Depends(http_bearer)]
CurrentUserDep = Annotated[UsersModel, Depends(get_current_user)]
CurrentAdminUserDep = Annotated[UsersModel, Depends(get_current_admin_user)]

UploadedImageDep = Annotated[dict, Depends(get_uploaded_image)]
UploadedMediaFilesDep = Annotated[list, Depends(get_uploaded_media_files)]


UsersServiceDep = Annotated[UsersService, Depends(get_users_service)]

ReviewsServiceDep = Annotated[ReviewsService, Depends(get_reviews_service)]

AuthServiceDep = Annotated[AuthService, Depends(get_auth_service)]

ListingsServiceDep = Annotated[ListingsService, Depends(get_listings_service)]
ListingViewsServiceDep = Annotated[ListingViewsService, Depends(get_listing_views_service)]
ListingFavoriteServiceDep = Annotated[ListingFavoriteService, Depends(get_listing_favorite_service)]
ListingMediaServiceDep = Annotated[ListingMediaService, Depends(get_listing_media_service)]

VerificationCodesServiceDep = Annotated[VerificationCodesService, Depends(get_verification_codes_service)]

ChatsServiceDep = Annotated[ChatsService, Depends(get_chats_service)]
ChatMessagesServiceDep = Annotated[ChatMessagesService, Depends(get_chat_messages_service)]
ChatParticipantsServiceDep = Annotated[ChatParticipantsService, Depends(get_chat_participants_service)]


GithubOAuthServiceDep = Annotated[GithubOAuthService, Depends(get_github_oauth_service)]


S3ClientDep = Annotated[S3Client, Depends(get_s3_client)]

RATE_LIMITER_GET_LISTING_DEP = Depends(rate_limiter_get_listings)