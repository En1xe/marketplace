from fastapi import APIRouter

from core.security.encryptors.redirect_encryption import redirect_encryptor
from schemas.redirect_tokens import RedirectTokenSchema
from schemas.verification_codes import VerificationCodeOnlySchema


router = APIRouter(
    prefix='/redirect_tokens', 
    tags=['Secure tokens']
)


@router.post('', response_model=RedirectTokenSchema)
async def create_secure_token(
    code: VerificationCodeOnlySchema
):
    token = redirect_encryptor.encrypt({'code': code.code})
    return {'token': token}


@router.get('')
async def get_secure_token_data(
    token: str
):
    return redirect_encryptor.decrypt(token)
