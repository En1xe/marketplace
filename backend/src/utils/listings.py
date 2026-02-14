from typing import Any
from models.listings import ListingsModel
from schemas.base import (
    UsersBaseSchema,
    ListingMediaBaseSchema, 
)
from schemas.listings import ListingViewsSchema


def create_test_listing_data(
    publisher_id: int,
    is_active: bool = True,
    price: int = 1000,
    is_price_negotiable: bool = False
) -> dict[str, Any]:
    return {
        'title': 'title',
        'description': '',
        'publisher_id': publisher_id,
        'price': price,
        'is_price_negotiable': is_price_negotiable,
        'is_active': is_active
    }
    
    
def create_test_listing_favorite_data(
    listing_id: int,
    user_id: int
) -> dict[str, Any]:
    return {
        'listing_id': listing_id,
        'user_id': user_id
    }
    
    
def create_test_listing_view_data(
    listing_id: int,
    viewer_id: int
) -> dict[str, Any]:
    return {
        'listing_id': listing_id,
        'viewer_id': viewer_id
    }
    
    
def create_test_listing_media_data(
    listing_id: int,
    url: str = ''
) -> dict[str, Any]:
    return {
        'listing_id': listing_id,
        'url': url
    }
    
    
def get_listing_schema_dict(
    model: ListingsModel
) -> dict:
    return {
        'id': model.id,
        'uuid': model.uuid,
        'title': model.title,
        'description': model.description,
        'created_at': model.created_at,
        'updated_at': model.updated_at,
        'publisher_id': model.publisher_id,
        'is_active': model.is_active,
        'price': model.price,
        'is_price_negotiable': model.is_price_negotiable,
        'publisher': UsersBaseSchema.model_validate(model.publisher),
        'media': [ListingMediaBaseSchema.model_validate(media) for media in model.media],
        'views': [
            ListingViewsSchema(
                id=view.id,
                listing_id=view.listing_id,
                viewer_id=view.viewer_id,
                created_at=view.created_at,    
            ) 
            for view in model.views
        ]
    }