from sqlalchemy.ext.asyncio import AsyncSession
from uuid import UUID

from repositories.chats import ChatMessagesRepository, ChatsRepository
from models.chats import ChatMessagesModel
from models.users import UsersModel
from schemas.chats import CreateChatMessagesSchema, UpdateChatMessagesSchema
from core.logging import get_logger
from core.exceptions import UnauthorizedException


logger = get_logger(__name__)

class ChatMessagesService:
    def __init__(
        self, 
        chat_messages_repo: ChatMessagesRepository, 
        chats_repo: ChatsRepository
    ):
        self.chat_messages_repo = chat_messages_repo
        self.chats_repo = chats_repo

    async def get_all_chat_messages(
        self, 
        session: AsyncSession, 
        **kwargs
    ) -> list[ChatMessagesModel]:
        logger.info('Getting all chat messages')
        
        chat_messages = await self.chat_messages_repo.get_all_with_validation(
            session,
            **kwargs
        )
        logger.info('Retrieved %s chat messages', len(chat_messages))
        
        return chat_messages
    
    async def get_chat_message_by_uuid(
        self, 
        session: AsyncSession, 
        chat_message_uuid: UUID,
        **kwargs
    ) -> ChatMessagesModel:
        logger.info('Getting a chat message by uuid')
        
        chat_message = await self.chat_messages_repo.get_one(
            session, 
            uuid=chat_message_uuid, 
            **kwargs
        )
        logger.info('Chat message found: %s', chat_message.id)
        
        return chat_message
    
    async def add_one_chat_message(
        self, 
        session: AsyncSession, 
        data: CreateChatMessagesSchema,
        request_user: UsersModel
    ) -> ChatMessagesModel:
        logger.info('Creating a chat message')
        
        if not request_user:
            logger.error('Unauthorized access')
            raise UnauthorizedException
        
        chat_message_data = data.model_dump()
        chat_message_data['author_id'] = request_user.id
        
        await self.chats_repo.get_one_with_validation(
            session, 
            request_user,
            id=data.chat_id
        )
        logger.info("Request user belongs to the chat")
        
        chat_message = await self.chat_messages_repo.add_one(
            session, 
            chat_message_data
        )
        
        logger.info('Chat message created: %s', chat_message.id)
        
        return chat_message
    
    async def update_one_chat_message(
        self, 
        session: AsyncSession,
        data: UpdateChatMessagesSchema, 
        chat_message_uuid: UUID,
        **kwargs
    ) -> ChatMessagesModel:
        logger.info('Updating the chat message')
        
        chat_message_data = data.model_dump(exclude_unset=True)
        chat_message = await self.chat_messages_repo.update_one(
            session, 
            chat_message_data, 
            uuid=chat_message_uuid,
            **kwargs
        )
        
        logger.info('Chat message updated: %s', chat_message.id)
        
        return chat_message
    
    
    async def delete_one_chat_message(
        self,
        session: AsyncSession,
        chat_message_uuid: UUID,
        **kwargs
    ) -> ChatMessagesModel:
        logger.info('Deleting the chat message')
        
        chat_message = await self.chat_messages_repo.delete_one(
            session, 
            uuid=chat_message_uuid, 
            **kwargs
        )
        
        logger.info('Chat message deleted: %s', chat_message.id)
        
        return chat_message 
