from sqlalchemy.orm import mapped_column, Mapped, relationship

from .base import int_id, _uuid, _bool_f, url
from core.databases.sql import Base


class UsersModel(Base):
    __tablename__ = 'users'
    
    id: Mapped[int_id]
    uuid: Mapped[_uuid]
    username: Mapped[str]
    password: Mapped[str]
    email: Mapped[str] = mapped_column(unique=True)
    avatar: Mapped[url]
    is_banned: Mapped[_bool_f]
    is_admin: Mapped[_bool_f]
    is_oauth: Mapped[_bool_f]
    
    verification_codes: Mapped[list['VerificationCodesModel']] = relationship(
        back_populates='user', 
    )
    
    reviews_as_author: Mapped[list['ReviewsModel']] = relationship(
        foreign_keys='ReviewsModel.author_id',
        back_populates='author', 
        lazy="select",
        cascade='all, delete-orphan'
    )
    
    reviews_as_seller: Mapped[list['ReviewsModel']] = relationship(
        foreign_keys='ReviewsModel.seller_id',
        back_populates='seller', 
        lazy="selectin",
        cascade='all, delete-orphan'
    )
    
    listings: Mapped[list['ListingsModel']] = relationship(
        back_populates='publisher',
        lazy='selectin',
        cascade='all, delete-orphan'
    )
    
    chat_participant: Mapped['ChatParticipantsModel'] = relationship(
        back_populates='participant'
    )
    
    def get_users_id(self) -> list[int]: 
        return [self.id]
    