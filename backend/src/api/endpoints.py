from fastapi import APIRouter

from src.api.providers_api import router as provider_router

router = APIRouter()


@router.get("/health")
async def health_check():
    """Health check endpoint."""
    return {"status": "healthy"}


# Include model routes
router.include_router(provider_router, prefix="/providers", tags=["providers"])
