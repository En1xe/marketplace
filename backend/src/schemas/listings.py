from datetime import datetime
from pydantic import BaseModel, computed_field

from .base import UsersBaseSchema, ListingsBaseSchema, ListingMediaBaseSchema


class ListingsSchema(ListingsBaseSchema):
    publisher: UsersBaseSchema
    media: list[ListingMediaBaseSchema] = []
    views: list[ListingViewsSchema] = []
    
    @computed_field
    def viewers_id(self) -> list[int]:
        return [view.viewer_id for view in self.views]
    
    
class CreateListingsSchema(BaseModel):
    title: str
    description: str
    is_active: bool = True
    price: int
    is_price_negotiable: bool
    
    
class UpdateListingsSchema(BaseModel):
    title: str | None = None
    description: str | None = None
    publisher_id: int | None = None
    is_active: bool | None = None
    price: int | None = None
    is_price_negotiable: bool | None = None
    

class ListingViewsSchema(BaseModel):
    id: int
    listing_id: int
    viewer_id: int
    created_at: datetime
    
    
class CreateListingViewsSchema(BaseModel):
    listing_id: int
    

class ListingFavoriteSchema(BaseModel):
    id: int
    user_id: int
    listing_id: int
    listing: ListingsSchema
    
    
class CreateListingFavoriteSchema(BaseModel):
    listing_id: int
    
    
class DeleteListingFavoriteSchema(BaseModel):
    listing_id: int
    
    
class ListingMediaSchema(ListingMediaBaseSchema):
    ...
