from src.models.ai_models import AIModel, AIModelType
from src.models.messages import MessageThread, Message, MessageRole
from src.services.openai import OpenAI
from requests_mock import Mocker


def test_get_models(requests_mock: Mocker) -> None:
    openai = OpenAI()


def test_converse(requests_mock: Mocker) -> None:
    openai = OpenAI()
