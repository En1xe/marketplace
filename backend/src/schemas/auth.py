from pydantic import BaseModel, ConfigDict, EmailStr


class AuthenticateUserSchema(BaseModel):
    email: EmailStr
    password: str

    model_config = ConfigDict(strict=True)
    
    
class CreateAccessTokenSchema(BaseModel):
    email: EmailStr
    id: int
    
    
class CreateRefreshTokenSchema(BaseModel):
    email: EmailStr
    
    
class AccessTokenSchema(BaseModel):
    access_token: str