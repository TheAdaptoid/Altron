from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from enum import Enum


@dataclass(slots=True)
class Serializable(ABC):
    @abstractmethod
    def serialize(self) -> dict:
        pass


class ModelType(Enum):
    """Enum for model types
    """

    EMBEDDING = 0
    COMPLETION = 1


class ModelProvider(Enum):
    """Enum for model providers
    """

    LMSTUDIO = 0
    OPENAI = 1
    OLLAMA = 2


class MessageRole(Enum):
    """Enum for message roles
    """

    USER = "user"
    ASSISTANT = "assistant"


@dataclass(slots=True)
class Model(Serializable):
    model_name: str
    model_alias: str
    type: ModelType
    provider: ModelProvider
    context_size: int

    def serialize(self) -> dict[str, str | int]:
        return {
            "model_name": self.model_name,
            "model_alias": self.model_alias,
            "type": self.type.value,
            "provider": self.provider.value,
            "context_size": self.context_size,
        }


@dataclass(slots=True)
class Message(Serializable):
    role: MessageRole
    content: str

    def serialize(self) -> dict[str, str]:
        return {
            "role": self.role.value,
            "content": self.content,
        }


@dataclass(slots=True)
class MessageThread(Serializable):
    id: int
    title: str = "Message Thread"
    messages: list[Message] = field(default_factory=list)

    @property
    def message_list(self) -> list[dict[str, str]]:
        return [message.serialize() for message in self.messages]

    def add_message(self, message: Message) -> None:
        self.messages.append(message)

    def serialize(self) -> dict[str, int | str | list[dict[str, str]]]:
        return {
            "id": self.id,
            "title": self.title,
            "messages": self.message_list,
        }


@dataclass(slots=True)
class CompletionDelta:
    role: str | None
    content: str | None

    @classmethod
    def from_dict(cls, data: dict[str, str]) -> "CompletionDelta":
        return cls(role=data.get("role"), content=data.get("content"))


@dataclass(slots=True)
class CompletionChunk:
    created: int
    delta: CompletionDelta
    is_finish_token: bool

    @classmethod
    def from_lmstudio_dict(
        cls, data: dict[str, int | str | list[dict[str, int | str | dict[str, str]]]]
    ) -> "CompletionChunk":
        created = data.get("created", 0)
        if not isinstance(created, int):
            raise TypeError("creation timestamp must be int")

        choices = data.get("choices")
        if not isinstance(choices, list):
            raise TypeError("choices must be list")

        delta = choices[0].get("delta")
        if not isinstance(delta, dict):
            raise TypeError("delta must be dict")

        return cls(
            created=created,
            delta=CompletionDelta.from_dict(data=delta),
            is_finish_token=choices[0].get("finish_reason") is not None,
        )
