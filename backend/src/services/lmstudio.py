from typing import Any

from requests import Response

from src.models import (
    AIModel,
    AIModelType,
    ChatData,
    Provider,
    AgentMessage,
    MessageThread,
)
from src.utils import http_request, load_env_var


class LMStudio(Provider):
    """Provider implementation for LM Studio."""

    MODELS_ENDPOINT: str = "/v1/models"
    CONVERSE_ENDPOINT: str = "/v1/chat/completions"

    def __init__(self):
        """Initialize a provider instance for LM Studio."""
        super().__init__(base_url=load_env_var("LMSTUDIO_BASE_URL"), name="LM Studio")

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
        model_list: list[dict[str, str]] = response.json()["data"]
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

    def converse(self, model: AIModel, message_thread: MessageThread) -> AgentMessage:
        """Send a message to the AI model and receive a response.

        Args:
            model (AIModel): The AI model to use for the conversation.
            message_thread (list[str]): The thread of messages to send.

        Returns:
            str: The response message from the AI model.
        """
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
