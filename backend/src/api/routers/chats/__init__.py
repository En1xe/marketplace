from fastapi import APIRouter

from .core import router as chats_router
from .messages import router as chat_messages_router
from .participants import router as chat_participants_router
from .ws import router as chat_websocket_router


main_chats_router = APIRouter()

main_chats_router.include_router(chat_participants_router)
main_chats_router.include_router(chat_messages_router)
main_chats_router.include_router(chats_router)
main_chats_router.include_router(chat_websocket_router)
