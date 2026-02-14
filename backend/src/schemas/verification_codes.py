from datetime import datetime
from uuid import UUID
from pydantic import BaseModel, EmailStr

from .base import UsersBaseSchema
from core.types.verification_codes import VerificationCodesOperationTypes


class VerificationCodeOnlySchema(BaseModel):
    code: str
    

class VerificationCodeSchema(BaseModel):
    id: int
    uuid: UUID
    user: UsersBaseSchema
    operation_type: VerificationCodesOperationTypes
    field_value: str | None
    code: str
    expire_at: datetime
    

class SecuredVerificationCodeSchema(BaseModel):
    id: int
    uuid: UUID
    operation_type: VerificationCodesOperationTypes
    field_value: str | None
    expire_at: datetime


class VerificationCodeCreateSchema(BaseModel):
    email: EmailStr
    user_id: int
    operation_type: VerificationCodesOperationTypes
    field_value: str | None = None


class EmailRequest(BaseModel):
    email: EmailStr