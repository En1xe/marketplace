from uuid import UUID
from fastapi import APIRouter, Request

from api.dependencies import (
    ChatsServiceDep, 
    SessionDep, 
    CurrentUserDep,
)
from core.decorators.auth import is_admin
from schemas.chats import ChatsSchema, CreateChatsSchema, DetailChatsSchema


router = APIRouter(
    prefix='/chats', 
    tags=['Chats']
)

@router.get('', response_model=list[ChatsSchema])
async def get_chats(
    session: SessionDep,
    service: ChatsServiceDep,
    current_user: CurrentUserDep,
    listing_id: int | None = None
):
    return await service.get_all_chats(
        session, 
        request_user=current_user,
        listing_id=listing_id
    )


@router.get('/{chat_uuid}', response_model=DetailChatsSchema)
async def get_chat(
    chat_uuid: UUID,
    session: SessionDep,
    service: ChatsServiceDep,
    current_user: CurrentUserDep
):
    return await service.get_chat_by_uuid(
        session, 
        chat_uuid, 
        request_user=current_user
    )
    

@router.post('', response_model=ChatsSchema)
@is_admin
async def create_chat(
    request: Request,
    data: CreateChatsSchema,
    session: SessionDep,
    service: ChatsServiceDep
):
    return await service.add_one_chat(session, data)


@router.post('/with_participants', response_model=ChatsSchema)
async def create_chat_with_participants(
    data: CreateChatsSchema,
    session: SessionDep,
    chats_service: ChatsServiceDep,
    current_user: CurrentUserDep
):
    return await chats_service.add_one_chat_with_participants(
        session,
        data,
        request_user=current_user
    )


@router.delete('/{chat_uuid}', status_code=204)
async def delete_chat(
    chat_uuid: UUID,
    session: SessionDep,
    service: ChatsServiceDep,
    current_user: CurrentUserDep
):
    await service.delete_one_chat(
        session, 
        chat_uuid=chat_uuid, 
        request_user=current_user
    )