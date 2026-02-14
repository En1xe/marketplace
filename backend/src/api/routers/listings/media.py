from fastapi import APIRouter, Form

from api.dependencies import (
    ListingMediaServiceDep,
    SessionDep, 
    CurrentUserDep, 
    S3ClientDep, 
    UploadedMediaFilesDep
)
from schemas.base import SuccessResponseSchema
from schemas.listings import ListingMediaSchema


router = APIRouter(
    prefix='/listings/media', 
    tags=['Listing Media']
)

@router.get('', response_model=list[ListingMediaSchema])
async def get_listings_media(
    session: SessionDep,
    service: ListingMediaServiceDep
):
    return await service.get_all_listing_media(session)


@router.post('', response_model=list[ListingMediaSchema])
async def create_listing_media(
    session: SessionDep,
    client: S3ClientDep,
    service: ListingMediaServiceDep,
    current_user: CurrentUserDep,
    files: UploadedMediaFilesDep,
    listing_id: int = Form(),
):
    return await service.add_listing_media(
        session, 
        client, 
        listing_id, 
        files, 
        request_user=current_user
    )
    
    
@router.patch('', response_model=SuccessResponseSchema)
async def update_listing_media(
    session: SessionDep,
    client: S3ClientDep,
    service: ListingMediaServiceDep,
    current_user: CurrentUserDep,
    files: UploadedMediaFilesDep,
    existing_files: list[str] = [],
    listing_id: int = Form(),
):    
    await service.update_listing_media(
        session, 
        client, 
        listing_id,
        existing_files,
        files, 
        request_user=current_user
    )
    
    return {'success': True}


@router.delete('/{listing_media_id}', status_code=204)
async def delete_listing_media(
    listing_media_id: int,
    session: SessionDep,
    client: S3ClientDep,
    service: ListingMediaServiceDep,
    current_user: CurrentUserDep
):
    await service.delete_one_listing_media(
        session, 
        client, 
        listing_media_id, 
        request_user=current_user
    )
