from fastapi import WebSocket
from uuid import UUID


class ConnectionManager:
    """A manager for working with websocket connections"""
    
    def __init__(self) -> None:
        self.active_connection: dict[UUID, list[WebSocket]] = {}
        
    async def connect(
        self, 
        websocket: WebSocket, 
        chat_uuid: UUID
    ):
        await websocket.accept()
        
        if chat_uuid not in self.active_connection.keys():
            self.active_connection[chat_uuid] = []
        
        chat_connections = self.active_connection[chat_uuid]
        chat_connections.append(websocket)
                
    async def disconnect(
        self,
        websocket: WebSocket,
        chat_uuid: UUID
    ):
        chat_connections = self.active_connection.get(chat_uuid)
        
        if chat_connections:
            chat_connections.remove(websocket)
            
        if not chat_connections:
            del self.active_connection[chat_uuid]
            
    async def send_message(
        self,
        websocket: WebSocket,
        message_data: dict
    ):
        await websocket.send_json(message_data)
                    
    async def broadcast(
        self,
        chat_uuid: UUID,
        message_data: dict
    ):
        chat_connections = self.active_connection.get(chat_uuid)
        
        if not chat_connections: return
        
        for conn in chat_connections:
            await conn.send_json(message_data)
        
        
conn_manager = ConnectionManager()
        