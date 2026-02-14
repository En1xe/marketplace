from sqlalchemy.ext.asyncio import AsyncSession
from uuid import UUID

from repositories.listings import ListingsRepository

from models.users import UsersModel
from models.listings import ListingsModel
from schemas.listings import (
    CreateListingsSchema, 
    UpdateListingsSchema
)
from core.logging import get_logger
from core.exceptions import UnauthorizedException


logger = get_logger(__name__)

class ListingsService:
    def __init__(self, listings_repo: ListingsRepository):
        self.listings_repo = listings_repo

    async def get_all_listings(
        self, 
        session: AsyncSession, 
        is_active: bool | None,
        publisher_id: int | None,
        min_price: int | None,
        max_price: int | None
    ) -> list[ListingsModel]:
        logger.info('Getting all listings with filters')
        filters = {}
        
        if publisher_id:
            filters['publisher_id'] = publisher_id
            
        if min_price:
            filters['min_price'] = min_price
            
        if max_price:
            filters['max_price'] = max_price
            
        if is_active:
            filters['is_active'] = is_active
        
        listings = await self.listings_repo.get_all(
            session, 
            filters
        )
        logger.info('Retrieved %s listings', len(listings))
        
        return listings
    
    async def get_listing_by_uuid(
        self, 
        session: AsyncSession, 
        listing_uuid: UUID,
        **kwargs
    ) -> ListingsModel:
        logger.info('Getting a listing by uuid')
        
        listing = await self.listings_repo.get_one(
            session, 
            uuid=listing_uuid, 
            **kwargs
        )
        logger.info('Listing found: %s', listing.id)
        
        return listing
    
    async def get_listing_by_id(
        self, 
        session: AsyncSession, 
        listing_id: int,
        **kwargs
    ) -> ListingsModel:
        logger.info('Getting a listing by id')
        
        listing = await self.listings_repo.get_one(
            session, 
            id=listing_id, 
            **kwargs
        )
        logger.info('Listing found: %s', listing.id)
        
        return listing
    
    async def add_one_listing(
        self, 
        session: AsyncSession, 
        data: CreateListingsSchema,
        publisher: UsersModel,
    ) -> ListingsModel:
        logger.info('Creating a listing')
        
        if not publisher:
            logger.error('Unauthorized access')
            raise UnauthorizedException
        
        listing_data = data.model_dump()
        listing_data['publisher_id'] = publisher.id
        listing = await self.listings_repo.add_one(
            session, 
            listing_data
        )
        
        logger.info('Listing created: %s', listing.id)
        
        return listing
    
    async def update_one_listing(
        self, 
        session: AsyncSession,
        data: UpdateListingsSchema, 
        listing_uuid: UUID,
        **kwargs
    ) -> ListingsModel:
        logger.info('Updating the listing')
        
        listing_data = data.model_dump(exclude_unset=True)
        listing = await self.listings_repo.update_one(
            session, 
            data=listing_data, 
            uuid=listing_uuid, 
            **kwargs
        )
        
        logger.info('Listing updated: %s', listing.id)
        
        return listing
    
    async def delete_one_listing(
        self,
        session: AsyncSession,
        listing_uuid: UUID,
        **kwargs
    ) -> ListingsModel:
        logger.info('Deleting the listing')
        
        listing = await self.listings_repo.delete_one(
            session, 
            uuid=listing_uuid, 
            **kwargs
        )
        
        logger.info('Listing deleted: %s', listing.id)
        
        return listing
    