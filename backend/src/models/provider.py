from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import Any

from src.models import AIModel, AIModelType, Message, MessageThread


@dataclass
class ChatData:
    """Data class to hold chat response data."""

    content: str
    finish_reason: str

    @classmethod
    def from_response(cls, response: dict[str, Any]) -> "ChatData":
        """Create a ChatData instance from a response dictionary."""
        choices: list[dict[str, Any]] = response.get("choices", [])
        if not choices:
            raise ValueError("No choices found in the response.")
        chat_data: dict[str, Any] = choices[0]  # Get the first choice
        return ChatData(
            content=chat_data["message"]["content"],
            finish_reason=chat_data.get("finish_reason", "unknown"),
        )


class Provider(ABC):
    """Abstract base class for AI model inference providers."""

    MODELS_ENDPOINT: str = "/models"
    CONVERSE_ENDPOINT: str = "/chat/completions"

    def __init__(self, name: str, base_url: str) -> None:
        """Initialize the provider with a name and base URL."""
        self._name: str = name
        self._base_url: str = base_url

    @property
    def name(self) -> str:
        """Retrieve the name of the provider."""
        return self._name

    @property
    def base_url(self) -> str:
        """Retrieve the base URL of the provider."""
        return self._base_url

    @abstractmethod
    def get_models(
        self, limit: int | None = None, type_filter: AIModelType | None = None
    ) -> list[AIModel]:
        """Retrieve a list of available AI models from the provider.

        Args:
            limit (int): The maximum number of models to return.
            type_filter (AIModelType): The type of models to retrieve.

        Returns:
            list[AIModel]: A list of AIModel instances
                representing the available models.
        """
        raise NotImplementedError(
            "This method should be implemented by subclasses of Provider."
        )

    @abstractmethod
    def converse(self, model: AIModel, message_thread: MessageThread) -> Message:
        """Send a message to the AI model and receive a response.

        Args:
            model (AIModel): The AI model to use for the conversation.
            message_thread (MessageThread): The thread of messages to send.

        Returns:
            Message: The response message from the AI model.
        """
        raise NotImplementedError(
            "This method should be implemented by subclasses of Provider."
        )
