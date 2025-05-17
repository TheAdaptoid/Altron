from src.data_models import (
    Message,
    MessageRole,
    MessageThread,
    Model,
    ModelProvider,
    ModelType,
)

LMSTUDIO_URL: str = "http://192.168.1.143:1234"

LMSTUDIO_MODEL: Model = Model(
    model_name="llama-3.2-3b-instruct",
    model_alias="llama",
    type=ModelType.COMPLETION,
    provider=ModelProvider.LMSTUDIO,
    context_size=2048,
)

TEST_MESSAGE_THREAD: MessageThread = MessageThread(
    id=1,
    title="Main Thread",
    messages=[
        Message(role=MessageRole.USER, content="Hello"),
    ],
)
