from fastapi import APIRouter, HTTPException

from src.models.schemas import ChatMessage
from src.services.chat_service import ChatService

router = APIRouter()


@router.post("/chat")
async def send_message(message: ChatMessage):
    """Send a chat message.

    This endpoint processes the chat message using the ChatService.
    """
    try:
        result = await ChatService.process_message(message.model_dump())
        return {"status": "success", "data": result}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e)) from e
