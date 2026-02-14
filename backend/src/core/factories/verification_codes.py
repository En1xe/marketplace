from sqlalchemy.ext.asyncio import AsyncSession

from models.verification_codes import VerificationCodesModel
from utils.verification_codes import create_test_verification_code_data


async def create_verification_code_factory(
    session: AsyncSession,
    **kwargs
) -> VerificationCodesModel:
    review = VerificationCodesModel(**create_test_verification_code_data(**kwargs))
    
    session.add(review)
    await session.commit()
    await session.refresh(review)
    return review
