from datetime import datetime
from uuid import UUID
from pydantic import BaseModel, ConfigDict

from core.types.base import SchemaDict, SqlAlchemyModel
from models.users import UsersModel
from utils.users import verify_if_request_user_is_owner
            

class SuccessResponseSchema(BaseModel):
    success: bool


class ReviewBaseSchema(BaseModel):
    id: int
    uuid: UUID
    text: str
    author_id: int
    seller_id: int
    listing_id: int
    rating: int
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)


class UsersBaseSchema(BaseModel):
    id: int
    uuid: UUID
    username: str
    avatar: str | None
    is_banned: bool

    model_config = ConfigDict(from_attributes=True)
    
    
class ListingsBaseSchema(BaseModel):
    id: int
    uuid: UUID
    title: str
    description: str
    created_at: datetime
    updated_at: datetime
    publisher_id: int
    is_active: bool
    price: int
    is_price_negotiable: bool
    
    model_config = ConfigDict(from_attributes=True)
    

class ListingMediaBaseSchema(BaseModel):
    id: int
    listing_id: int
    url: str
    
    model_config = ConfigDict(from_attributes=True)
    
    
class ListingsWithMediaBaseSchema(ListingsBaseSchema):
    media: list[ListingMediaBaseSchema]
    

class ChatBaseSchema(BaseModel):
    id: int
    uuid: UUID
    listing_id: int
    
    model_config = ConfigDict(from_attributes=True)
    
    
class ChatMessagesBaseSchema(BaseModel):
    id: int
    uuid: UUID
    author_id: int
    chat_id: int
    text: str
    created_at: datetime
    updated_at: datetime
    
    
def get_schema(
    obj: SqlAlchemyModel, 
    request_user: UsersModel | None,
    schemas: SchemaDict
) -> BaseModel:
    if request_user:
        if request_user.is_admin:
            return schemas['admin'].model_validate(obj)
        elif verify_if_request_user_is_owner(
            obj, 
            request_user, 
            raise_exception=False
        ):
            return schemas['owner'].model_validate(obj)

    return schemas['public'].model_validate(obj)