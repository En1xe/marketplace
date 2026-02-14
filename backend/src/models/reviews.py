from sqlalchemy import ForeignKey, UniqueConstraint, CheckConstraint
from sqlalchemy.orm import mapped_column, Mapped, relationship

from .base import int_id, _uuid, created_at
from core.databases.sql import Base


class ReviewsModel(Base):
    __tablename__ = 'reviews'
    
    id: Mapped[int_id]
    uuid: Mapped[_uuid]
    text: Mapped[str]
    author_id: Mapped[int] = mapped_column(ForeignKey('users.id', ondelete='CASCADE'))
    seller_id: Mapped[int] = mapped_column(ForeignKey('users.id', ondelete='CASCADE'))
    listing_id: Mapped[int] = mapped_column(ForeignKey('listings.id', ondelete='CASCADE'))
    rating: Mapped[int]
    created_at: Mapped[created_at]
    
    author: Mapped['UsersModel'] = relationship(
        foreign_keys=[author_id],
        back_populates='reviews_as_author'
    )
    
    seller: Mapped['UsersModel'] = relationship(
        foreign_keys=[seller_id],
        back_populates='reviews_as_seller'
    )
    
    __table_args__ = (
        UniqueConstraint('author_id', 'seller_id', name='unique_author_seller_constraint'),
        CheckConstraint('rating BETWEEN 1 AND 5', name='check_rating_range'),
    )
    
    def get_users_id(self) -> list[int]:
        return [self.author_id]