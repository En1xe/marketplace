from uuid import UUID
from fastapi import APIRouter, Request

from api.dependencies import ChatMessagesServiceDep, SessionDep, CurrentUserDep
from core.decorators.auth import is_admin
from schemas.chats import (
    ChatMessagesSchema, 
    CreateChatMessagesSchema, 
    UpdateChatMessagesSchema
)


router = APIRouter(
    prefix='/chats/messages', 
    tags=['Chat messages']
)

@router.get('', response_model=list[ChatMessagesSchema])
async def get_chat_messages(
    session: SessionDep,
    service: ChatMessagesServiceDep,
    current_user: CurrentUserDep
):
    return await service.get_all_chat_messages(
        session, 
        request_user=current_user
    )


@router.get('/{chat_message_uuid}', response_model=ChatMessagesSchema)
@is_admin
async def get_chat_message(
    request: Request,
    chat_message_uuid: UUID,
    session: SessionDep,
    service: ChatMessagesServiceDep
):
    return await service.get_chat_message_by_uuid(
        session, 
        chat_message_uuid
    )
    

@router.post('', response_model=ChatMessagesSchema)
async def create_chat_message(
    data: CreateChatMessagesSchema,
    session: SessionDep,
    service: ChatMessagesServiceDep,
    current_user: CurrentUserDep
):
    return await service.add_one_chat_message(
        session, 
        data, 
        request_user=current_user
    )


@router.patch('/{chat_message_uuid}', response_model=ChatMessagesSchema)
async def update_chat_message(
    chat_message_uuid: UUID,
    data: UpdateChatMessagesSchema,
    session: SessionDep,
    service: ChatMessagesServiceDep,
    current_user: CurrentUserDep
):
    return await service.update_one_chat_message(
        session, 
        data, 
        chat_message_uuid,
        request_user=current_user
    )


@router.delete('/{chat_message_uuid}', status_code=204)
async def delete_chat_message(
    chat_message_uuid: UUID,
    session: SessionDep,
    service: ChatMessagesServiceDep,
    current_user: CurrentUserDep
):
    print(chat_message_uuid)
    await service.delete_one_chat_message(
        session, 
        chat_message_uuid, 
        request_user=current_user
    )