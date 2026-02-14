from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import IntegrityError

from .crud import SqlalchemyRepository
from utils.auth import hash_password
from core.handlers import handle_sql_integrity_error
from core.logging import get_logger
from models.users import UsersModel


logger = get_logger(__name__)

class UsersRepository(SqlalchemyRepository):
    model = UsersModel
    
    def __init__(self) -> None:
        super().__init__(object_name='user')

    async def add_one(
        self, 
        session: AsyncSession,
        data: dict, 
    ):
        """Add a user to the db with a hashed password"""
        logger.debug('Create %s with details: %s', self.object_name, data)
        
        instance = self.model(**data)
        session.add(instance)

        try:
            await session.flush()
            instance.password = hash_password(instance.password)

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
        *args,
        **fields
    ):
        """Update a user with a hashed password"""
        logger.debug('Update %s with details: %s', self.object_name, data)
        
        instance = await self.get_one_with_validation(session, *args, **fields)
        
        logger.debug('%s was found', self.object_name.capitalize())

        for key, value in data.items():
            setattr(instance, key, value)

        try:
            await session.flush()
            instance.password = hash_password(instance.password)

            await session.commit()
            logger.debug('Transaction was committed')
            await session.refresh(instance)
            
            return instance
        except IntegrityError as e:
            logger.error('%s was not updated', self.object_name.capitalize())
            
            handle_sql_integrity_error(e)
    
    async def update_one_without_user_validation(
        self, 
        session: AsyncSession,
        data: dict, 
        *args,
        **fields
    ):
        """Update a user with a hashed password, excluding request user validation"""
        logger.debug('Update %s without validation, with details: %s', self.object_name, data)
        
        instance = await self.get_one(session, *args, **fields)
        
        logger.debug('%s was found', self.object_name.capitalize())

        for key, value in data.items():
            setattr(instance, key, value)

        try:
            await session.flush()
            instance.password = hash_password(instance.password)

            await session.commit()
            logger.debug('Transaction was committed')
            await session.refresh(instance)
            
            return instance
        except IntegrityError as e:
            logger.error('%s was not updated', self.object_name.capitalize())
            
            handle_sql_integrity_error(e)