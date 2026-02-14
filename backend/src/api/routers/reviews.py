from uuid import UUID
from fastapi import APIRouter

from api.dependencies import ReviewsServiceDep, SessionDep, CurrentUserDep
from schemas.reviews import (
    ReviewSchema, 
    CreateReviewSchema, 
    UpdateReviewSchema
)


router = APIRouter(
    prefix='/reviews', 
    tags=['Reviews']
)

@router.get('', response_model=list[ReviewSchema])
async def get_reviews(
    session: SessionDep,
    service: ReviewsServiceDep
):
    return await service.get_all_reviews(session)


@router.get('/{review_uuid}', response_model=ReviewSchema)
async def get_review(
    review_uuid: UUID,
    session: SessionDep,
    service: ReviewsServiceDep
):
    return await service.get_one_review(
        session, 
        review_uuid
    )
    

@router.post('', response_model=ReviewSchema)
async def create_review(
    data: CreateReviewSchema,
    session: SessionDep,
    service: ReviewsServiceDep,
    curr_user: CurrentUserDep,
):
    return await service.add_one_review(
        session, 
        data, 
        author=curr_user
    )


@router.patch('/{review_uuid}', response_model=ReviewSchema)
async def update_review(
    review_uuid: UUID,
    data: UpdateReviewSchema,
    session: SessionDep,
    service: ReviewsServiceDep,
    current_user: CurrentUserDep
):
    return await service.update_one_review(
        session, 
        data=data, 
        review_uuid=review_uuid,
        request_user=current_user
    )


@router.delete('/{review_uuid}', status_code=204)
async def delete_review(
    review_uuid: UUID,
    session: SessionDep,
    service: ReviewsServiceDep,
    current_user: CurrentUserDep
):
    await service.delete_one_review(
        session, 
        review_uuid=review_uuid, 
        request_user=current_user
    )