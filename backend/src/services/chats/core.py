from sqlalchemy.ext.asyncio import AsyncSession
from uuid import UUID

from repositories.listings import ListingsRepository
from repositories.chats import ChatsRepository, ChatParticipantsRepository
from models.users import UsersModel
from models.chats import ChatsModel
from schemas.chats import CreateChatsSchema
from core.exceptions import (
    ObjectCompletedException, 
    DuplicateEntryFoundException,
    OwnListingFavoriteException
)
from core.logging import get_logger


logger = get_logger(__name__)

class ChatsService:
    def __init__(
        self, 
        chats_repo: ChatsRepository,
        chat_participants_repo: ChatParticipantsRepository,
        listings_repo: ListingsRepository
    ):
        self.chats_repo = chats_repo
        self.chat_participants_repo = chat_participants_repo
        self.listings_repo = listings_repo

    async def get_all_chats(
        self, 
        session: AsyncSession,
        listing_id: int | None,
        **kwargs 
    ) -> list[ChatsModel]:
        logger.info('Getting all chats with filters')
        filters = {}
        
        if listing_id:
            filters['listing_id'] = listing_id
        
        chats = await self.chats_repo.get_all_with_validation(
            session, 
            **filters, 
            **kwargs
        )
        logger.info('Retrieved %s chats', len(chats))
        
        return chats
    
    async def get_chat_by_uuid(
        self, 
        session: AsyncSession, 
        chat_uuid: UUID,
        **kwargs
    ) -> ChatsModel:
        logger.info('Getting a chat by uuid')
        
        chat = await self.chats_repo.get_one_with_validation(
            session, 
            uuid=chat_uuid, 
            **kwargs
        )
        logger.info('Chat found: %s', chat.id)
        
        return chat
    
    async def add_one_chat(
        self, 
        session: AsyncSession, 
        data: CreateChatsSchema
    ) -> ChatsModel:
        logger.info('Creating a chat')
        
        chat_data = data.model_dump()
        chat = await self.chats_repo.add_one(
            session, 
            chat_data
        )
        
        logger.info('Chat created: %s', chat.id)
        
        return chat
    
    async def add_one_chat_with_participants(
        self, 
        session: AsyncSession, 
        data: CreateChatsSchema,
        request_user: UsersModel
    ) -> ChatsModel:
        """A full circle of chat creation.
           
           Fetches the listing and all chats associated with that listing.
           Checks if there is already a chat between two given users.
           Creates a chat and two chat participants.
        """
        logger.info("Creating both chat and two participants")
        
        listing = await self.listings_repo.get_one(
            session, 
            id=data.listing_id
        )
        logger.info("Listing found %s", listing.id)
        
        if not listing.is_active:
            logger.error("Listing is not active")
            raise ObjectCompletedException(object_name='listing')
        
        if listing.publisher.id == request_user.id:
            logger.error('Request user is the owner of the listing favorite')
            raise OwnListingFavoriteException
        
        chats = await self.get_all_chats(
            session, 
            request_user=request_user, 
            listing_id=listing.id
        )
        
        if any([
                True 
                for chat in chats 
                if request_user.id in chat.get_users_id() 
                and listing.publisher.id in chat.get_users_id()
        ]):
            logger.error('Chat already exists')
            raise DuplicateEntryFoundException
        
        chat_data = data.model_dump()
        chat = await self.chats_repo.add_one(
            session, 
            chat_data
        )
        logger.info("Chat created %s", chat.id)
        
        participant_1 = {
            'chat_id': chat.id,
            'participant_id': request_user.id
        }
        participant_2 = {
            'chat_id': chat.id,
            'participant_id': listing.publisher_id
        }
        
        participant1 = await self.chat_participants_repo.add_one(
            session, 
            participant_1
        )
        logger.info("Chat participant was created %s", participant1.id)
        participant2 = await self.chat_participants_repo.add_one(
            session, 
            participant_2
        )
        logger.info("Chat participant was created %s", participant2.id)
        
        await session.refresh(chat)
        logger.info("Chat and two participants were created successfully")
        return chat
    
    async def delete_one_chat(
        self,
        session: AsyncSession,
        chat_uuid: UUID,
        **kwargs
    ) -> ChatsModel:
        logger.info('Deleting the chat within recovery')
        
        chat = await self.chats_repo.delete_one(
            session, 
            uuid=chat_uuid, 
            **kwargs
        )
        
        logger.info('Chat deleted: %s', chat.id)
        
        return chat
