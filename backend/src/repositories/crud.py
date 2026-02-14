import logging
from abc import abstractmethod, ABC
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import IntegrityError

from core.handlers import handle_sql_integrity_error
from core.decorators.auth import is_owner_or_admin
from core.exceptions import NoObjectWasFoundException
from core.logging import get_logger


logger = get_logger(__name__)


class AbstractRepository(ABC):
    """Abstract basic class for repositories
       
       Defines the interface for CRUD operations.
    """

    @abstractmethod
    async def get_all():
        raise NotImplementedError
    
    @abstractmethod
    async def get_one():
        raise NotImplementedError

    @abstractmethod
    async def add_one():
        raise NotImplementedError

    @abstractmethod
    async def update_one():
        raise NotImplementedError

    @abstractmethod
    async def delete_one():
        raise NotImplementedError


class SqlalchemyRepository(AbstractRepository):
    """Basic repository for working with SQLAlchemy models"""
    
    model = None
    
    def __init__(self, object_name: str = 'object') -> None:
        self.object_name = object_name
        self.no_object_was_found_exception = NoObjectWasFoundException(object_name)
        
    async def get_all(
            self, 
            session: AsyncSession, 
            **kwargs
    ):
        """Get all records with filters"""
        
        logger.debug('Fetching %s records with filters: %s', self.object_name, kwargs)
        
        stmt = select(self.model).filter_by(**kwargs)
        
        res = await session.execute(stmt)
        records = res.scalars().all()

        logger.debug('Fetched %s records', len(records))
        
        return records
    
    async def get_one(
            self, 
            session: AsyncSession, 
            **kwargs
    ):
        """Get a record with filters"""
        logger.debug('Fetching %s with filters: %s', self.object_name, kwargs)
        
        stmt = select(self.model).filter_by(**kwargs)
        
        res = await session.execute(stmt)

        instance = res.scalar_one_or_none()
        if not instance:
            logger.warning('%s was not found', self.object_name.capitalize())
            raise self.no_object_was_found_exception
        
        logger.debug('%s was found', self.object_name.capitalize())
        return instance
    
    @is_owner_or_admin
    async def get_one_with_validation(
            self, 
            session: AsyncSession, 
            **kwargs
    ):
        """Get a record with filters and access rights checking"""
        
        return await self.get_one(session, **kwargs)
    
    @is_owner_or_admin
    async def get_all_with_validation(
            self, 
            session: AsyncSession, 
            **filters
    ):
        """Get all records with filters and access rights checking"""
        
        return await self.get_all(session, **filters)
        
    async def add_one(
            self, 
            session: AsyncSession, 
            data: dict
    ):
        """Add a new record to the db"""
        
        logger.debug('Create %s with details: %s', self.object_name, data)
        
        instance = self.model(**data)
        session.add(instance)
        
        try:
            await session.commit()
            logger.debug('Transaction was committed')
            await session.refresh(instance)
            
            return instance
        except IntegrityError as e:
            logger.error('%s was not created', self.object_name.capitalize())
            handle_sql_integrity_error(e)
        
    async def update_one(
            self, 
            session: AsyncSession,
            data: dict, 
            **kwargs
    ):
        """Update an existing record with access rights checking"""
        
        logger.debug('Update %s with details: %s', self.object_name, data)
        
        instance = await self.get_one_with_validation(session, **kwargs)
        logger.debug('%s was found', self.object_name.capitalize())

        for key, value in data.items():
            setattr(instance, key, value)

        try:
            await session.commit()
            logger.debug('Transaction was committed')
            await session.refresh(instance)
            
            return instance
        except IntegrityError as e:
            logger.error('%s was not updated', self.object_name.capitalize())
            handle_sql_integrity_error(e)
        
    async def delete_one(
            self, 
            session: AsyncSession, 
            **kwargs
    ):
        """Delete a record from db with access rights checking"""
        
        logger.debug('Delete %s', self.object_name)
        
        instance = await self.get_one_with_validation(session, **kwargs)
        logger.debug('%s was found', self.object_name.capitalize())

        try:
            await session.delete(instance)
            await session.commit()
            logger.debug('Transaction was committed')
            
            return instance
        except IntegrityError as e:
            logger.error('%s was not deleted', self.object_name.capitalize())
            handle_sql_integrity_error(e)
            