from fastapi import APIRouter

from api.dependencies import ListingViewsServiceDep, SessionDep, CurrentUserDep
from schemas.listings import CreateListingViewsSchema, ListingViewsSchema


router = APIRouter(
    prefix='/listings/views', 
    tags=['Listing Views']
)

@router.get('', response_model=list[ListingViewsSchema])
async def get_listings_views(
    session: SessionDep,
    service: ListingViewsServiceDep
):
    return await service.get_all_listing_views(session)


@router.post('', response_model=ListingViewsSchema)
async def create_listing_view(
    data: CreateListingViewsSchema,
    session: SessionDep,
    service: ListingViewsServiceDep,
    current_user: CurrentUserDep
):
    return await service.add_one_listing_view(
        session, 
        data,
        request_user=current_user,
    )
