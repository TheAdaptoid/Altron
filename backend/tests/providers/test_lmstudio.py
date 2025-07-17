from src.models import AIModel, MessageThread, Message, MessageRole
from src.models.ai_models import AIModelType
from src.providers import LMStudio
from requests_mock import Mocker
import pytest

_lmstudio: LMStudio = LMStudio()
MOCK_MODELS_ENDPOINT: str = "http://" + _lmstudio.base_url + _lmstudio.MODELS_ENDPOINT
MOCK_CONVERSE_ENDPOINT: str = (
    "http://" + _lmstudio.base_url + _lmstudio.CONVERSE_ENDPOINT
)


def test_lmstudio_init():
    lmstudio = LMStudio()
    assert lmstudio.name == "LM Studio"
    assert lmstudio.connected is True


@pytest.mark.parametrize("limit,expected_count", [(2, 2), (1, 1)])
def test_get_models_limit(requests_mock: Mocker, limit: int, expected_count: int):
    lmstudio = LMStudio()
    requests_mock.get(
        url=MOCK_MODELS_ENDPOINT,
        json={
            "data": [
                {"id": "lmstudio-chat-model"},
                {"id": "lmstudio-chat-model-v2"},
                {"id": "lmstudio-chat-model-v3"},
            ]
        },
    )
    models = lmstudio.get_models(limit=limit)
    assert len(models) == expected_count
    assert all(isinstance(model, AIModel) for model in models)
    assert all(model.provider == lmstudio.name for model in models)


def test_get_models_type_filter(requests_mock: Mocker):
    lmstudio = LMStudio()
    requests_mock.get(
        url=MOCK_MODELS_ENDPOINT,
        json={
            "data": [
                {"id": "lmstudio-chat-model"},
                {"id": "embedding-model-v1"},
                {"id": "lmstudio-chat-model-v3"},
            ]
        },
    )
    models = lmstudio.get_models(type_filter=AIModelType.EMBEDDING)
    assert len(models) == 1
    assert models[0].id == "embedding-model-v1"
    assert all(isinstance(model, AIModel) for model in models)
    assert all(model.provider == lmstudio.name for model in models)


def test_get_models_empty_response(requests_mock: Mocker):
    lmstudio = LMStudio()
    requests_mock.get(url=MOCK_MODELS_ENDPOINT, json={"data": []})
    models = lmstudio.get_models()
    assert models == []


def test_get_models_invalid_response(requests_mock: Mocker):
    lmstudio = LMStudio()
    requests_mock.get(url=MOCK_MODELS_ENDPOINT, json={"unexpected": "value"})
    with pytest.raises(ValueError):
        lmstudio.get_models()


def test_converse(requests_mock: Mocker):
    lmstudio = LMStudio()
    requests_mock.get(
        url=MOCK_MODELS_ENDPOINT, json={"data": [{"id": "lmstudio-chat-model"}]}
    )
    requests_mock.post(
        url=MOCK_CONVERSE_ENDPOINT,
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
    model = lmstudio.get_models(limit=1, type_filter=AIModelType.CHAT)[0]
    message_thread = MessageThread(
        messages=[Message(role=MessageRole.USER, content="Hello, how are you?")]
    )
    response = lmstudio.converse(model, message_thread)
    assert isinstance(response.content, str)
    assert response.content == "Hello! How can I assist you today?"
    assert response.role == MessageRole.AGENT


def test_converse_too_long(requests_mock: Mocker):
    lmstudio = LMStudio()
    requests_mock.get(
        url=MOCK_MODELS_ENDPOINT, json={"data": [{"id": "lmstudio-chat-model"}]}
    )
    requests_mock.post(
        url=MOCK_CONVERSE_ENDPOINT,
        json={
            "choices": [
                {
                    "message": {
                        "role": "assistant",
                        "content": "Hello! How ca",
                    },
                    "finish_reason": "length",
                }
            ]
        },
    )
    model = lmstudio.get_models(limit=1, type_filter=AIModelType.CHAT)[0]
    message_thread = MessageThread(
        messages=[Message(role=MessageRole.USER, content="Hello, how are you?")]
    )
    response = lmstudio.converse(model, message_thread)
    assert isinstance(response.content, str)
    assert (
        response.content
        == "Hello! How ca\n\n[[The response was truncated due to length limits.]]"
    )
    assert response.role == MessageRole.AGENT


def test_converse_empty_thread(requests_mock: Mocker):
    lmstudio = LMStudio()
    model = AIModel(
        id="lmstudio-chat-model", provider=lmstudio.name, type=AIModelType.CHAT
    )
    message_thread = MessageThread(messages=[])
    # Optionally mock the endpoint if needed
    mock_url = "http://192.168.1.143:1234/v1/chat/completions"
    requests_mock.post(mock_url, status_code=404)
    with pytest.raises(ValueError):
        lmstudio.converse(model, message_thread)


def test_converse_invalid_message_content():
    lmstudio = LMStudio()
    model = AIModel(
        id="lmstudio-chat-model", provider=lmstudio.name, type=AIModelType.CHAT
    )
    message_thread = MessageThread(
        messages=[Message(role=MessageRole.USER, content=None)]
    )
    with pytest.raises(Exception):
        lmstudio.converse(model, message_thread)
