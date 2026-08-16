from pydantic import BaseModel, IPvAnyAddress
from datetime import datetime


class CreateMessage(BaseModel):
    message: str
    room_key: str


class Message(CreateMessage):
    id: int
    sender_ip: IPvAnyAddress
    created_at: datetime


class ReceiveMessage(BaseModel):
    message: str
    sender_ip: str
