from sqlalchemy import ForeignKey, UniqueConstraint
from sqlalchemy.orm import mapped_column, Mapped, relationship

from core.databases.sql import Base
from .base import int_id, _uuid, created_at, updated_at


class ChatsModel(Base):
    __tablename__ = 'chats'
    
    id: Mapped[int_id]
    uuid: Mapped[_uuid]
    listing_id: Mapped[int] = mapped_column(ForeignKey('listings.id', ondelete='CASCADE'))
    
    participants: Mapped[list['ChatParticipantsModel']] = relationship(
        back_populates='chat',
        lazy='selectin',
        cascade='all, delete-orphan'
    )
    
    listing: Mapped['ListingsModel'] = relationship(
        back_populates='chats',
        lazy='selectin'
    )
    
    messages: Mapped[list['ChatMessagesModel']] = relationship(
        back_populates='chat',
        lazy='selectin',
        order_by='ChatMessagesModel.created_at.desc()',
        cascade='all, delete-orphan'
    )
    
    def get_users_id(self) -> list[int]: 
        return [
            participant.participant_id 
            for participant in self.participants
        ] 
    
    @property
    def last_message(self):
        """Get chat last message or None"""
        if not self.messages: 
            return None
        
        return self.messages[0]
        
    
class ChatParticipantsModel(Base):
    __tablename__ = 'chat_participants'
    
    id: Mapped[int_id]
    chat_id: Mapped[int] = mapped_column(ForeignKey('chats.id', ondelete='CASCADE'))
    participant_id: Mapped[int] = mapped_column(ForeignKey('users.id', ondelete='CASCADE'))
    
    participant: Mapped['UsersModel'] = relationship(
        back_populates='chat_participant',
        lazy='selectin'
    )
    
    chat: Mapped['ChatsModel'] = relationship(
        back_populates='participants',
    )
    
    __table_args__ = (
        UniqueConstraint('chat_id', 'participant_id', name='unique_chat_participant_constraint'),
    )
    
    def get_users_id(self) -> list[int]: 
        return [self.participant_id]
    
    
class ChatMessagesModel(Base):
    __tablename__ = 'chat_messages'
    
    id: Mapped[int_id]
    uuid: Mapped[_uuid]
    author_id: Mapped[int] = mapped_column(ForeignKey('users.id', ondelete='CASCADE'))
    chat_id: Mapped[int] = mapped_column(ForeignKey('chats.id', ondelete='CASCADE'))
    text: Mapped[str]
    created_at: Mapped[created_at]
    updated_at: Mapped[updated_at]
    
    chat: Mapped['ChatsModel'] = relationship(
        back_populates='messages'
    )
    
    def get_users_id(self) -> list[int]: 
        return [self.author_id]
