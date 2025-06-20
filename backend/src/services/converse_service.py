from src.models import Message, MessageThread, Provider
from src.models.ai_models import AIModel, AIModelType
from src.services.provider_service import get_provider


def __retrieve_provider(model: AIModel) -> Provider:
    """Retrieve the provider name for a given AI model.

    Args:
        model (AIModel): The AI model for which to retrieve the provider.

    Returns:
        Provider: The provider instance associated with the AI model.

    Raises:
        ValueError: If the provider for the model is not found.
    """
    provider_name: str = model.provider

    # Attempt to retrieve the provider instance
    try:
        provider: Provider = get_provider(provider_name)
    except ValueError as e:
        raise ValueError(
            f"Provider '{provider_name}' not found for model '{model.id}'."
        ) from e

    return provider


def converse(model: AIModel, message_thread: MessageThread) -> Message:
    """Send a message to the AI model and receive a response.

    Args:
        model (AIModel): The AI model to use for the conversation.
        message_thread (MessageThread): The thread of messages to send.

    Returns:
        Message: The response message from the AI model.

    Raises:
        ValueError: If the provider for the model is not found.
    """
    # validate the model
    if model.type is not AIModelType.CHAT:
        raise ValueError(f"Model '{model.id}' is not a chat model.")

    # retrieve the AI model provider
    provider: Provider = __retrieve_provider(model)

    # call the provider's converse method
    return provider.converse(model, message_thread)
