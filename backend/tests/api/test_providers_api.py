from typing import Any

from fastapi import Response, status
from fastapi.testclient import TestClient
from src.models.ai_models import AIModel
import pytest


@pytest.mark.parametrize("provider_name", ["OpenAI", "LM Studio"])
def test_providers_endpoint(client: TestClient, provider_name: str):
    """Test the AI model endpoint."""
    # Send request
    response: Response = client.get("/api/v1/providers/")

    # Validate the response status code
    assert response.status_code == status.HTTP_200_OK

    # Validate the response data
    data: list[Any] = response.json()
    assert isinstance(data, list)
    assert provider_name in data
    assert all(isinstance(item, str) for item in data)  # Ensure all items are strings


def test_provider_models_endpoint(client: TestClient):
    """Test the provider models endpoint."""
    # Send request
    response: Response = client.get("/api/v1/providers/OpenAI/models")

    # Validate the response status code
    assert response.status_code == status.HTTP_200_OK

    # Validate the response data
    data: list[AIModel] = [AIModel(**model) for model in response.json()]
    assert isinstance(data, list)
    assert all(
        isinstance(item, AIModel) for item in data
    )  # Ensure all items are AIModel instances
    assert all(
        model.provider == "OpenAI" for model in data
    )  # Ensure all models are from openai


def test_provider_models_invalid(client: TestClient):
    """Test the provider models endpoint with an invalid provider."""
    # Send request
    response: Response = client.get("/api/v1/providers/NonExistent/models")

    # Validate the response status code
    assert (
        response.status_code == status.HTTP_404_NOT_FOUND
        or response.status_code == status.HTTP_400_BAD_REQUEST
    )


def test_all_models_endpoint(client: TestClient):
    """Test the all models endpoint."""
    # Send request
    response: Response = client.get("/api/v1/providers/models")

    # Validate the response status code
    assert response.status_code == status.HTTP_200_OK

    # Validate the response data
    data: list[AIModel] = [AIModel(**model) for model in response.json()]
    assert isinstance(data, list)
    assert all(
        isinstance(item, AIModel) for item in data
    )  # Ensure all items are AIModel instances
    valid_providers = client.get("/api/v1/providers/").json()
    assert all(
        model.provider in valid_providers for model in data
    )  # Ensure models are from known providers


def test_wrong_method_provider_models(client: TestClient):
    """Test the provider models endpoint with a wrong HTTP method."""
    response: Response = client.post("/api/v1/providers/OpenAI/models")
    assert response.status_code in (
        status.HTTP_405_METHOD_NOT_ALLOWED,
        status.HTTP_400_BAD_REQUEST,
    )
