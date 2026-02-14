from sqlalchemy.ext.asyncio import AsyncSession
from uuid import UUID

from repositories.reviews import ReviewsRepository
from models.reviews import ReviewsModel
from models.users import UsersModel
from schemas.reviews import CreateReviewSchema, UpdateReviewSchema
from core.logging import get_logger


logger = get_logger(__name__)

class ReviewsService:
    
    def __init__(self, reviews_repo: ReviewsRepository):
        self.reviews_repo = reviews_repo

    async def get_all_reviews(
        self, 
        session: AsyncSession, 
    ) -> list[ReviewsModel]:
        logger.info('Getting all reviews')
        
        reviews = await self.reviews_repo.get_all(session)
        logger.info('Retrieved %s reviews', len(reviews))
        
        return reviews
    
    async def get_one_review(
        self, 
        session: AsyncSession, 
        review_uuid: UUID,
        **kwargs
    ) -> ReviewsModel:
        logger.info('Getting a review by field')
        
        review = await self.reviews_repo.get_one(
            session, 
            uuid=review_uuid, 
            **kwargs
        )
        logger.info('Review found: %s', review.id)
        
        return review
    
    async def add_one_review(
        self, 
        session: AsyncSession, 
        data: CreateReviewSchema,
        author: UsersModel,
    ) -> ReviewsModel:
        logger.info('Creating a review')
        
        review_data = data.model_dump()
        review_data['author_id'] = author.id
        review = await self.reviews_repo.add_one(
            session, 
            review_data
        )
        
        logger.info('Review created: %s', review.id)
        
        return review
    
    async def update_one_review(
        self, 
        session: AsyncSession,
        data: UpdateReviewSchema, 
        review_uuid: UUID,
        **kwargs
    ) -> ReviewsModel:
        logger.info('Updating the review')
        
        review_data = data.model_dump(exclude_unset=True)
        review = await self.reviews_repo.update_one(
            session, 
            review_data, 
            uuid=review_uuid, 
            **kwargs
        )
        
        logger.info('Review updated: %s', review.id)
        
        return review
        
    async def delete_one_review(
        self,
        session: AsyncSession,
        review_uuid: UUID,
        **kwargs
    ) -> ReviewsModel:
        logger.info('Deleting the review within recovery')
        
        review = await self.reviews_repo.delete_one(
            session, 
            uuid=review_uuid, 
            **kwargs
        )
        
        logger.info('Review deleted: %s', review.id)
        
        return review
