from src.models.ai_models import AIModel
from src.services import provider_service


def test_get_models():
    """Test the model service get_model method."""
    # Get models
    result = provider_service.get_available_models()

    # Assertions
    assert isinstance(result, list)
    assert all(isinstance(model, AIModel) for model in result)

    known_providers = provider_service.get_available_providers()
    assert all(model.provider in known_providers for model in result)
