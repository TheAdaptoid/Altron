import pytest
from requests_mock import Mocker
from src.models.ai_models import AIModelType
from src.services import converse_service
from src.models import AIModel, MessageThread, Message, MessageRole
from src.providers import LMStudio


@pytest.mark.parametrize(
    "model_type,expected_role",
    [
        (AIModelType.CHAT, MessageRole.AGENT),
        (AIModelType.EMBEDDING, None),
    ],
)
def test_converse_model_types(
    requests_mock: Mocker, model_type: AIModelType, expected_role: MessageRole | None
):
    lmstudio = LMStudio()
    model = AIModel(id="test-model", provider="LM Studio", type=model_type)
    message_thread = MessageThread(
        messages=[Message(role=MessageRole.USER, content="Hello?")]
    )

    if model_type == AIModelType.CHAT:
        # Use the actual host for LMStudio
        mock_url = "http://192.168.1.143:1234/v1/chat/completions"
        requests_mock.post(
            url=mock_url,
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
        response_message = converse_service.converse(model, message_thread)
        assert isinstance(response_message, Message)
        assert response_message.role == expected_role
        assert response_message.content == "Hello! How can I assist you today?"
    else:
        with pytest.raises(TypeError):
            converse_service.converse(model, message_thread)


def test_converse_empty_message_thread():
    model = AIModel(id="test-model", provider="LM Studio", type=AIModelType.CHAT)
    message_thread = MessageThread(messages=[])
    with pytest.raises(ValueError):
        converse_service.converse(model, message_thread)


def test_converse_invalid_message_content():
    model = AIModel(id="test-model", provider="LM Studio", type=AIModelType.CHAT)
    message_thread = MessageThread(
        messages=[Message(role=MessageRole.USER, content=None)]
    )
    with pytest.raises(Exception):
        converse_service.converse(model, message_thread)
