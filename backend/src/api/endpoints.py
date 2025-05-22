from fastapi import APIRouter

from src.api.models import router as model_router

router = APIRouter()


@router.get("/health")
async def health_check():
    """Health check endpoint."""
    return {"status": "ok"}


# Include model routes
router.include_router(model_router, prefix="/models", tags=["models"])
