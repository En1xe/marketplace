from fastapi import APIRouter

from .auth import router as auth_router
from .users import router as users_router
from .listings import main_listing_router
from .chats import main_chats_router
from .verification_codes import router as verify_codes_router
from .oauth import main_oauth_router
from .secure_tokens import router as secure_tokens_router
from .reviews import router as reviews_router


main_router = APIRouter()

main_router.include_router(auth_router)
main_router.include_router(users_router)
main_router.include_router(main_listing_router)
main_router.include_router(main_chats_router)
main_router.include_router(verify_codes_router)
main_router.include_router(main_oauth_router)
main_router.include_router(secure_tokens_router)
main_router.include_router(reviews_router)
