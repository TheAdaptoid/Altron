from fastapi import APIRouter, HTTPException

from src.models import AIModel, AIModelType
from src.services import provider_service
from src.utils import setup_logger

logger = setup_logger(__name__)
router = APIRouter(prefix="/providers", tags=["providers"])


@router.get(path="/", response_model=list[str])
async def get_providers() -> list[str]:
    """Get a list of available AI model providers."""
    try:
        return list(provider_service.get_available_providers())
    except Exception as e:
        logger.error(
            "Error retrieving providers", exc_info=True, extra={"error": str(e)}
        )
        raise HTTPException(status_code=500, detail=str(e)) from e


@router.get(path="/{provider_name}/models", response_model=list[AIModel])
async def get_provider_models(
    provider_name: str, limit: int | None = None, type_filter: AIModelType | None = None
) -> list[AIModel]:
    """Get a list of AI models from a specific provider."""
    try:
        return provider_service.get_provider_models(provider_name, limit, type_filter)
    except ValueError as ve:
        logger.error(
            f"Provider '{provider_name}' not found",
            exc_info=True,
            extra={"error": str(ve)},
        )
        raise HTTPException(status_code=404, detail=str(ve)) from ve
    except Exception as e:
        logger.error(
            f"Error retrieving models from provider {provider_name}",
            exc_info=True,
            extra={"error": str(e)},
        )
        raise HTTPException(status_code=500, detail=str(e)) from e


@router.get(path="/models", response_model=list[AIModel])
async def get_all_models(
    limit: int | None = None, type_filter: AIModelType | None = None
) -> list[AIModel]:
    """Get a list of available AI models."""
    try:
        return provider_service.get_available_models(limit, type_filter)
    except Exception as e:
        logger.error("Error retrieving models", exc_info=True, extra={"error": str(e)})
        raise HTTPException(status_code=500, detail=str(e)) from e
