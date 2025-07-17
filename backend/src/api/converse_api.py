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
    except TypeError as e:
        logger.error(
            "Invalid model type for conversation",
            exc_info=True,
            extra={"error": str(e)},
        )
        raise HTTPException(status_code=422, detail=str(e)) from e
    except ValueError as e:
        logger.error(
            "Validation error in conversation",
            exc_info=True,
            extra={"error": str(e)},
        )
        # Use 404 for not found, 400 for other validation errors
        if "not found" in str(e):
            raise HTTPException(status_code=404, detail=str(e)) from e
        raise HTTPException(status_code=400, detail=str(e)) from e
    except Exception as e:
        logger.error(
            "Error processing conversation",
            exc_info=True,
            extra={"error": str(e)},
        )
        raise HTTPException(status_code=500, detail=str(e)) from e
