from fastapi import APIRouter

from .core import router as listings_router
from .favorite import router as listing_favorite_router
from .views import router as listing_views_router
from .media import router as listing_media_router


main_listing_router = APIRouter()

main_listing_router.include_router(listing_favorite_router)
main_listing_router.include_router(listing_media_router)
main_listing_router.include_router(listing_views_router)
main_listing_router.include_router(listings_router)
