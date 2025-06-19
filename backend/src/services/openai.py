from os import getenv

from dotenv import load_dotenv
from requests import Response

from src.models import AIModel, AIModelType, Provider
from src.utils import http_request

ALLOWED_MODELS: tuple[str, ...] = ("gpt-4o-mini", "gpt-4o", "gpt-4")


class OpenAI(Provider):
    """Provider implementation for OpenAI."""

    MODELS_ENDPOINT: str = "/models"

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
            headers={
                "Authorization": f"Bearer {self.api_key}",
                "Content-Type": "application/json",
            },
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
