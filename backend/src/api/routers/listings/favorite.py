from fastapi import APIRouter

from api.dependencies import ListingFavoriteServiceDep, SessionDep, CurrentUserDep
from schemas.listings import (
    CreateListingFavoriteSchema, 
    ListingFavoriteSchema,
)


router = APIRouter(
    prefix='/listings/favorite', 
    tags=['Listing Favorite']
)

@router.get('', response_model=list[ListingFavoriteSchema])
async def get_listings_favorite(
    session: SessionDep,
    service: ListingFavoriteServiceDep,
    current_user: CurrentUserDep,
    listing_id: int | None = None
):
    return await service.get_all_listing_favorite(
        session,
        request_user=current_user,
        listing_id=listing_id
    )
    

@router.post('', response_model=ListingFavoriteSchema)
async def create_listing_favorite(
    data: CreateListingFavoriteSchema,
    session: SessionDep,
    service: ListingFavoriteServiceDep,
    current_user: CurrentUserDep,
):
    return  await service.add_one_listing_favorite(
        session, 
        data,
        request_user=current_user
    )


@router.delete('/{listing_id}', status_code=204)
async def delete_listing_favorite(
    listing_id: int,
    session: SessionDep,
    service: ListingFavoriteServiceDep,
    current_user: CurrentUserDep
):
    await service.delete_one_listing_favorite(
        session, 
        listing_id, 
        request_user=current_user
    )
    