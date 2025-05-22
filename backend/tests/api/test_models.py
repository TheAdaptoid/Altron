import pytest
from fastapi import Response, status

from src.models.ai_models import AIModel


@pytest.mark.asyncio
async def test_ai_model_endpoint(client):
    """Test the AI model endpoint."""
    # Send request
    response: Response = client.get("/api/v1/models/")

    # Validate the response status code
    assert response.status_code == status.HTTP_200_OK

    # Validate the response data
    data = response.json()
    assert isinstance(data, list)
    assert isinstance(data[0], dict)
    assert AIModel(**data[0])  # Validate the first item against the AIModel schema
