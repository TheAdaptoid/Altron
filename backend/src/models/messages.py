import json
from datetime import datetime
from enum import Enum

from pydantic import BaseModel, Field

type SERIALIZABLE = int | float | str


class MessageRole(str, Enum):
    """The role of the originator of a message."""

    USER = "user"
    ASSISTANT = "assistant"
    SYSTEM = "system"


class ContentType(str, Enum):
    """The type of content in a message."""

    TEXT = "text"
    IMAGE = "image"
    AUDIO = "audio"
    TOOL_REQUEST = "tool_request"
    TOOL_RESPONSE = "tool_response"


class ToolRequest(BaseModel):
    """A request to use a tool."""

    name: str = Field(
        ...,
        description="The name of the tool to be used.",
    )
    id: str = Field(
        ...,
        description="The unique identifier for the tool request.",
    )
    args: dict[str, SERIALIZABLE] = Field(
        ...,
        description="The arguments to pass to the tool, stored as a dictionary.",
    )


class ToolResponse(BaseModel):
    """A response from a tool."""

    name: str = Field(
        ...,
        description="The name of the tool that generated the response.",
    )
    id: str = Field(
        ...,
        description="The unique identifier for the tool response.",
    )
    content: str = Field(
        ...,
        description="The content of the tool response, stored as a JSON string.",
    )

    def load_content(self) -> SERIALIZABLE:
        """Load the content of the tool response.

        Converts the content JSON string to a valid Python object.

        Returns:
            SERIALIZABLE: The content as a Python object.
        """
        return json.loads(self.content)


class Message(BaseModel):
    """A message in a conversation."""

    role: MessageRole = Field(
        default=MessageRole.USER,
        description="The role of the message originator.",
    )
    timestamp: str = Field(
        default_factory=lambda: datetime.now().isoformat(),
        description="The timestamp of when the message was created.",
    )
    content_type: ContentType = Field(
        default=ContentType.TEXT,
        description="The type of content in the message.",
    )
    content: str | ToolRequest | ToolResponse = Field(
        ...,
        description="The content of the message, "
        "which can be text, a tool request, or a tool response.",
    )


class MessageThread(BaseModel):
    """A thread of messages in a conversation."""

    title: str = Field(
        default="New Thread",
        description="The title of the message thread.",
    )
    messages: list[Message] = Field(
        default_factory=list[Message],
        description="The messages in the thread.",
    )
    modified_at: str = Field(
        default_factory=lambda: datetime.now().isoformat(),
        description="The timestamp of when the thread was last modified.",
    )
