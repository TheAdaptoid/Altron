from abc import ABC, abstractmethod

from src.models import AgentMessage, AIModel, AIModelType, MessageThread


class Provider(ABC):
    """Abstract base class for AI model inference providers."""

    def __init__(self, name: str) -> None:
        """Initialize the provider with a name and base URL."""
        self._name: str = name

    @property
    def name(self) -> str:
        """Retrieve the name of the provider."""
        return self._name

    @property
    def connected(self) -> bool:
        """Status of the connection to the provider."""
        models: list[AIModel] = self.get_models(limit=1)
        return len(models) > 0

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

    @abstractmethod
    def get_model(self, model_id: str) -> AIModel:
        """Retrieve an AIModel instance by its unique identifier.

        Args:
            model_id (str): The unique identifier of the AI model to retrieve.

        Returns:
            AIModel: The AI model instance corresponding to the provided model_id.
        """
        raise NotImplementedError(
            "This method should be implemented by subclasses of Provider."
        )

    @abstractmethod
    def converse(self, model: AIModel, message_thread: MessageThread) -> AgentMessage:
        """Send a message to the AI model and receive a response.

        Args:
            model (AIModel): The AI model to use for the conversation.
            message_thread (MessageThread): The thread of messages to send.

        Returns:
            Message: The response message from the AI model.
        """
        raise NotImplementedError(
            "This method should be implemented by subclasses of Provider."
        )
