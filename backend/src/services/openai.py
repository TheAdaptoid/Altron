from os import getenv
from typing import Any

from dotenv import load_dotenv
from requests import Response

from src.models import (
    AIModel,
    AIModelType,
    ChatData,
    ContentType,
    Message,
    MessageThread,
    Provider,
)
from src.models.messages import MessageRole
from src.utils import http_request

ALLOWED_MODELS: tuple[str, ...] = ("gpt-4o-mini", "gpt-4o", "gpt-4")


class OpenAI(Provider):
    """Provider implementation for OpenAI."""

    def __init__(self) -> None:
        """Initialize a provider instance for OpenAI."""
        self.api_key: str = self.__load_key_from_env()
        super().__init__(base_url="https://api.openai.com/v1", name="OpenAI")

    def __load_key_from_env(self) -> str:
        """Load the OpenAI API key from environment variables.

        Returns:
            str: The OpenAI API key.

        Raises:
            ValueError: If the API key is not found in the environment variables.
        """
        load_dotenv()
        api_key: str | None = getenv("OPENAI_API_KEY")
        if not api_key:
            raise ValueError(
                "No API key found. "
                "Please set the `OPENAI_API_KEY` environment variable."
            )
        return api_key

    def __headers(self) -> dict[str, str]:
        """Generate the headers for the OpenAI API request.

        Returns:
            dict[str, str]: Headers including the authorization token.
        """
        return {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json",
        }

    def get_models(
        self, limit: int | None = None, type_filter: AIModelType | None = None
    ) -> list[AIModel]:
        """Retrieve a list of available AI models from OpenAI.

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
            url=self._base_url + self.MODELS_ENDPOINT,
            headers=self.__headers(),
        )

        # Parse the response
        model_list: list[dict[str, str]] = response.json()["data"]
        return_list: list[AIModel] = []

        for model in model_list:
            # Skip models that are not in the allowed list
            if model["id"] not in ALLOWED_MODELS:
                continue

            # Determine the model type based on the model ID
            model_type: AIModelType = (
                AIModelType.CHAT if "gpt" in model["id"] else AIModelType.UNDEFINED
            )
            if type_filter and model_type != type_filter:
                continue

            return_list.append(
                AIModel(id=model["id"], provider=self._name, type=model_type)
            )

        # Return the models, limited by the specified limit if provided
        return return_list[:limit] if limit is not None else return_list

    def converse(self, model: AIModel, message_thread: MessageThread) -> Message:
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
                {
                    "role": msg.role.value if not MessageRole.SYSTEM else "developer",
                    "content": msg.content,
                }
                for msg in message_thread.messages
                if msg.content_type == ContentType.TEXT and isinstance(msg.content, str)
            ],
        }

        # Make the request
        response: Response = http_request(
            method="POST",
            url=self._base_url + self.CONVERSE_ENDPOINT,
            json=payload,
            headers=self.__headers(),
        )

        # Parse the response
        response_data: dict[str, Any] = response.json()
        chat_data: ChatData = ChatData.from_response(response_data)

        # Determine the next step based on the finish reason
        match chat_data.finish_reason:
            case "stop":
                return Message(
                    role=MessageRole.ASSISTANT,
                    content_type=ContentType.TEXT,
                    content=chat_data.content,
                )
            case "length":
                return Message(
                    role=MessageRole.ASSISTANT,
                    content=chat_data.content
                    + "\n\n[[The response was truncated due to length limits.]]",
                    content_type=ContentType.TEXT,
                )
            case _:
                raise ValueError(
                    f"Unexpected finish reason: {chat_data.finish_reason}. "
                    "Please check the model and the request."
                )
