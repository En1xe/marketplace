from sqlalchemy.ext.asyncio import AsyncSession

from models.reviews import ReviewsModel
from utils.reviews import create_test_review_data


async def create_review_factory(
    session: AsyncSession,
    **kwargs
) -> ReviewsModel:
    review = ReviewsModel(**create_test_review_data(**kwargs))
    
    session.add(review)
    await session.commit()
    await session.refresh(review)
    return review
