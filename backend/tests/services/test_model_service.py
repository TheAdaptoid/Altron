from src.models.ai_models import AIModel
from src.services import provider_service
import pytest


@pytest.mark.parametrize("provider_name", ["OpenAI", "LM Studio"])
def test_get_provider_valid(provider_name):
    """Test the model service get_provider method with valid providers."""
    provider = provider_service.get_provider(provider_name)

    # Assertions
    assert provider is not None
    assert provider.name == provider_name


def test_get_provider_not_found():
    """Test the model service get_provider method with a non-existent provider."""
    # Attempt to get a non-existent provider
    with pytest.raises(ValueError):
        provider_service.get_provider("NonExistent")


def test_get_available_models_type_and_provider():
    """Test the model service get_available_models method for type and provider."""
    # Get models
    models = provider_service.get_available_models()

    # Assertions
    assert isinstance(models, list)
    assert all(isinstance(model, AIModel) for model in models)

    known_providers = provider_service.get_available_providers()
    assert all(model.provider in known_providers for model in models)


def test_get_available_models_empty(monkeypatch):
    """Test the model service get_available_models method with no available providers."""
    # Simulate no available providers
    monkeypatch.setattr(provider_service, "get_available_providers", lambda: [])

    # Get models
    models = provider_service.get_available_models()

    # Assertions
    assert models == []
