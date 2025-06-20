from typing import Any
from fastapi import Response, status
from fastapi.testclient import TestClient
from requests_mock import Mocker

from src.models.ai_models import AIModel, AIModelType
from src.models.messages import ContentType, Message, MessageRole, MessageThread
from src.services.lmstudio import LMStudio
from src.api.converse_api import ConverseRequest


def test_converse_endpoint(client: TestClient, requests_mock: Mocker) -> None:
    lmstudio = LMStudio()

    # Mock the response for the models endpoint
    requests_mock.post(
        url=lmstudio.base_url + lmstudio.CONVERSE_ENDPOINT,
        json={
            "choices": [
                {
                    "message": {
                        "role": "assistant",
                        "content": "Hello! How can I assist you today?",
                    },
                    "finish_reason": "stop",
                }
            ]
        },
    )

    # Send request
    con_req = ConverseRequest(
        model=AIModel(
            id="lmstudio-model",
            alias="lmstudio-model",
            provider=lmstudio.name,
            type=AIModelType.CHAT,
        ),
        message_thread=MessageThread(
            title="Test Thread",
            messages=[
                Message(
                    role=MessageRole.USER,
                    content_type=ContentType.TEXT,
                    content="Hello, AI!",
                )
            ],
            modified_at="2022-09-27 18:00:00.000",
        ),
    ).model_dump()
    response: Response = client.post(  # type: ignore
        "/api/v1/converse/",
        json=con_req,
    )

    # Validate the response status code
    assert response.status_code == status.HTTP_200_OK

    # Validate the response data
    data: dict[str, Any] = response.json()
    assert isinstance(data, dict)
    assert "role" in data and data["role"] == "assistant"
    assert "content" in data and isinstance(data["content"], str)
    assert data["content"] == "Hello! How can I assist you today?"
    assert "content_type" in data and data["content_type"] == "text"
