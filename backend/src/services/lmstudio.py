from os import getenv

from dotenv import load_dotenv
from requests import Response

from src.models import AIModel, AIModelType, Provider
from src.utils import http_request


class LMStudio(Provider):
    """Provider implementation for LM Studio."""

    MODELS_ENDPOINT: str = "/models"

    def __init__(self):
        """Initialize a provider instance for LM Studio."""
        super().__init__(base_url=self.__load_url_from_env(), name="LM Studio")

    def __load_url_from_env(self) -> str:
        """Load the base url key from environment variables.

        Returns:
            str: The base URL for the LM Studio API.

        Raises:
            ValueError: If the base URL is not found in the environment variables.
        """
        load_dotenv()
        url: str | None = getenv("LMSTUDIO_BASE_URL")
        if not url:
            raise ValueError(
                "No URL found. Please set the `LMSTUDIO_BASE_URL` environment variable."
            )
        return url

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
            url=self._base_url + self.MODELS_ENDPOINT,
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
