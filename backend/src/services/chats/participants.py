from sqlalchemy.ext.asyncio import AsyncSession

from repositories.chats import ChatParticipantsRepository
from models.chats import ChatParticipantsModel
from schemas.chats import CreateParticipantsSchema
from core.logging import get_logger


logger = get_logger(__name__)

class ChatParticipantsService:
    def __init__(self, chat_participants_repo: ChatParticipantsRepository):
        self.chat_participants_repo = chat_participants_repo

    async def get_all_chat_participants(
        self, 
        session: AsyncSession, 
    ) -> list[ChatParticipantsModel]:
        logger.info('Getting all chat participants')
        
        chat_participants = await self.chat_participants_repo.get_all(session)

        logger.info('Retrieved %s chat participants', len(chat_participants))
        
        return chat_participants
    
    
    async def get_chat_participant_by_id(
        self, 
        session: AsyncSession, 
        chat_participant_id: int,
        **kwargs
    ) -> ChatParticipantsModel:
        logger.info('Getting a chat participant by id')
        
        chat_participant = await self.chat_participants_repo.get_one(
            session, 
            id=chat_participant_id,
            **kwargs
        )
        logger.info('Chat participant found: %s', chat_participant.id)
        
        return chat_participant 
    
    async def add_one_chat_participant(
        self, 
        session: AsyncSession, 
        data: CreateParticipantsSchema
    ) -> ChatParticipantsModel:
        logger.info('Creating a chat participant')
        
        chat_participant_data = data.model_dump()
        chat_participant = await self.chat_participants_repo.add_one(
            session, 
            chat_participant_data
        )
        
        logger.info('Chat participant created: %s', chat_participant.id)
        
        return chat_participant
    
    async def delete_one_chat_participant(
        self,
        session: AsyncSession,
        chat_participant_id: int,
        **kwargs
    ) -> ChatParticipantsModel:
        logger.info('Deleting the chat participant')
        
        chat_participant = await self.chat_participants_repo.delete_one(
            session, 
            id=chat_participant_id,
            **kwargs
        )
        
        logger.info('Chat participant deleted: %s', chat_participant.id)
        
        return chat_participant 
    