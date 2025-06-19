import json
from dataclasses import dataclass
from enum import Enum

type SERIALIZABLE = int | float | str


class MessageRole(Enum):
    """The role of the originator of a message."""

    USER = "user"
    ASSISTANT = "assistant"
    SYSTEM = "system"


class ContentType(Enum):
    """The type of content in a message."""

    TEXT = "text"
    IMAGE = "image"
    AUDIO = "audio"
    TOOL_REQUEST = "tool_request"
    TOOL_RESPONSE = "tool_response"


@dataclass
class ToolRequest:
    """A request to use a tool."""

    name: str
    id: str
    args: dict[str, SERIALIZABLE]


@dataclass
class ToolResponse:
    """A response from a tool."""

    name: str
    id: str
    content: str

    def load_content(self) -> SERIALIZABLE:
        """Load the content of the tool response.

        Converts the content string to a valid Python object.

        Returns:
            SERIALIZABLE: The content as a Python object.
        """
        return json.loads(self.content)


@dataclass
class Message:
    """A message in a conversation."""

    role: MessageRole
    content_type: ContentType
    content: str | ToolRequest | ToolResponse
