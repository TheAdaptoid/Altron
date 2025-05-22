
from src.common import http_request
from src.config import settings
from src.models.ai_models import AIModel


class ModelService:
    """Service to handle AI model-related operations."""

    @staticmethod
    async def get_available_models() -> list[AIModel]:
        """Retrieve a list of available AI models.

        Returns:
            List of available AI models.
        """
        # Placeholder for actual model retrieval logic
        raw_model_list: list[dict[str, str]] = http_request(
            method="GET",
            url=settings.INFERENCE_URL + "/models",
        ).json()["data"]

        return [
            AIModel(
                id=model["id"],
            )
            for model in raw_model_list
            if "embed" not in model["id"].lower()
        ]
