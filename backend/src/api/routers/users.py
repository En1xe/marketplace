from uuid import UUID
from fastapi import APIRouter, Body

from core.security.encryptors.redirect_encryption import redirect_encryptor
from api.dependencies import (
    UsersServiceDep, 
    VerificationCodesServiceDep,
    SessionDep, 
    CurrentUserDep, 
    S3ClientDep, 
    UploadedImageDep,
    CurrentAdminUserDep
)
from schemas.users import (
    UsersSchema, 
    CreateUsersSchema, 
    UpdateUsersSchema,
    UpdateUsersSchemaWithinRecovery,
    get_user_schema,
    get_detail_user_schema
)

router = APIRouter(
    prefix='/users', 
    tags=['Users']
)

@router.get('')
async def get_users(
    session: SessionDep,
    service: UsersServiceDep,
    curr_user: CurrentUserDep
):
    users = await service.get_all_users(session)
    return [
        get_user_schema(user, curr_user) 
        for user in users
    ]


@router.get('/token')
async def get_user_by_token(
    curr_user: CurrentUserDep,
    service: UsersServiceDep,
):
    return await service.get_one_by_token(
        curr_user
    )


@router.get('/{user_uuid}')
async def get_user(
    user_uuid: UUID,
    session: SessionDep,
    service: UsersServiceDep,
    curr_user: CurrentUserDep,
    detail: bool = False
):  
    user = await service.get_one_by_field(
        session,
        uuid=user_uuid
    )

    response = get_detail_user_schema(user, curr_user) if detail \
                else get_user_schema(user, curr_user) 

    return response


@router.post('/email')
async def get_user_by_email(
    session: SessionDep,
    service: UsersServiceDep,
    curr_user: CurrentUserDep,
    email: str = Body(embed=True),
):
    user = await service.get_one_by_field(
        session, 
        email=email
    )
    return get_user_schema(user, curr_user)
    

@router.post('')
async def create_user(
    data: CreateUsersSchema,
    session: SessionDep,
    service: UsersServiceDep
):
    user = await service.add_one_user(
        session, 
        data
    )
    return user


@router.patch('/{user_uuid}', response_model=UsersSchema)
async def update_user(
    user_uuid: UUID,
    data: UpdateUsersSchema,
    session: SessionDep,
    service: UsersServiceDep,
    curr_user: CurrentUserDep,
):
    user = await service.update_one_user(
        session, 
        data=data, 
        user_uuid=user_uuid,
        request_user=curr_user
    )
    return user


@router.patch('/redirect_token')
async def update_user_within_recovery(
    data: UpdateUsersSchemaWithinRecovery,
    session: SessionDep,
    user_service: UsersServiceDep,
    verify_codes_service: VerificationCodesServiceDep,
):
    code = redirect_encryptor.decrypt(data.token).get('code')
    
    verify_code = await verify_codes_service.validate_and_confirm_verification_code(
        session,
        data.verify_code_uuid, 
        code
    )
    
    user_uuid = verify_code.user.uuid

    user = await user_service.update_one_user_within_recovery(
        session, 
        data=UpdateUsersSchema(password=data.password), 
        user_uuid=user_uuid,
    )
    return user


@router.delete('/{user_uuid}', status_code=204)
async def delete_user(
    user_uuid: UUID,
    session: SessionDep,
    service: UsersServiceDep,
    current_user: CurrentAdminUserDep
):
    await service.delete_one_user(
        session, 
        user_uuid=user_uuid, 
        request_user=current_user
    )
    
    
@router.post('/{user_uuid}/avatar', response_model=UsersSchema)
async def upload_user_avatar(
    user_uuid: UUID,
    session: SessionDep,
    client: S3ClientDep,
    service: UsersServiceDep,
    current_user: CurrentUserDep,
    image: UploadedImageDep
):
    return await service.upload_one_user_avatar(
        session=session,
        s3_client=client,
        image=image,
        user_uuid=user_uuid,
        request_user=current_user
    )
    