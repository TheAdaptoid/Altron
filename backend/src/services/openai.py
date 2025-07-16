from os import getenv
from typing import Any


from src.models import (
    AIModel,
    AIModelType,
    ChatData,
    Message,
    MessageThread,
    Provider,
    MessageRole,
)

ALLOWED_MODELS: tuple[str, ...] = ("gpt-4o-mini", "gpt-4o", "gpt-4")


class OpenAI(Provider):
    """Provider implementation for OpenAI."""

    ...
