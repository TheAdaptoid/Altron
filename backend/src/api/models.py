from fastapi import APIRouter, HTTPException

from src.models.ai_models import AIModel
from src.services.model_service import ModelService
from src.utils.logger import setup_logger

logger = setup_logger(__name__)
router = APIRouter()


@router.get(path="/", response_model=list[AIModel])
async def get_models() -> list[AIModel]:
    """Get a list of available AI models."""
    try:
        return await ModelService.get_available_models()
    except Exception as e:
        logger.error("Error retrieving models", exc_info=True, extra={"error": str(e)})
        raise HTTPException(status_code=500, detail=str(e)) from e
