from sqlalchemy import select
from sqlalchemy.orm import selectinload
from sqlalchemy.ext.asyncio import AsyncSession

from .crud import SqlalchemyRepository
from models.verification_codes import VerificationCodesModel


class VerificationCodesRepository(SqlalchemyRepository):
    model = VerificationCodesModel
    
    def __init__(self) -> None:
        super().__init__(object_name='verification code')

    # async def get_one(
    #         self, 
    #         session: AsyncSession,
    #         **fields
    #     ):
        
    #     stmt = (
    #         select(self.model)
    #         .options(selectinload(VerifyCodesModel.user))
    #         .filter_by(**fields)
    #     )
    #     instance = await session.execute(stmt)
        
    #     if not instance:
    #         raise self.no_object_was_found_exception
        
    #     return instance.scalar_one_or_none()