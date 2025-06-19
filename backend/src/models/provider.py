from abc import ABC, abstractmethod

from src.models.ai_models import AIModel, AIModelType


class Provider(ABC):
    """Abstract base class for AI model inference providers."""

    def __init__(self, name: str, base_url: str) -> None:
        """Initialize the provider with a name and base URL."""
        self._name: str = name
        self._base_url: str = base_url

    @property
    def name(self) -> str:
        """Retrieve the name of the provider."""
        return self._name

    @abstractmethod
    def get_models(
        self, limit: int | None = None, type_filter: AIModelType | None = None
    ) -> list[AIModel]:
        """Retrieve a list of available AI models from the provider.

        Args:
            limit (int): The maximum number of models to return.
            type_filter (AIModelType): The type of models to retrieve.

        Returns:
            list[AIModel]: A list of AIModel instances
                representing the available models.
        """
        raise NotImplementedError(
            "This method should be implemented by subclasses of Provider."
        )
