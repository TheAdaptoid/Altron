import time
from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from enum import Enum
from typing import Any


@dataclass(slots=True)
class Serializable(ABC):
    """Abstract base class for serializable objects."""

    @abstractmethod
    def serialize(self) -> dict[str, Any]:
        """Serialize the object to a dictionary.

        Returns:
            dict: A dictionary representation of the object.
        """


class ModelType(Enum):
    """Enum for model types."""

    EMBEDDING = 0
    COMPLETION = 1


class ModelProvider(Enum):
    """Enum for model providers."""

    LMSTUDIO = 0
    OPENAI = 1
    OLLAMA = 2


class MessageRole(Enum):
    """Enum for message roles."""

    USER = "user"
    ASSISTANT = "assistant"


@dataclass(slots=True)
class Model(Serializable):
    """Dataclass for models.

    Attributes:
        model_name (str): The name of the model.
        model_alias (str): The alias of the model.
        type (ModelType): The type of the model.
        provider (ModelProvider): The provider of the model.
        context_size (int): The size of the context window.
    """

    model_name: str
    model_alias: str
    type: ModelType
    provider: ModelProvider
    context_size: int

    def serialize(self) -> dict[str, str | int]:
        """Serialize the model to a dictionary.

        Returns:
            dict[str, str | int]: A dictionary representation of the model.
        """
        return {
            "model_name": self.model_name,
            "model_alias": self.model_alias,
            "type": self.type.value,
            "provider": self.provider.value,
            "context_size": self.context_size,
        }


@dataclass(slots=True)
class Message(Serializable):
    """Dataclass for messages.

    Attributes:
        role (MessageRole): The role of the message.
        content (str): The content of the message.
    """

    role: MessageRole
    content: str
    timestamp: float = field(default_factory=time.time)

    def serialize(self) -> dict[str, str | float]:
        """Serialize the message to a dictionary.

        Returns:
            dict[str, str | float]: A dictionary representation of the message.
        """
        return {
            "role": self.role.value,
            "content": self.content,
            "timestamp": self.timestamp,
        }

    def model_serialize(self) -> dict[str, str]:
        """Serialize the message to a dictionary formatted for LLMs.

        Returns:
            dict[str, str]: A dictionary representation of the message.
                Contains only the role and content.
        """
        return {
            "role": self.role.value,
            "content": self.content,
        }


@dataclass(slots=True)
class MessageThread(Serializable):
    """Dataclass for message threads.

    Attributes:
        id (int): The id of the thread.
        title (str): The title of the thread.
        messages (list[Message]): The messages in the thread.
    """

    id: int
    title: str = "Message Thread"
    messages: list[Message] = field(default_factory=list[Message])

    @property
    def message_list(self) -> list[dict[str, str]]:
        """Convert the messages to a list of dictionaries formatted for LLMs.

        Returns:
            list[dict[str, str]]: A list of dictionaries representing the messages.
        """
        return [message.model_serialize() for message in self.messages]

    def add_message(self, message: Message) -> None:
        """Add a message to the thread.

        Args:
            message (Message): The message to add.
        """
        self.messages.append(message)

    def serialize(self) -> dict[str, int | str | list[dict[str, str | float]]]:
        """Serialize the thread to a dictionary.

        Returns:
            dict[str, int | str | list[dict[str, str | float]]]:
                A dictionary representation of the thread.
        """
        return {
            "id": self.id,
            "title": self.title,
            "messages": [message.serialize() for message in self.messages],
        }


@dataclass(frozen=True, slots=True)
class CompletionChunk:
    """Dataclass for completion chunks.

    Attributes:
        created (int): The creation timestamp of the chunk.
        delta (str | None): The delta of the chunk.
        is_finish_token (bool): Whether the chunk is a finish token.
    """

    created: int
    delta: str | None
    is_finish_token: bool

    @classmethod
    def from_lmstudio_dict(
        cls, data: dict[str, int | str | list[dict[str, int | str | dict[str, str]]]]
    ) -> "CompletionChunk":
        """Create a CompletionChunk from a dictionary provided by an LMStudio stream.

        Args:
            data (dict[str, int | str | list[dict[str, int | str | dict[str, str]]]]):
                The dictionary to create the CompletionChunk from.

        Returns:
            CompletionChunk: The created CompletionChunk.
        """
        # Extract the creation timestamp
        created = data.get("created", 0)
        if not isinstance(created, int):
            raise TypeError("creation timestamp must be int")

        # Extract the delta
        choices = data.get("choices")
        if not isinstance(choices, list):
            raise TypeError("choices must be list")
        delta_data = choices[0].get("delta")
        if not isinstance(delta_data, dict):
            raise TypeError("delta must be dict")
        delta_token: str | None = delta_data.get("content")

        # Determine if the chunk is a finish token
        finish_token: bool = False
        if delta_token is None:
            finish_token = True

        return cls(
            created=created,
            delta=delta_token,
            is_finish_token=finish_token,
        )
