import asyncio
from collections.abc import AsyncGenerator

from src.data_models import (
    CompletionChunk,
    Message,
    MessageRole,
    MessageThread,
    Model,
    ModelProvider,
    ModelType,
)
from src.providers import LMStudio, Provider

# TODO: Make delta delay configurable
TOKEN_DELTA_DELAY: float = 0.05
BASE_URL_LMSTUDIO: str = "http://192.168.1.143:1234"


async def print_stream(stream: AsyncGenerator[CompletionChunk, None]) -> str:
    # Prepare to print
    print("\nAssistant > ", end="", flush=True)

    # Print the stream
    complete_stream: str = ""
    async for chunk in stream:
        if chunk.delta.content is None:
            continue

        if chunk.is_finish_token:
            break

        # Append the delta to the complete stream
        complete_stream += chunk.delta.content

        # Print the delta
        print(chunk.delta.content, end="", flush=True)
        await asyncio.sleep(TOKEN_DELTA_DELAY)

    # Return the complete stream
    print()
    return complete_stream


def invoke_embedding_model() -> None:
    pass


def select_inference_provider(provider_key: ModelProvider) -> Provider:
    provider: Provider
    match provider_key:
        case ModelProvider.LMSTUDIO:
            # TODO: Fetch the url from a user defined json file
            provider = LMStudio(base_url=BASE_URL_LMSTUDIO)
        case _:
            raise ValueError("Unknown model provider")

    return provider


async def invoke_chat_model(message_thread: MessageThread, model: Model) -> Message:
    # Verify the model is a chat model
    if model.type != ModelType.COMPLETION:
        raise ValueError("Model is not a chat model")

    # Pick a model provider
    provider: Provider = select_inference_provider(model.provider)

    # invoke the model
    token_stream: AsyncGenerator[CompletionChunk, None] = provider.request_completion(
        model=model, message_thread=message_thread
    )

    # return the response
    return Message(
        role=MessageRole.ASSISTANT,
        content=await print_stream(token_stream),
    )
