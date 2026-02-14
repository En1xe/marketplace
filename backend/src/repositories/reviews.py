from .crud import SqlalchemyRepository

from models.reviews import ReviewsModel


class ReviewsRepository(SqlalchemyRepository):
    model = ReviewsModel
    
    def __init__(self) -> None:
        super().__init__(object_name='review')
        