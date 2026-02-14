from uuid import UUID
from pydantic import BaseModel, EmailStr, computed_field

from .base import (
    ListingsWithMediaBaseSchema, 
    UsersBaseSchema, 
    ReviewBaseSchema,
    get_schema
)
from models.users import UsersModel


class UsersSchema(UsersBaseSchema):
    reviews_as_seller: list[ReviewBaseSchema] = []
    
    @computed_field
    def rating(self) -> float:
        """Calculates the rating of a user"""
        
        if not self.reviews_as_seller:
            return 0

        rating_arr = [review.rating for review in self.reviews_as_seller]
        return round(sum(rating_arr) / len(rating_arr), 2)
    

class PublicUsersSchema(UsersSchema):
    ...
    
    
class OwnerUsersSchema(UsersSchema):
    email: EmailStr
    is_admin: bool
    is_oauth: bool
    
    
class CreateUsersSchema(BaseModel):
    username: str
    password: str
    email: EmailStr
    avatar: str | None = None
    
    
class CreateOAuthUsersSchema(BaseModel):
    username: str
    password: str
    email: EmailStr
    avatar: str
    
    
class UpdateUsersSchema(BaseModel):
    username: str | None = None
    password: str | None = None
    email: EmailStr | None = None
    avatar: str | None = None
    

class UpdateUsersSchemaWithinRecovery(BaseModel):
    token: str
    verify_code_uuid: UUID
    password: str
    

class DetailUsersSchema(UsersSchema):
    listings: list[ListingsWithMediaBaseSchema]

    
class PublicDetailUsersSchema(DetailUsersSchema):
    ...
    
    
class OwnerDetailUsersSchema(DetailUsersSchema):
    email: EmailStr
    is_admin: bool
    is_oauth: bool
    

UsersResponseSchema = PublicUsersSchema | OwnerUsersSchema
DetailUsersResponseSchema = PublicDetailUsersSchema | OwnerDetailUsersSchema


def get_user_schema(
    user_obj: UsersModel, 
    request_user: UsersModel | None
) -> BaseModel:
    return get_schema(
        user_obj, 
        request_user,
        {
            'admin': OwnerUsersSchema,
            'owner': OwnerUsersSchema,
            'public': PublicUsersSchema
        }
    )
    
    
def get_detail_user_schema(
    user_obj: UsersModel, 
    request_user: UsersModel | None
) -> BaseModel:
    return get_schema(
        user_obj, 
        request_user,
        {
            'admin': OwnerDetailUsersSchema,
            'owner': OwnerDetailUsersSchema,
            'public': PublicDetailUsersSchema
        }
    )
