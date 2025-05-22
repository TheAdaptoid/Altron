from fastapi import APIRouter, HTTPException

from src.models.ai_models import AIModel
from src.services.model_service import ModelService

router = APIRouter()


@router.get("/models", response_model=list[AIModel])
async def get_models() -> list[AIModel]:
    """Get a list of available AI models."""
    try:
        # Placeholder for actual model retrieval logic
        return await ModelService.get_available_models()
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e)) from e
