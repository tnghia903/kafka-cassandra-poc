from uuid import UUID
from pydantic import BaseModel


class Message(BaseModel):
    chat_id: str
    message_id: str
    content: str
    sender_id: str
    timestamp: int
