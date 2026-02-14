from fastapi import APIRouter, WebSocket, WebSocketDisconnect
from uuid import UUID

from core.managers.chats import conn_manager

router = APIRouter(
    prefix='/chats/{chat_uuid}/ws', 
    tags=['Chat participants']
)

@router.websocket('')
async def websocket_endpoint(
    chat_uuid: UUID,
    websocket: WebSocket,
):
    await conn_manager.connect(
        websocket=websocket,
        chat_uuid=chat_uuid
    )
    
    try:
        while True:
            data = await websocket.receive_json()
            
            await conn_manager.broadcast(
                chat_uuid, 
                data
            )
    except WebSocketDisconnect:
        await conn_manager.disconnect(
            websocket=websocket,
            chat_uuid=chat_uuid
        )
