from typing import Any
from fastapi import Response, status
from fastapi.testclient import TestClient
from requests_mock import Mocker
from src.models.ai_models import AIModel, AIModelType
from src.models.messages import Message, MessageRole, MessageThread
from src.api.converse_api import ConverseRequest
import pytest


@pytest.mark.parametrize(
    "provider_name,model_id",
    [
        ("LM Studio", "lmstudio-model"),
        ("OpenAI", "gpt-4o-mini"),
    ],
)
def test_converse_endpoint(
    client: TestClient, requests_mock: Mocker, provider_name: str, model_id: str
):
    from src.models.messages import UserMessage

    if provider_name == "LM Studio":
        from src.providers.lmstudio import LMStudio

        lmstudio = LMStudio()
        # Mock both possible LM Studio addresses
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
        requests_mock.post(
            url="http://192.168.1.143:1234/v1/chat/completions",
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
        messages = [Message(role=MessageRole.USER, content="Hello, AI!")]
    elif provider_name == "OpenAI":
        messages = [UserMessage(content="Hello, AI!")]
    con_req = ConverseRequest(
        model=AIModel(
            id=model_id,
            alias=model_id,
            provider=provider_name,
            type=AIModelType.CHAT,
        ),
        message_thread=MessageThread(
            title="Test Thread",
            messages=messages,
            modified_at="2022-09-27 18:00:00.000",
        ),
    ).model_dump()
    response: Response = client.post("/api/v1/converse/", json=con_req)
    assert response.status_code == status.HTTP_200_OK
    data: dict[str, Any] = response.json()
    assert isinstance(data, dict)
    assert "role" in data and data["role"] == "assistant"
    assert "content" in data and isinstance(data["content"], str)
    assert data["content"] == "Hello! How can I assist you today?"


def test_converse_endpoint_empty_thread(client: TestClient):
    # Only use the correct construction below
    con_req = ConverseRequest(
        model=AIModel(
            id="lmstudio-model",
            alias="lmstudio-model",
            provider="LM Studio",
            type=AIModelType.CHAT,
        ),
        message_thread=MessageThread(
            title="Empty Thread", messages=[], modified_at="2022-09-27 18:00:00.000"
        ),
    ).model_dump()
    response = client.post("/api/v1/converse/", json=con_req)
    assert response.status_code == status.HTTP_400_BAD_REQUEST


def test_converse_endpoint_wrong_method(client: TestClient):
    response = client.get("/api/v1/converse/")
    assert response.status_code in (
        status.HTTP_405_METHOD_NOT_ALLOWED,
        status.HTTP_400_BAD_REQUEST,
    )
