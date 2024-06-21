from uuid import UUID
from pydantic import BaseModel


class MessageCreate(BaseModel):
    chat_id: str
    content: str
    sender_id: str
