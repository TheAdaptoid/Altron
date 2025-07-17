from dataclasses import dataclass
from typing import Any

from requests import Response

from src.models import (
    AgentMessage,
    AIModel,
    AIModelType,
    MessageThread,
    Provider,
)
from src.utils import http_request, load_env_var


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


class LMStudio(Provider):
    """Provider implementation for LM Studio."""

    MODELS_ENDPOINT: str = "/v1/models"
    CONVERSE_ENDPOINT: str = "/v1/chat/completions"

    def __init__(self):
        """Initialize a provider instance for LM Studio."""
        self._base_url: str = load_env_var("LMSTUDIO_BASE_URL")
        super().__init__(name="LM Studio")

    @property
    def base_url(self) -> str:
        """Retrieve the base URL of the LM Studio instance."""
        return self._base_url

    def _resolve_url(self, endpoint: str) -> str:
        """Resolve the full URL for a given endpoint.

        Args:
            endpoint (str): The endpoint to resolve.

        Returns:
            str: The full URL for the endpoint.
        """
        return f"http://{self._base_url}{endpoint}"

    def get_models(
        self, limit: int | None = None, type_filter: AIModelType | None = None
    ) -> list[AIModel]:
        """Retrieve a list of available AI models from LM Studio.

        Args:
            limit (int | None): Optional limit on the number of models to return.
                If None, all available models will be returned.
            type_filter (AIModelType | None):
                Optional filter for the type of models to return.

        Returns:
            List of AIModel instances representing the available models.
        """
        # Make the request
        response: Response = http_request(
            method="GET",
            url=self._resolve_url(self.MODELS_ENDPOINT),
        )

        # Parse the response
        try:
            model_list: list[dict[str, str]] = response.json()["data"]
        except KeyError as e:
            raise ValueError(
                "Invalid response format from LM Studio. Expected 'data' key."
            ) from e

        return_list: list[AIModel] = []
        for model in model_list:
            # determine the model type based on the model ID
            model_type: AIModelType = (
                AIModelType.EMBEDDING if "embed" in model["id"] else AIModelType.CHAT
            )
            if type_filter and model_type != type_filter:
                continue

            return_list.append(
                AIModel(id=model["id"], provider=self._name, type=model_type)
            )

        # Return the models, limited by the specified limit if provided
        return return_list[:limit] if limit is not None else return_list

    def get_model(self, model_id: str) -> AIModel:
        """Retrieve an AIModel instance by its unique identifier.

        Args:
            model_id (str): The unique identifier of the AI model to retrieve.

        Returns:
            AIModel: The AI model instance corresponding to the provided model_id.
        """
        models = self.get_models()
        for model in models:
            if model.id == model_id:
                return model
        raise ValueError(f"Model with ID '{model_id}' not found.")

    def converse(self, model: AIModel, message_thread: MessageThread) -> AgentMessage:
        """Send a message to the AI model and receive a response.

        Args:
            model (AIModel): The AI model to use for the conversation.
            message_thread (list[str]): The thread of messages to send.

        Returns:
            str: The response message from the AI model.
        """
        # Raise ValueError if message thread is empty
        if not message_thread.messages:
            raise ValueError("Message thread is empty.")

        # Prepare the request payload
        payload: dict[str, str | list[dict[str, str]] | bool] = {
            "model": model.id,
            "messages": [
                {"role": msg.role.value, "content": msg.content}
                for msg in message_thread.messages
                if isinstance(msg.content, str)  # Ensure content is not "empty"
            ],
            "stream": False,
        }

        # Make the request
        response: Response = http_request(
            method="POST",
            url=self._resolve_url(self.CONVERSE_ENDPOINT),
            json=payload,
        )

        # Parse the response
        response_data: dict[str, Any] = response.json()
        chat_data: ChatData = ChatData.from_response(response_data)

        # Determine the next step based on the finish reason
        match chat_data.finish_reason:
            case "stop":
                return AgentMessage(
                    content=chat_data.content,
                )
            case "length":
                return AgentMessage(
                    content=chat_data.content
                    + "\n\n[[The response was truncated due to length limits.]]",
                )
            case _:
                raise ValueError(
                    f"Unexpected finish reason: {chat_data.finish_reason}. "
                    "Please check the model and the request."
                )
