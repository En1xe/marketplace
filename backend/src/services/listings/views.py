from sqlalchemy.ext.asyncio import AsyncSession

from repositories.listings import ListingViewsRepository
from models.listings import ListingViewsModel
from models.users import UsersModel
from schemas.listings import  CreateListingViewsSchema
from core.exceptions import UnauthorizedException
from core.logging import get_logger


logger = get_logger(__name__)

class ListingViewsService:
    def __init__(self, listing_views_repo: ListingViewsRepository):
        self.listing_views_repo = listing_views_repo

    async def get_all_listing_views(
        self, 
        session: AsyncSession, 
    ) -> list[ListingViewsModel]:
        logger.info('Getting all listing views')
        
        listing_views = await self.listing_views_repo.get_all(session)
        logger.info('Retrieved %s listing views', len(listing_views))
        
        return listing_views

    
    async def add_one_listing_view(
        self, 
        session: AsyncSession, 
        data: CreateListingViewsSchema,
        request_user: UsersModel,
    ) -> ListingViewsModel:
        logger.info('Creating a listing view')
        
        if not request_user:
            logger.error("Unauthorized access")
            raise UnauthorizedException
        
        listing_view_data = data.model_dump()
        listing_view_data['viewer_id'] = request_user.id
        
        listing_view = await self.listing_views_repo.add_one(
            session, 
            listing_view_data
        )
        logger.info('Listing view created: %s', listing_view.id)
        
        return listing_view