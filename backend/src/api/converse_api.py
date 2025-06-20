from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

from src.models import AIModel, Message, MessageThread
from src.services import converse_service
from src.utils import setup_logger

logger = setup_logger(__name__)
router = APIRouter(prefix="/converse", tags=["converse"])


class ConverseRequest(BaseModel):
    """Request model for the converse endpoint."""

    model: AIModel
    message_thread: MessageThread


@router.post(path="/")
async def converse(converse_request: ConverseRequest) -> Message:
    """Send a message to the AI model and get a response."""
    try:
        return converse_service.converse(
            converse_request.model, converse_request.message_thread
        )
    except Exception as e:
        logger.error(
            "Error processing conversation",
            exc_info=True,
            extra={"error": str(e)},
        )
        raise HTTPException(status_code=500, detail=str(e)) from e
