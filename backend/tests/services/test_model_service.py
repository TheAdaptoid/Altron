from src.models.ai_models import AIModel
from src.services import provider_service
import pytest


def test_get_models():
    """Test the model service get_model method."""
    # Get models
    result = provider_service.get_available_models()

    # Assertions
    assert isinstance(result, list)
    assert all(isinstance(model, AIModel) for model in result)

    known_providers = provider_service.get_available_providers()
    assert all(model.provider in known_providers for model in result)


def test_get_provider():
    """Test the model service get_provider method."""
    # Get a specific provider
    provider_name = "OpenAI"  # Replace with an actual provider name
    provider = provider_service.get_provider(provider_name)

    # Assertions
    assert provider is not None
    assert provider.name == provider_name


def test_get_provider_not_found():
    """Test the model service get_provider method with a non-existent provider."""
    # Attempt to get a non-existent provider
    with pytest.raises(ValueError):
        provider_service.get_provider("NonExistent")
