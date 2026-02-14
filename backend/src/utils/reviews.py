from typing import Any


def create_test_review_data(
    author_id: int,
    seller_id: int,
    listing_id: int,
    rating: int = 5
) -> dict[str, Any]:
    return {
        'text': 'text',
        'author_id': author_id,
        'seller_id': seller_id,
        'listing_id': listing_id,
        'rating': rating
    }