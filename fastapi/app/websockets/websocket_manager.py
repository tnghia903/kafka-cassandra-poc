import json
from fastapi import WebSocket


class WebSocketManager:
    def __init__(self) -> None:
        self.active_connection: list[WebSocket] = []

    async def connect(self, websocket: WebSocket):
        await websocket.accept()
        self.active_connection.append(websocket)

    def disconnect(self, websocket: WebSocket):
        self.active_connection.remove(websocket)

    async def websocket_endpoint(self, websocket: WebSocket):
        await websocket.accept()
        while True:
            data = await websocket.receive_text()
            await websocket.send_text(data)


websocket_manager = WebSocketManager()


async def websocket_endpoint(websocket: WebSocket, chat_id: str):
    await websocket_manager.websocket_endpoint(websocket)
