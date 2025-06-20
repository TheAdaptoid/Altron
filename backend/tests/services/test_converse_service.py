from requests_mock import Mocker
from src.models.ai_models import AIModelType
from src.services import converse_service
from src.models import AIModel, MessageThread, Message, MessageRole
from src.services.lmstudio import LMStudio
import pytest


def test_converse(requests_mock: Mocker) -> None:
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

    # Create a mock AI model
    model = AIModel(id="test-model", provider="LM Studio", type=AIModelType.CHAT)

    # Create a mock message thread
    message_thread = MessageThread(
        messages=[
            Message(role=MessageRole.USER, content="Hello, how are you?"),
        ]
    )

    # Call the converse function
    response_message = converse_service.converse(model, message_thread)

    # Check that the response is of type Message
    assert isinstance(response_message, Message)
    assert response_message.role == MessageRole.ASSISTANT


def test_converse_invalid_model_type(requests_mock: Mocker) -> None:
    # Create a mock AI model
    model = AIModel(id="test-model", provider="LM Studio", type=AIModelType.EMBEDDING)

    # Create a mock message thread
    message_thread = MessageThread(
        messages=[
            Message(role=MessageRole.USER, content="Hello, how are you?"),
        ]
    )

    # Call the converse function
    with pytest.raises(ValueError):
        converse_service.converse(model, message_thread)


def test_converse_provider_not_found(requests_mock: Mocker) -> None:
    # Create a mock AI model with a non-existent provider
    model = AIModel(
        id="test-model", provider="NonExistentProvider", type=AIModelType.CHAT
    )

    # Create a mock message thread
    message_thread = MessageThread(
        messages=[
            Message(role=MessageRole.USER, content="Hello, how are you?"),
        ]
    )

    # Call the converse function and expect a ValueError
    with pytest.raises(ValueError):
        converse_service.converse(model, message_thread)
