from uuid import UUID
from fastapi import APIRouter
from fastapi_cache.decorator import cache

from api.dependencies import (
    ListingsServiceDep, 
    SessionDep, 
    CurrentUserDep, 
    RATE_LIMITER_GET_LISTING_DEP
)
from schemas.listings import (
    ListingsSchema, 
    CreateListingsSchema, 
    UpdateListingsSchema
)
from utils.caching import custom_key_builder


router = APIRouter(
    prefix='/listings', 
    tags=['Listings']
)

@router.get(
    '', 
    response_model=list[ListingsSchema], 
    dependencies=[RATE_LIMITER_GET_LISTING_DEP]
)
# @cache(expire=60, key_builder=custom_key_builder)
async def get_listings(
    session: SessionDep,
    service: ListingsServiceDep,
    is_active: bool | None = None,
    publisher_id: int | None = None,
    min_price: int | None = None,
    max_price: int | None = None
):
    return await service.get_all_listings(
        session,
        is_active=is_active,
        publisher_id=publisher_id,
        min_price=min_price,
        max_price=max_price
    )


@router.get('/{listing_uuid}', response_model=ListingsSchema)
async def get_listing(
    listing_uuid: UUID,
    session: SessionDep,
    service: ListingsServiceDep
):
    return await service.get_listing_by_uuid(
        session, 
        listing_uuid
    )
    

@router.post('', response_model=ListingsSchema)
async def create_listing(
    data: CreateListingsSchema,
    session: SessionDep,
    service: ListingsServiceDep,
    curr_user: CurrentUserDep,
):
    return await service.add_one_listing(
        session, 
        data, 
        publisher=curr_user
    )


@router.patch('/{listing_uuid}', response_model=ListingsSchema)
async def update_listing(
    listing_uuid: UUID,
    data: UpdateListingsSchema,
    session: SessionDep,
    service: ListingsServiceDep,
    current_user: CurrentUserDep
):
    return await service.update_one_listing(
        session, 
        data=data, 
        listing_uuid=listing_uuid,
        request_user=current_user
    )


@router.delete('/{listing_uuid}', status_code=204)
async def delete_listing(
    listing_uuid: UUID,
    session: SessionDep,
    service: ListingsServiceDep,
    current_user: CurrentUserDep
):
    await service.delete_one_listing(
        session, 
        listing_uuid=listing_uuid, 
        request_user=current_user
    )