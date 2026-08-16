from typing import Dict, List
from fastapi import WebSocket
from settings import database
import sqlite3
import asyncio


class ConnectionManager:
    def __init__(self):
        # room_key -> list of active WebSocket connections
        self.active_connections: Dict[str, List[WebSocket]] = {}

    async def connect(self, room_key: str, websocket: WebSocket):
        await websocket.accept()
        if room_key not in self.active_connections:
            self.active_connections[room_key] = []
        self.active_connections[room_key].append(websocket)

    async def disconnect(self, room_key: str, websocket: WebSocket):
        if room_key in self.active_connections:
            self.active_connections[room_key].remove(websocket)
            # Clean up empty rooms
            if not self.active_connections[room_key]:
                del self.active_connections[room_key]
                await asyncio.to_thread(clear_room, room_key)

    async def broadcast(self, room_key: str, message: dict):
        """Send a message to all connections in a room."""
        if room_key in self.active_connections:
            for connection in self.active_connections[room_key]:
                await connection.send_json(message)


def clear_room(room_key: str):
    with sqlite3.connect(database.DATABASE_PATH) as conn:
        conn.execute("DELETE FROM messages WHERE room_key = ?", (room_key,))
        conn.commit()


# Global instance (can be imported anywhere)
wsManager = ConnectionManager()
