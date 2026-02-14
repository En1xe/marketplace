from fastapi import APIRouter

from .github import router as github_oauth_router


main_oauth_router = APIRouter()
main_oauth_router.include_router(github_oauth_router)
