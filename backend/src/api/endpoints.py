from fastapi import APIRouter

from src.api.chat import router as chat_router
from src.api.models import router as model_router

router = APIRouter()


@router.get("/health")
async def health_check():
    """Health check endpoint."""
    return {"status": "ok"}


# Include chat routes
router.include_router(chat_router, prefix="/chat", tags=["chat"])

# Include model routes
router.include_router(model_router, prefix="/models", tags=["models"])
