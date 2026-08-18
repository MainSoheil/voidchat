from typing import List
from fastapi import FastAPI, Depends, WebSocket, WebSocketDisconnect, Request, HTTPException
from starlette.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from contextlib import asynccontextmanager
from settings import database
import sqlite3
from settings.schema import CreateMessage, ReceiveMessage
from settings.websocketManager import wsManager
from pathlib import Path


@asynccontextmanager
async def lifespan(application: FastAPI):
    database.init_db()
    yield


app = FastAPI(
    title="VOIDCHAT API",
    description="Backend API for VOIDCHAT anonymous chat platform",
    version="1.0.0",
    lifespan=lifespan
)
REACT_BUILD_DIR = Path('dist')


@app.post("/messages")
def create_message(message: CreateMessage, request: Request, db: sqlite3.Connection = Depends(database.get_db)):
    ip = request.client.host if request.client else None
    cursor = db.execute("INSERT INTO messages (sender_ip, message, room_key) VALUES (?, ?, ?)", (ip, message.message, message.room_key))
    db.commit()
    return {'id': cursor.lastrowid, 'ip': ip, **message.model_dump()}


@app.get("/messages/{room_key}", response_model=List[ReceiveMessage])
def all_messages(room_key: str, db: sqlite3.Connection = Depends(database.get_db)):
    cursor = db.execute("SELECT message, sender_ip FROM messages WHERE room_key = ? ORDER BY created_at DESC", (room_key,))
    messages = reversed([dict(row) for row in cursor.fetchall()])
    return messages


@app.get("/ip")
async def get_ip(request: Request):
    ip = request.client.host if request.client else None
    return {'ip': ip}


@app.websocket("/ws/{room_key}")
async def chat(websocket: WebSocket, room_key: str):
    await wsManager.connect(room_key, websocket)
    try:
        while True:
            data = await websocket.receive_json()
            if not data.get("message", "").strip():
                continue
            await wsManager.broadcast(room_key, data)
    except WebSocketDisconnect:
        await wsManager.disconnect(room_key, websocket)


@app.get("/{path:path}")
async def catch_all_routes(path: str):
    if path.startswith("api/"):
        raise HTTPException(status_code=404, detail="API endpoint not found")
    file_path = REACT_BUILD_DIR / path
    if file_path.is_file():
        return FileResponse(file_path)
    return FileResponse(str(REACT_BUILD_DIR / "index.html"))


app.mount("/", StaticFiles(directory=str(REACT_BUILD_DIR), html=True), name="static")
