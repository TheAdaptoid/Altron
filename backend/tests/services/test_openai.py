from src.models.ai_models import AIModel, AIModelType
from src.models.messages import MessageThread, Message, MessageRole, ContentType
from src.services.openai import OpenAI
from requests_mock import Mocker


def test_get_models(requests_mock: Mocker) -> None:
    openai = OpenAI()

    # Mock the response for the models endpoint
    requests_mock.get(
        url=openai.base_url + openai.MODELS_ENDPOINT,
        json={
            "data": [
                {
                    "id": "gpt-3.5-turbo",
                },
                {
                    "id": "gpt-4o",
                },
                {
                    "id": "gpt-4o-mini",
                },
            ]
        },
    )

    # Retrieve models with a limit of 2
    models = openai.get_models(limit=2)
    assert models
    assert len(models) == 2
    assert all(isinstance(model, AIModel) for model in models)
    assert all(model.provider == openai.name for model in models)


def test_converse(requests_mock: Mocker) -> None:
    openai = OpenAI()

    # Mock the response for the models endpoint
    requests_mock.get(
        url=openai.base_url + openai.MODELS_ENDPOINT,
        json={
            "data": [
                {
                    "id": "gpt-4o",
                }
            ]
        },
    )
    requests_mock.post(
        url=openai.base_url + openai.CONVERSE_ENDPOINT,
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
    model: AIModel = openai.get_models(limit=1, type_filter=AIModelType.CHAT)[0]
    message_thread: MessageThread = MessageThread(
        messages=[
            Message(
                content="Hello, how are you?",
            )
        ]
    )

    # Send a message to the AI model and receive a response
    response: Message = openai.converse(model, message_thread)

    # Check that the response is not empty and has the expected role
    assert isinstance(response.content, str)
    assert response.content == "Hello! How can I assist you today?"
    assert response.role == MessageRole.ASSISTANT
    assert response.content_type == ContentType.TEXT
