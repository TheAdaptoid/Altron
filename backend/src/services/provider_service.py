from src.models import AIModel, AIModelType, Provider

# Inference providers
from src.providers import LMStudio, OpenAI
from src.utils import setup_logger

logger = setup_logger(__name__)


def __retrieve_providers() -> dict[str, Provider]:
    """Retrieve a dictionary of available AI model providers."""
    openai_p: Provider = OpenAI()
    lmstudio_p: Provider = LMStudio()

    return {
        openai_p.name: openai_p,
        lmstudio_p.name: lmstudio_p,
    }


def get_provider(provider_name: str) -> Provider:
    """Retrieve a specific AI model provider by name.

    Args:
        provider_name (str): The name of the provider to retrieve.

    Returns:
        Provider: The provider instance.

    Raises:
        ValueError: If the provider is not found.
    """
    providers: dict[str, Provider] = __retrieve_providers()
    if provider_name not in providers:
        raise ValueError(f"Provider '{provider_name}' not found.")
    return providers[provider_name]


def get_available_providers() -> tuple[str, ...]:
    """Retrieve a list of known AI model providers.

    Returns:
        tuple[str, ...]: List of provider names.
    """
    providers: dict[str, Provider] = __retrieve_providers()
    return tuple(providers.keys())


def get_available_models(
    limit: int | None = None, type_filter: AIModelType | None = None
) -> list[AIModel]:
    """Retrieve a list of available AI models.

    Args:
        limit (int | None): Optional limit on the number of models to return.
            If None, all available models will be returned.
        type_filter (AIModelType | None):
            Optional filter for the type of models to return.

    Returns:
        list[AIModel]: List of available AI models.

    Raises:
        Exception: If there is an error retrieving models from any provider.
    """
    # Get provider names from get_available_providers
    provider_names = get_available_providers()
    model_list: list[AIModel] = []
    for name in provider_names:
        # Retrieve provider instance
        providers: dict[str, Provider] = __retrieve_providers()
        provider = providers.get(name)
        if provider is None:
            continue
        try:
            logger.info(f"Retrieving models from provider: {name}")
            models: list[AIModel] = provider.get_models(type_filter=type_filter)
        except Exception as e:
            logger.error(
                f"Error retrieving models from provider {name}: {e}",
                exc_info=True,
                extra={"error": str(e)},
            )
            continue  # Skip this provider if an error occurs

        logger.info(f"Retrieved {len(models)} models from provider: {name}")
        model_list.extend(models)

    # limit the number of models if a limit is specified
    if limit:
        model_list = model_list[:limit]

    return model_list


def get_provider_models(
    provider_name: str, limit: int | None = None, type_filter: AIModelType | None = None
) -> list[AIModel]:
    """Retrieve models from a specific provider.

    Args:
        provider_name (str): The name of the provider.
        limit (int | None): Optional limit on the number of models to return.
            If None, all available models will be returned.
        type_filter (AIModelType | None):
            Optional filter for the type of models to return.

    Returns:
        list[AIModel]: List of AI models from the specified provider.

    Raises:
        ValueError: If the provider is not found.
        Exception: If there is an error retrieving models from the provider.
    """
    # Validate provider name
    providers: dict[str, Provider] = __retrieve_providers()
    if provider_name not in providers:
        raise ValueError(f"Provider '{provider_name}' not found.")

    # Get the provider instance
    provider: Provider = providers[provider_name]

    try:
        logger.info(f"Retrieving models from provider: {provider_name}")
        models: list[AIModel] = provider.get_models(
            limit=limit, type_filter=type_filter
        )
    except Exception as e:
        logger.error(
            f"Error retrieving models from provider {provider_name}: {e}",
            exc_info=True,
            extra={"error": str(e)},
        )
        raise

    return models
