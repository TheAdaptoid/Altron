import pytest
from unittest.mock import patch, MagicMock
from src.providers import OpenAI
from src.models.ai_models import AIModelType


@patch("src.providers.openai.OpenAIClient")
def test_get_models_returns_models(mock_client_class):
    # Mock OpenAIModel objects
    mock_model1 = MagicMock()
    mock_model1.id = "gpt-4o"
    mock_model2 = MagicMock()
    mock_model2.id = "embed-ada"
    mock_model3 = MagicMock()
    mock_model3.id = "other-model"

    # Mock the client .models.list() method
    mock_client = MagicMock()
    mock_client.models.list.return_value = [mock_model1, mock_model2, mock_model3]
    mock_client_class.return_value = mock_client

    provider = OpenAI()
    models = provider.get_models()
    assert len(models) == 3
    assert models[0].id == "gpt-4o"
    assert models[0].type == AIModelType.CHAT
    assert models[1].id == "embed-ada"
    assert models[1].type == AIModelType.EMBEDDING
    assert models[2].id == "other-model"
    assert models[2].type == AIModelType.UNDEFINED


@patch("src.providers.openai.OpenAIClient")
def test_get_models_type_filter(mock_client_class):
    mock_model1 = MagicMock()
    mock_model1.id = "gpt-4o"
    mock_model2 = MagicMock()
    mock_model2.id = "embed-ada"
    mock_client = MagicMock()
    mock_client.models.list.return_value = [mock_model1, mock_model2]
    mock_client_class.return_value = mock_client

    provider = OpenAI()
    chat_models = provider.get_models(type_filter=AIModelType.CHAT)
    assert len(chat_models) == 1
    assert chat_models[0].id == "gpt-4o"
    assert chat_models[0].type == AIModelType.CHAT

    embedding_models = provider.get_models(type_filter=AIModelType.EMBEDDING)
    assert len(embedding_models) == 1
    assert embedding_models[0].id == "embed-ada"
    assert embedding_models[0].type == AIModelType.EMBEDDING


@patch("src.providers.openai.OpenAIClient")
def test_get_models_limit(mock_client_class):
    mock_model1 = MagicMock()
    mock_model1.id = "gpt-4o"
    mock_model2 = MagicMock()
    mock_model2.id = "embed-ada"
    mock_model3 = MagicMock()
    mock_model3.id = "other-model"
    mock_client = MagicMock()
    mock_client.models.list.return_value = [mock_model1, mock_model2, mock_model3]
    mock_client_class.return_value = mock_client

    provider = OpenAI()
    models = provider.get_models(limit=2)
    assert len(models) == 2
    assert models[0].id == "gpt-4o"
    assert models[1].id == "embed-ada"


@patch("src.providers.openai.OpenAIClient")
def test_get_model_returns_single_model(mock_client_class):
    mock_model = MagicMock()
    mock_model.id = "gpt-4o"
    mock_client = MagicMock()
    mock_client.models.retrieve.return_value = mock_model
    mock_client_class.return_value = mock_client

    provider = OpenAI()
    model = provider.get_model("gpt-4o")
    assert model.id == "gpt-4o"
    assert model.type == AIModelType.CHAT


# --- Private message dict function tests ---
from src.models import ToolResponse, UserMessage, AgentMessage, MessageRole, ToolRequest


def test_create_tool_message_dict():
    provider = OpenAI.__new__(OpenAI)  # Bypass __init__
    tool_response = ToolResponse(id="123", name="tool1", content="tool content")
    result = provider._create_tool_message_dict(tool_response)
    assert result == {
        "role": "tool",
        "content": "tool content",
        "tool_call_id": "123",
    }


def test_create_user_message_dict_tool_response():
    provider = OpenAI.__new__(OpenAI)
    tool_response = ToolResponse(id="123", name="tool1", content="tool content")
    user_msg = UserMessage(content="should not be used", tool_response=tool_response)
    result = provider._create_user_message_dict(user_msg)
    assert result["role"] == "tool"
    assert result["tool_call_id"] == "123"


def test_create_user_message_dict_content():
    provider = OpenAI.__new__(OpenAI)
    user_msg = UserMessage(content="hello", tool_response=None)
    result = provider._create_user_message_dict(user_msg)
    assert result == {"role": MessageRole.USER.value, "content": "hello"}


def test_create_user_message_dict_content_none_raises():
    provider = OpenAI.__new__(OpenAI)
    user_msg = UserMessage(content=None, tool_response=None)
    # Expect ValueError when content is None
    with pytest.raises(ValueError):
        provider._create_user_message_dict(user_msg)


def test_create_agent_message_dict():
    provider = OpenAI.__new__(OpenAI)
    tool_req1 = ToolRequest(id="id1", name="func1", arguments={})
    tool_req2 = ToolRequest(id="id2", name="func2", arguments={"x": 1})
    agent_msg = AgentMessage(
        content="agent reply", tool_requests=[tool_req1, tool_req2]
    )
    result = provider._create_agent_message_dict(agent_msg)
    assert result["role"] == MessageRole.AGENT.value
    assert result["content"] == "agent reply"
    assert isinstance(result["tool_calls"], list)
    assert result["tool_calls"][0]["id"] == "id1"
    assert result["tool_calls"][1]["function"]["name"] == "func2"


def test_converse_returns_agent_message(monkeypatch):
    # Setup provider and mock client
    provider = OpenAI.__new__(OpenAI)
    provider._client = MagicMock()

    # Prepare input model and message thread
    model = MagicMock()
    model.id = "gpt-4o"
    from src.models import (
        MessageThread,
        UserMessage,
        AgentMessage,
        ToolRequest,
        MessageRole,
    )

    message_thread = MessageThread(
        messages=[UserMessage(content="Hello", tool_response=None)]
    )

    # Prepare mock response for OpenAI client
    mock_tool_call = MagicMock()
    mock_tool_call.id = "tool-id"
    mock_tool_call.function.name = "tool-func"
    mock_tool_call.function.arguments = '{"x":1}'
    mock_response_message = MagicMock()
    mock_response_message.content = "response content"
    mock_response_message.tool_calls = [mock_tool_call]
    mock_choice = MagicMock()
    mock_choice.message = mock_response_message
    mock_completion = MagicMock()
    mock_completion.choices = [mock_choice]
    provider._client.chat.completions.create.return_value = mock_completion

    # Call converse
    result = provider.converse(model, message_thread)
    assert isinstance(result, AgentMessage)
    assert result.content == "response content"
    assert result.role == MessageRole.AGENT
    assert len(result.tool_requests) == 1
    assert result.tool_requests[0].id == "tool-id"
    assert result.tool_requests[0].name == "tool-func"
    assert result.tool_requests[0].arguments == {"x": 1}


def test_converse_no_tool_calls(monkeypatch):
    provider = OpenAI.__new__(OpenAI)
    provider._client = MagicMock()
    model = MagicMock()
    model.id = "gpt-4o"
    from src.models import MessageThread, UserMessage, AgentMessage, MessageRole

    message_thread = MessageThread(
        messages=[UserMessage(content="Hello", tool_response=None)]
    )

    mock_response_message = MagicMock()
    mock_response_message.content = "response content"
    mock_response_message.tool_calls = None
    mock_choice = MagicMock()
    mock_choice.message = mock_response_message
    mock_completion = MagicMock()
    mock_completion.choices = [mock_choice]
    provider._client.chat.completions.create.return_value = mock_completion

    result = provider.converse(model, message_thread)
    assert isinstance(result, AgentMessage)
    assert result.content == "response content"
    assert result.role == MessageRole.AGENT
    assert result.tool_requests == []
