from sqlalchemy.ext.asyncio import AsyncSession

from repositories.listings import ListingFavoriteRepository
from models.users import UsersModel
from models.listings import ListingFavoriteModel
from schemas.listings import CreateListingFavoriteSchema
from core.exceptions import UnauthorizedException
from core.logging import get_logger


logger = get_logger(__name__)

class ListingFavoriteService:
    def __init__(self, listing_favorite_repo: ListingFavoriteRepository):
        self.listing_favorite_repo = listing_favorite_repo

    async def get_all_listing_favorite(
        self, 
        session: AsyncSession, 
        request_user: UsersModel,
        listing_id: int | None,
    ) -> list[ListingFavoriteModel]:
        logger.info('Getting all listing favorite')
        
        if not request_user:
            logger.error('Unauthorized access')
            raise UnauthorizedException
        
        filters = {}
        filters['user_id'] = request_user.id
        
        if listing_id:
            filters['listing_id'] = listing_id
        
        listing_favorites = await self.listing_favorite_repo.get_all(
            session, 
            **filters
        )
        
        logger.info('Retrieved %s listing favorites', len(listing_favorites))

        return listing_favorites
    
    async def add_one_listing_favorite(
        self, 
        session: AsyncSession, 
        data: CreateListingFavoriteSchema,
        request_user: UsersModel
    ) -> ListingFavoriteModel:
        logger.info('Creating a listing favorite')
        
        if not request_user: 
            logger.error('Unauthorized access')
            raise UnauthorizedException
        
        listing_favorite_data = data.model_dump()
        listing_favorite_data['user_id'] = request_user.id
        
        listing_favorite = await self.listing_favorite_repo.add_one(
            session, 
            listing_favorite_data
        )
        
        logger.info('Listing favorite created: %s', listing_favorite.id)
        
        return listing_favorite
    
    async def delete_one_listing_favorite(
        self,
        session: AsyncSession,
        listing_id: int | None,
        request_user: UsersModel,
    ) -> ListingFavoriteModel:
        logger.info('Deleting the listing favorite')
        
        if not request_user:
            logger.error('Unauthorized access')
            raise UnauthorizedException
        
        filters = {}
        filters['user_id'] = request_user.id
        
        if listing_id:
            filters['listing_id'] = listing_id

        listing_favorite = await self.listing_favorite_repo.delete_one(
            session, 
            request_user=request_user,
            **filters
        )
        
        logger.info('Listing favorite deleted: %s', listing_favorite.id)
        
        return listing_favorite
    