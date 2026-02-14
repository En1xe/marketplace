from fastapi import APIRouter, Body, Response, status
from fastapi.responses import RedirectResponse

from api.dependencies import (
    GithubOAuthServiceDep, 
    UsersServiceDep, 
    SessionDep, 
    AuthServiceDep
)
from schemas.auth import AccessTokenSchema
from schemas.users import OwnerUsersSchema
from utils.auth import set_refresh_token_cookie


router = APIRouter(
    prefix='/oauth/github',
    tags=['Github OAuth']
)

@router.get('/url')
def get_github_auth_url(
    service: GithubOAuthServiceDep
):
    url = service.get_oauth_redirect_uri()
    
    return RedirectResponse(
        url=url, 
        status_code=status.HTTP_302_FOUND
    )


@router.post('/users/login', response_model=AccessTokenSchema)
async def login_github_user(
    session: SessionDep,
    users_service: UsersServiceDep,
    auth_service: AuthServiceDep,
    github_oauth_service: GithubOAuthServiceDep,
    response: Response,
    code: str = Body(embed=True)
):          
    """User authentication via GitHub OAuth
    
    Receives a GitHub code, fetches user data, creates a new user
    or gets an existing one and returns JWT tokens
    """
    
    user_data = await github_oauth_service.get_user_data(code)

    user = await users_service.get_or_create_one_oauth_user(
        session,
        user_data
    )
    user = OwnerUsersSchema.model_validate(user)
    
    tokens = auth_service.get_auth_tokens_by_user(user)
    set_refresh_token_cookie(tokens.get('refresh'), response)
    
    return {'access_token': tokens.get('access')}