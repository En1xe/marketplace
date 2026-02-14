from .crud import SqlalchemyRepository
from models.chats import *


class ChatsRepository(SqlalchemyRepository):
    model = ChatsModel
    
    def __init__(self) -> None:
        super().__init__(object_name='chat')
        
        
class ChatParticipantsRepository(SqlalchemyRepository):
    model = ChatParticipantsModel
    
    def __init__(self) -> None:
        super().__init__(object_name='chat participant')
        
        
class ChatMessagesRepository(SqlalchemyRepository):
    model = ChatMessagesModel
    
    def __init__(self) -> None:
        super().__init__(object_name='chat message')
            