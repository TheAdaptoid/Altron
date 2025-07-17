import json
from typing import Any

from openai import OpenAI as OpenAIClient
from openai.types.chat.chat_completion import ChatCompletion, Choice
from openai.types.model import Model as OpenAIModel

from src.models import (
    AgentMessage,
    AIModel,
    AIModelType,
    MessageRole,
    MessageThread,
    Provider,
    ToolRequest,
    ToolResponse,
    UserMessage,
)
from src.utils import load_env_var

ALLOWED_MODELS: tuple[str, ...] = ("gpt-4o-mini", "gpt-4o", "gpt-4")


class OpenAI(Provider):
    """Provider implementation for OpenAI."""

    def __init__(self) -> None:
        """Initialize a provider instance for OpenAI."""
        self._client: OpenAIClient = OpenAIClient(
            api_key=load_env_var("OPENAI_API_KEY")
        )
        super().__init__(name="OpenAI")

    def _convert_to_ai_model(self, model: OpenAIModel) -> AIModel:
        """Convert an OpenAI model to an AIModel instance.

        Args:
            model (OpenAIModel): The OpenAI model to convert.

        Returns:
            AIModel: The converted AIModel instance.
        """
        model_type: str = AIModelType.UNDEFINED
        if "gpt" in model.id:
            model_type = AIModelType.CHAT
        elif "embed" in model.id:
            model_type = AIModelType.EMBEDDING

        return AIModel(
            id=model.id,
            alias=model.id,
            type=model_type,
            provider=self.name,
        )

    def get_models(
        self, limit: int | None = None, type_filter: str | None = None
    ) -> list[AIModel]:
        """Retrieve a list of available AI models from OpenAI.

        Args:
            limit (int | None): The maximum number of models to return.
            type_filter (str | None): The type of models to retrieve.

        Returns:
            list[str]: A list of model names.
        """
        # Retrieve models from OpenAI
        openai_models = self._client.models.list()

        # Convert to AIModel instances
        generalized_models: list[AIModel] = [
            self._convert_to_ai_model(model) for model in openai_models
        ]

        # Filter models based on type
        if type_filter:
            generalized_models = [
                model for model in generalized_models if model.type == type_filter
            ]

        # Limit the number of models returned
        if limit is not None:
            generalized_models = generalized_models[:limit]

        return generalized_models

    def get_model(self, model_id: str) -> AIModel:
        """Retrieves an AI model by its identifier from the OpenAI client.

        Args:
            model_id (str): The unique identifier of the model to retrieve.

        Returns:
            AIModel: An instance of AIModel representing the retrieved model.
        """
        openai_model = self._client.models.retrieve(model_id)

        return self._convert_to_ai_model(openai_model)

    def _create_tool_message_dict(self, tool_response: ToolResponse) -> dict[str, Any]:
        return {
            "role": "tool",
            "content": tool_response.content,
            "tool_call_id": tool_response.id,
        }

    def _create_user_message_dict(self, message: UserMessage) -> dict[str, Any]:
        # If the message has a tool response, create a tool message dict
        if message.tool_response:
            return self._create_tool_message_dict(message.tool_response)

        # Otherwise, create a standard user message dict
        if message.content is None:
            raise ValueError("User message content cannot be `None`.")
        return {"role": MessageRole.USER.value, "content": message.content}

    def _create_agent_message_dict(self, message: AgentMessage) -> dict[str, Any]:
        return {
            "role": MessageRole.AGENT.value,
            "content": message.content,
            "tool_calls": [
                {
                    "id": tool_request.id,
                    "type": "function",
                    "function": {
                        "name": tool_request.name,
                        "arguments": tool_request.arguments,
                    },
                }
                for tool_request in message.tool_requests
            ],
        }

    def _convert_to_message_list(
        self, message_thread: MessageThread
    ) -> list[dict[str, Any]]:
        """Convert a MessageThread to a list of dictionaries for OpenAI API.

        Args:
            message_thread (MessageThread): The thread of messages to convert.

        Returns:
            list[dict]: A list of dictionaries representing the messages.
        """
        message_list: list[dict[str, Any]] = []

        for message in message_thread.messages:
            if isinstance(message, UserMessage):
                message_list.append(self._create_user_message_dict(message))
            elif isinstance(message, AgentMessage):
                message_list.append(self._create_agent_message_dict(message))
            else:
                raise ValueError(f"Unsupported message type: {type(message)}")

        return message_list

    def converse(self, model: AIModel, message_thread: MessageThread) -> AgentMessage:
        """Sends a messages to the specified AI model and returns the agent's response.

        Args:
            model (AIModel): The AI model to interact with.
            message_thread (MessageThread):
                The sequence of messages to send to the model.

        Returns:
            AgentMessage: The agent's response, including content and any tool requests.

        Raises:
            Any exceptions raised by the underlying client or JSON parsing.
        """
        # Send a message to the AI model and receive a response.
        completion: ChatCompletion = self._client.chat.completions.create(
            model=model.id,
            messages=self._convert_to_message_list(message_thread),
        )
        response: Choice = completion.choices[0]

        # Check for tool calls in the response
        tool_requests: list[ToolRequest] = []
        if response.message.tool_calls:
            tool_requests: list[ToolRequest] = [
                ToolRequest(
                    id=tool_call.id,
                    name=tool_call.function.name,
                    arguments=json.loads(tool_call.function.arguments),
                )
                for tool_call in response.message.tool_calls
            ]

        # Create and return an AgentMessage with the response content and tool requests
        return AgentMessage(
            role=MessageRole.AGENT,
            content=response.message.content,
            tool_requests=tool_requests,
        )
