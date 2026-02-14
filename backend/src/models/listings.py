from sqlalchemy import ForeignKey, UniqueConstraint
from sqlalchemy.orm import mapped_column, Mapped, relationship

from core.databases.sql import Base
from .base import int_id, _uuid, created_at, updated_at, _bool_t, _bool_f, url


class ListingsModel(Base):
    __tablename__ = 'listings'
    
    id: Mapped[int_id]
    uuid: Mapped[_uuid]
    title: Mapped[str]
    description: Mapped[str]
    created_at: Mapped[created_at]
    updated_at: Mapped[updated_at]
    publisher_id: Mapped[int] = mapped_column(ForeignKey('users.id', ondelete='CASCADE'))
    is_active: Mapped[_bool_t]
    price: Mapped[int] = mapped_column(nullable=True)
    is_price_negotiable: Mapped[_bool_f]
    
    def get_users_id(self) -> list[int]: 
        return [self.publisher_id]
    
    publisher: Mapped['UsersModel'] = relationship(
        back_populates='listings',
        lazy='selectin' 
    )
    
    chats: Mapped[list['ChatsModel']] = relationship(
        back_populates='listing'
    )
    
    favorite: Mapped[list['ListingFavoriteModel']] = relationship(
        back_populates='listing'
    )
    
    media: Mapped[list['ListingMediaModel']] = relationship(
        back_populates='listing',
        lazy='selectin',
        cascade='all, delete-orphan'
    )
    
    views: Mapped[list['ListingViewsModel']] = relationship(
        back_populates='listing',
        lazy='selectin',
        cascade='all, delete-orphan'
    )
    
    
class ListingViewsModel(Base):
    __tablename__ = 'listing_views'
    
    id: Mapped[int_id]
    listing_id: Mapped[int] = mapped_column(ForeignKey('listings.id', ondelete='CASCADE'))
    viewer_id: Mapped[int] = mapped_column(ForeignKey('users.id', ondelete='CASCADE'))
    created_at: Mapped[created_at]
    
    __table_args__ = (
        UniqueConstraint('listing_id', 'viewer_id', name='unique_views_listing_constraint'),
    )
    
    listing: Mapped['ListingsModel'] = relationship(
        back_populates='views'
    )
    

class ListingFavoriteModel(Base):
    __tablename__ = 'listing_favorite'
    
    id: Mapped[int_id]
    user_id: Mapped[int] = mapped_column(ForeignKey('users.id', ondelete='CASCADE'))
    listing_id: Mapped[int] = mapped_column(ForeignKey('listings.id', ondelete='CASCADE'))
    
    __table_args__ = (
        UniqueConstraint('user_id', 'listing_id', name='unique_user_listing_constraint'),
    )
    
    listing: Mapped['ListingsModel'] = relationship(
        back_populates='favorite',
        lazy='selectin'
    )
    
    def get_users_id(self) -> list: 
        return [self.user_id]
    
    
class ListingMediaModel(Base):
    __tablename__ = 'listing_media'
    
    id: Mapped[int_id]
    listing_id: Mapped[int] = mapped_column(ForeignKey('listings.id', ondelete='CASCADE'))
    url: Mapped[url]
    
    listing: Mapped['ListingsModel'] = relationship(
        back_populates='media',
        lazy='selectin'
    )
    
    def get_users_id(self) -> list: 
        return [self.listing.publisher_id]
 