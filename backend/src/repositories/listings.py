from sqlalchemy import select, and_
from sqlalchemy.ext.asyncio import AsyncSession

from .crud import SqlalchemyRepository
from core.logging import get_logger
from models.listings import *


logger = get_logger(__name__)

class ListingsRepository(SqlalchemyRepository):
    model = ListingsModel
    
    def __init__(self) -> None:
        super().__init__(object_name='listing')
        
    async def get_all(
        self, 
        session: AsyncSession, 
        filters: dict = {},
    ):
        """Get all listings with custom filters"""
        logger.debug('Fetching %s records with filters: %s', self.object_name, filters)
        stmt = select(self.model)
        
        if filters:
            condition = []
            
            if 'min_price' in filters:
                condition.append(self.model.price >= filters['min_price'])
                
            if 'max_price' in filters:
                condition.append(self.model.price <= filters['max_price'])
            
            if 'publisher_id' in filters:
                condition.append(self.model.publisher_id == filters['publisher_id'])
                
            if 'is_active' in filters:
                condition.append(self.model.is_active == filters['is_active'])
                
            stmt = stmt.filter(and_(*condition))
        
        res = await session.execute(stmt)
        records = res.scalars().all()

        logger.debug('Fetched %s records', len(records))
        
        return records
        
        
class ListingViewsRepository(SqlalchemyRepository):
    model = ListingViewsModel
    
    def __init__(self) -> None:
        super().__init__()
        
        
class ListingMediaRepository(SqlalchemyRepository):
    model = ListingMediaModel
    
    def __init__(self) -> None:
        super().__init__()
            
            
class ListingFavoriteRepository(SqlalchemyRepository):
    model = ListingFavoriteModel
    
    def __init__(self) -> None:
        super().__init__()