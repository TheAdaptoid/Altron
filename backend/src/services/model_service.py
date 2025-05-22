from requests.exceptions import HTTPError

from src.config import settings
from src.models.ai_models import AIModel
from src.utils.logger import setup_logger
from src.utils.requests import http_request

logger = setup_logger(__name__)


class ModelService:
    """Service to handle AI model-related operations."""

    @staticmethod
    async def get_available_models() -> list[AIModel]:
        """Retrieve a list of available AI models.

        Returns:
            List of available AI models.
        """
        # Retrieve the list of models from the inference server
        # and filter out the ones that contain "embed" in their ID
        try:
            logger.info("Fetching available models from inference server")

            model_list: list[dict[str, str]] = http_request(
                method="GET",
                url=settings.INFERENCE_URL + "/models",
            ).json()["data"]

        # Raise an exception if the request fails
        except HTTPError as e:
            logger.error(
                msg="Failed to retrieve models from inference server",
                exc_info=True,
                extra={"error": str(e)},
            )
            raise

        return [
            AIModel(
                id=model["id"],
            )
            for model in model_list
            if "embed" not in model["id"].lower()
        ]
