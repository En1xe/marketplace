from uuid import UUID
from fastapi import APIRouter, BackgroundTasks

from utils.emails import send_email_async
from api.dependencies import SessionDep, VerificationCodesServiceDep
from schemas.verification_codes import (
    VerificationCodeCreateSchema,
    VerificationCodeOnlySchema,
    SecuredVerificationCodeSchema
)
from schemas.base import SuccessResponseSchema


router = APIRouter(
    prefix='/verification_codes', 
    tags=['verification codes']
)

@router.get('/{verification_code_uuid}', response_model=SecuredVerificationCodeSchema)
async def get_verification_code(
    verification_code_uuid: UUID,
    session: SessionDep,
    service: VerificationCodesServiceDep,
):
    return await service.get_one_verification_code(
        session, 
        uuid=verification_code_uuid
    )


@router.post('/', response_model=SecuredVerificationCodeSchema)
async def add_verification_code(
    data: VerificationCodeCreateSchema,
    background_tasks: BackgroundTasks,
    session: SessionDep,
    service: VerificationCodesServiceDep,
):
    verification_code = await service.add_one_verification_code(
        session, 
        data=data
    )

    background_tasks.add_task(
        send_email_async, 
        to_email=data.email,
        subject='Verification code',
        body=f'Verification code: {verification_code.code}'
    )

    return verification_code


@router.post(
    '/{verification_code_uuid}/verify', 
    response_model=SuccessResponseSchema
)
async def check_verification_code(
    verification_code_uuid: UUID,
    session: SessionDep,
    service: VerificationCodesServiceDep,
):
    await service.validate_verification_code(
        session, 
        uuid=verification_code_uuid
    )
    
    return {'success': True}


@router.post(
    '/{verification_code_uuid}/confirm', 
    response_model=SuccessResponseSchema
)
async def confirm_verification_code(
    verification_code: VerificationCodeOnlySchema,
    verification_code_uuid: UUID,
    session: SessionDep,
    service: VerificationCodesServiceDep,
):
    await service.confirm_verification_code(
        session,
        uuid=verification_code_uuid, 
        code=verification_code.code
    )
    
    return {'success': True}