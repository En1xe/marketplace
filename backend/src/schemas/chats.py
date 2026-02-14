from pydantic import BaseModel, ConfigDict, field_validator

from .base import (
    UsersBaseSchema, 
    ChatMessagesBaseSchema, 
    ChatBaseSchema, 
    ListingsBaseSchema
)


class ChatsSchema(ChatBaseSchema):
    participants: list[ChatParticipantsSchema]
    last_message: ChatMessagesBaseSchema | None = None
    listing: ListingsBaseSchema
    
    model_config = ConfigDict(from_attributes=True)
    

class DetailChatsSchema(ChatBaseSchema):
    participants: list[ChatParticipantsSchema]
    messages: list[ChatMessagesBaseSchema]
    
    
class CreateChatsSchema(BaseModel):
    listing_id: int
   
   
class ChatParticipantsSchema(BaseModel):
    id: int
    chat_id: int
    participant_id: int
    participant: UsersBaseSchema
    
    
class CreateParticipantsSchema(BaseModel):
    chat_id: int
    participant_id: int
   
   
class ChatMessagesSchema(ChatMessagesBaseSchema):
    ...
    
    
class CreateChatMessagesSchema(BaseModel):
    chat_id: int
    text: str
    
    @field_validator('text')
    def validate_text_length(cls, value):
        if len(value.strip()) == 0:
            raise ValueError('Text cannot by empty')
        
        return value
    
class UpdateChatMessagesSchema(BaseModel):
    text: str | None = None
