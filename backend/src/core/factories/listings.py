from sqlalchemy.ext.asyncio import AsyncSession

from models.listings import (
    ListingsModel, 
    ListingViewsModel, 
    ListingFavoriteModel,
    ListingMediaModel
)
from utils.listings import (
    create_test_listing_data, 
    create_test_listing_view_data,
    create_test_listing_favorite_data,
    create_test_listing_media_data
)


async def create_listing_factory(
    session: AsyncSession,
    **kwargs
) -> ListingsModel:
    listing = ListingsModel(**create_test_listing_data(**kwargs))
    
    session.add(listing)
    await session.commit()
    await session.refresh(listing)
    return listing


async def create_listing_favorite_factory(
    session: AsyncSession,
    **kwargs
) -> ListingFavoriteModel:
    listing_favorite = ListingFavoriteModel(**create_test_listing_favorite_data(**kwargs))
    
    session.add(listing_favorite)
    await session.commit()
    await session.refresh(listing_favorite)
    return listing_favorite


async def create_listing_view_factory(
    session: AsyncSession,
    **kwargs
) -> ListingViewsModel:
    listing_view = ListingViewsModel(**create_test_listing_view_data(**kwargs))
    
    session.add(listing_view)
    await session.commit()
    await session.refresh(listing_view)
    return listing_view


async def create_listing_media_factory(
    session: AsyncSession,
    **kwargs
) -> ListingMediaModel:
    listing_view = ListingMediaModel(**create_test_listing_media_data(**kwargs))
    
    session.add(listing_view)
    await session.commit()
    await session.refresh(listing_view)
    return listing_view