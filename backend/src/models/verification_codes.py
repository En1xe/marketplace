from datetime import datetime
from sqlalchemy import ForeignKey
from sqlalchemy.orm import mapped_column, Mapped, relationship

from .base import int_id, _uuid
from core.databases.sql import Base
from core.types.verification_codes import VerificationCodesOperationTypes
from utils.verification_codes import generate_6_digits_code, get_verification_code_expire_time


class VerificationCodesModel(Base):
    __tablename__ = 'verification_codes'

    id: Mapped[int_id]
    uuid: Mapped[_uuid]
    user_id: Mapped[int] = mapped_column(
        ForeignKey('users.id', ondelete='CASCADE'), 
        nullable=True
    )
    operation_type: Mapped[VerificationCodesOperationTypes] = mapped_column(default='verification')
    field_value: Mapped[str] = mapped_column(nullable=True)
    code: Mapped[str] = mapped_column(default=lambda: generate_6_digits_code())
    expire_at: Mapped[datetime] = mapped_column(default=lambda: get_verification_code_expire_time())
    
    user: Mapped['UsersModel'] = relationship(
        back_populates='verification_codes',
        lazy='selectin'
    )
    