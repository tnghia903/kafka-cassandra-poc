from time import time
from uuid import uuid4
from fastapi import APIRouter, HTTPException
from fastapi.responses import HTMLResponse

from app.models.message import Message
from app.schemas.message import MessageCreate
from app.services.message_service import MessageService


router = APIRouter()
message_service = MessageService()


@router.get("/", response_class=HTMLResponse)
async def get_form():
    with open("app/html/index.html") as f:
        return HTMLResponse(content=f.read(), status_code=200)


@router.post("/send-message/")
async def send_message(message: MessageCreate):
    try:
        message_data = {
            "chat_id": message.chat_id,
            "message_id": str(uuid4()),
            "content": message.content,
            "sender_id": message.sender_id,
            "timestamp": int(time() * 1000),
        }
        message_service.send_message(message_data)
        return {"message": "Message sent successfully"}
    except Exception as e:
        raise HTTPException(500, str(e))
