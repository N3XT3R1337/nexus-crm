from typing import Dict, Set
from fastapi import WebSocket


class ConnectionManager:
    def __init__(self):
        self.active_connections: Dict[str, Set[WebSocket]] = {}

    async def connect(self, websocket: WebSocket, user_id: str):
        await websocket.accept()
        if user_id not in self.active_connections:
            self.active_connections[user_id] = set()
        self.active_connections[user_id].add(websocket)

    def disconnect(self, websocket: WebSocket, user_id: str):
        if user_id in self.active_connections:
            self.active_connections[user_id].discard(websocket)
            if not self.active_connections[user_id]:
                del self.active_connections[user_id]

    async def send_personal(self, message: dict, user_id: str):
        if user_id in self.active_connections:
            for connection in self.active_connections[user_id]:
                try:
                    await connection.send_json(message)
                except Exception:
                    self.active_connections[user_id].discard(connection)

    async def broadcast(self, message: dict, exclude: str = None):
        for user_id, connections in self.active_connections.items():
            if user_id != exclude:
                for connection in connections.copy():
                    try:
                        await connection.send_json(message)
                    except Exception:
                        connections.discard(connection)

    async def send_to_org(self, message: dict, user_ids: list):
        for user_id in user_ids:
            await self.send_personal(message, user_id)


manager = ConnectionManager()
