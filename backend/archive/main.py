import asyncio

from src.comm_tunnel import invoke_chat_model
from src.data_models import (
    Message,
    MessageRole,
    MessageThread,
    Model,
    ModelProvider,
    ModelType,
)


def get_user_input() -> Message | None:
    input_text: str = input("\nYou > ")

    if input_text == "exit":
        return None

    return Message(role=MessageRole.USER, content=input_text)


async def main() -> None:
    # Load messages
    message_thread: MessageThread = MessageThread(id=1, title="Main Thread")

    # Pick a model
    chat_model: Model = Model(
        model_name="llama-3.2-3b-instruct",
        model_alias="llama",
        type=ModelType.COMPLETION,
        provider=ModelProvider.LMSTUDIO,
        context_size=2048,
    )

    # Main loop
    while True:
        if (user_message := get_user_input()) is None:
            break
        message_thread.add_message(user_message)

        assistant_message: Message = await invoke_chat_model(message_thread, chat_model)
        message_thread.add_message(assistant_message)


if __name__ == "__main__":
    asyncio.run(main())
