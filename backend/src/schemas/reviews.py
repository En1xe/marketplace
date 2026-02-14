from pydantic import BaseModel

from .base import ReviewBaseSchema


class ReviewSchema(ReviewBaseSchema):
    ...
    
    
class CreateReviewSchema(BaseModel):
    text: str
    seller_id: int
    listing_id: int
    rating: int
    
    
class UpdateReviewSchema(BaseModel):
    text: str | None = None
    author_id: int | None = None
    seller_id: int | None = None
    listing_id: int | None = None
    rating: int | None = None
