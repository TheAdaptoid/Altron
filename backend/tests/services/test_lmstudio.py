from src.models import AIModel, MessageThread, Message, MessageRole
from src.models.ai_models import AIModelType
from src.models.messages import ContentType
from src.services.lmstudio import LMStudio
from requests_mock import Mocker


def test_get_models(requests_mock: Mocker) -> None:
    lmstudio = LMStudio()

    # Mock the response for the models endpoint
    requests_mock.get(
        url=lmstudio.base_url + lmstudio.MODELS_ENDPOINT,
        json={
            "data": [
                {
                    "id": "lmstudio-chat-model",
                },
                {
                    "id": "lmstudio-chat-model-v2",
                },
                {
                    "id": "lmstudio-chat-model-v3",
                },
            ]
        },
    )

    # Retrieve models with a limit of 2
    models = lmstudio.get_models(limit=2)
    assert models
    assert len(models) == 2
    assert models[0].id == "lmstudio-chat-model"
    assert all(isinstance(model, AIModel) for model in models)
    assert all(model.provider == lmstudio.name for model in models)


def test_get_models_type_filter(requests_mock: Mocker) -> None:
    lmstudio = LMStudio()

    # Mock the response for the models endpoint
    requests_mock.get(
        url=lmstudio.base_url + lmstudio.MODELS_ENDPOINT,
        json={
            "data": [
                {
                    "id": "lmstudio-chat-model",
                },
                {
                    "id": "embedding-model-v1",
                },
                {
                    "id": "lmstudio-chat-model-v3",
                },
            ]
        },
    )

    # Retrieve models with a limit of 2
    models = lmstudio.get_models(type_filter=AIModelType.EMBEDDING)
    assert models
    assert len(models) == 1
    assert models[0].id == "embedding-model-v1"
    assert all(isinstance(model, AIModel) for model in models)
    assert all(model.provider == lmstudio.name for model in models)


def test_converse(requests_mock: Mocker) -> None:
    lmstudio = LMStudio()

    # Mock the response for the models endpoint
    requests_mock.get(
        url=lmstudio.base_url + lmstudio.MODELS_ENDPOINT,
        json={
            "data": [
                {
                    "id": "lmstudio-chat-model",
                }
            ]
        },
    )
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

    # Build structures for the test
    model: AIModel = lmstudio.get_models(limit=1, type_filter=AIModelType.CHAT)[0]
    message_thread: MessageThread = MessageThread(
        messages=[
            Message(
                content="Hello, how are you?",
            )
        ]
    )

    # Send a message to the AI model and receive a response
    response: Message = lmstudio.converse(model, message_thread)

    # Check that the response is not empty and has the expected role
    assert isinstance(response.content, str)
    assert response.content == "Hello! How can I assist you today?"
    assert response.role == MessageRole.ASSISTANT
    assert response.content_type == ContentType.TEXT


def test_converse_too_long(requests_mock: Mocker) -> None:
    lmstudio = LMStudio()

    # Mock the response for the models endpoint
    requests_mock.get(
        url=lmstudio.base_url + lmstudio.MODELS_ENDPOINT,
        json={
            "data": [
                {
                    "id": "lmstudio-chat-model",
                }
            ]
        },
    )
    requests_mock.post(
        url=lmstudio.base_url + lmstudio.CONVERSE_ENDPOINT,
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

    # Build structures for the test
    model: AIModel = lmstudio.get_models(limit=1, type_filter=AIModelType.CHAT)[0]
    message_thread: MessageThread = MessageThread(
        messages=[
            Message(
                content="Hello, how are you?",
            )
        ]
    )

    # Send a message to the AI model and receive a response
    response: Message = lmstudio.converse(model, message_thread)

    # Check that the response is not empty and has the expected role
    assert isinstance(response.content, str)
    assert (
        response.content
        == "Hello! How ca\n\n[[The response was truncated due to length limits.]]"
    )
    assert response.role == MessageRole.ASSISTANT
    assert response.content_type == ContentType.TEXT
