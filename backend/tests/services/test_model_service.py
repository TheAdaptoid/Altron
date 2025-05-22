import pytest

from src.models.ai_models import AIModel
from src.services.model_service import ModelService


@pytest.mark.asyncio
async def test_model_service_get_model():
    """Test the model service get_model method."""
    # Get model
    result = await ModelService.get_available_models()

    # Assertions
    assert isinstance(result, list)
    assert isinstance(result[0], AIModel)
