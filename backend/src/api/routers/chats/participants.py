from fastapi import APIRouter, Request

from api.dependencies import ChatParticipantsServiceDep, SessionDep
from core.decorators.auth import is_admin
from schemas.chats import (
    ChatParticipantsSchema, 
    CreateParticipantsSchema,
)


router = APIRouter(
    prefix='/chats/participants', 
    tags=['Chat participants']
)

@router.get('', response_model=list[ChatParticipantsSchema])
@is_admin
async def get_chat_participants(
    request: Request,
    session: SessionDep,
    service: ChatParticipantsServiceDep,
):
    return await service.get_all_chat_participants(session)


@router.get('/{chat_participant_id}', 
            response_model=ChatParticipantsSchema)
@is_admin
async def get_chat_participant(
    request: Request,
    chat_participant_id: int,
    session: SessionDep,
    service: ChatParticipantsServiceDep
):
    chat_participant = await service.get_chat_participant_by_id(
        session, 
        chat_participant_id
    )
    return chat_participant
    

@router.post('', response_model=ChatParticipantsSchema)
@is_admin
async def create_chat_participant(
    request: Request,
    data: CreateParticipantsSchema,
    session: SessionDep,
    service: ChatParticipantsServiceDep
):
    chat_participant = await service.add_one_chat_participant(
        session, 
        data
    )
    return chat_participant


@router.delete('/{chat_participant_id}', status_code=204)
@is_admin
async def delete_chat_participant(
    request: Request,
    chat_participant_id: int,
    session: SessionDep,
    service: ChatParticipantsServiceDep
):
    await service.delete_one_chat_participant(
        session, 
        chat_participant_id
    )