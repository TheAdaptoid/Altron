import json
from dataclasses import dataclass
from enum import Enum
from typing import TypeAlias

SERIALIZABLE: TypeAlias = int | float | str


class MessageRole(Enum):
    USER = "user"
    ASSISTANT = "assistant"
    SYSTEM = "system"


class ContentType(Enum):
    TEXT = "text"
    IMAGE = "image"
    AUDIO = "audio"
    TOOL_REQUEST = "tool_request"
    TOOL_RESPONSE = "tool_response"


@dataclass
class ToolRequest:
    name: str
    id: str
    args: dict[str, SERIALIZABLE]


@dataclass
class ToolResponse:
    name: str
    id: str
    content: str

    @property
    def content_object(self) -> SERIALIZABLE:
        return json.loads(self.content)


@dataclass
class Message:
    role: MessageRole
    content_type: ContentType
    content: str | ToolRequest | ToolResponse
