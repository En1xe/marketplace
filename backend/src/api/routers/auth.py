from fastapi import APIRouter, Request, Response

from schemas.auth import AuthenticateUserSchema, AccessTokenSchema
from schemas.base import SuccessResponseSchema
from api.dependencies import AuthServiceDep, SessionDep, CredentialsDep
from utils.auth import set_refresh_token_cookie


router = APIRouter(
    prefix='/auth', 
    tags=['Authentication']
)


@router.post('/login', response_model=AccessTokenSchema)
async def login(
    data: AuthenticateUserSchema,
    auth_service: AuthServiceDep,
    session: SessionDep,
    response: Response
):
    tokens = await auth_service.get_auth_tokens_by_email_and_password(
        session, 
        data
    )

    set_refresh_token_cookie(tokens.get('refresh'), response)
    
    return {'access_token': tokens.get('access')}


@router.post('/logout', response_model=SuccessResponseSchema)
async def logout(
    request: Request,
    response: Response
):
    refresh_token = request.cookies.get('refresh_token')
    
    if not refresh_token:
        return {'success': False}
        
    response.delete_cookie(key='refresh_token')
    return {'success': True}
    

@router.get('/tokens', response_model=AccessTokenSchema)
async def update_access_token(
    request: Request,
    auth_service: AuthServiceDep,
    session: SessionDep,
):
    refresh_token = request.cookies.get('refresh_token')

    new_access_token = await auth_service.get_access_token_by_refresh(
        session, 
        refresh_token
    )
    
    return {'access_token': new_access_token}


@router.post('/tokens/verify', response_model=SuccessResponseSchema)
async def verify_user(
    auth_service: AuthServiceDep,
    session: SessionDep,
    credentials: CredentialsDep
):
    await auth_service.verify_token(
        session, 
        credentials.credentials
    )
    return {'success': True}
