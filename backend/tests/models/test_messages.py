import pytest
from src.models.messages import (
    MessageRole,
    ToolRequest,
    ToolResponse,
    Message,
    UserMessage,
    AgentMessage,
)
from datetime import datetime
import json


class NonSerializable:
    def __str__(self):
        return "non-serializable"


class TestMessageRole:
    # Test that the enum has the correct values
    def test_message_role_values(self):
        assert MessageRole.USER == "user"
        assert MessageRole.AGENT == "assistant"

    # Test that the enum can be instantiated from string values
    def test_message_role_from_string(self):
        assert MessageRole("user") == MessageRole.USER
        assert MessageRole("assistant") == MessageRole.AGENT

    # Test that invalid values raise ValueError
    def test_message_role_invalid_value(self):
        with pytest.raises(ValueError):
            MessageRole("invalid")


class TestToolRequest:
    def test_tool_request_fields(self):
        arguments = {"var_one": 2, "var_two": 1}
        req = ToolRequest(id="123", name="calculator", arguments=arguments)
        assert req.id == "123"
        assert req.name == "calculator"
        assert req.arguments == arguments

    def test_tool_request_serialization(self):
        arguments = {"var_one": 2, "var_two": 1}
        req = ToolRequest(id="123", name="calculator", arguments=arguments)
        serialized = req.model_dump_json()
        assert '"id":"123"' in serialized
        assert '"name":"calculator"' in serialized
        assert '"arguments":{"var_one":2,"var_two":1}' in serialized


class TestToolResponse:
    def test_tool_response_fields(self):
        resp = ToolResponse(
            id="456", name="calculator", content=json.dumps({"result": 3})
        )
        assert resp.id == "456"
        assert resp.name == "calculator"
        assert resp.content == json.dumps({"result": 3})

    def test_tool_response_to_json_string(self):
        data = {"result": 3}
        resp = ToolResponse(id="456", name="calculator", content=data)
        assert resp.to_json_string() == json.dumps(data)

    def test_tool_response_serialization(self):
        resp = ToolResponse(
            id="789", name="echo", content=json.dumps({"message": "Hello!"})
        )
        serialized = resp.model_dump_json()
        assert '"id":"789"' in serialized
        assert '"name":"echo"' in serialized
        assert '"content":"{\\"message\\": \\"Hello!\\"}"' in serialized


class TestMessage:
    BASE_DATE: str = datetime(2023, 10, 1, 12, 0, 0).isoformat()

    def test_message_fields(self):
        msg = Message(
            role=MessageRole.USER, content="Hello, world!", timestamp=self.BASE_DATE
        )
        assert msg.role == MessageRole.USER
        assert msg.content == "Hello, world!"
        assert msg.timestamp == self.BASE_DATE

    def test_message_serialization(self):
        msg = Message(
            role=MessageRole.AGENT,
            content="This is a response.",
            timestamp=self.BASE_DATE,
        )
        serialized = msg.model_dump_json()
        assert "assistant" in serialized
        assert "This is a response." in serialized
        assert f"{self.BASE_DATE}" in serialized

    def test_immutable_fields(self):
        msg = Message(
            role=MessageRole.USER, content="Hello, world!", timestamp=self.BASE_DATE
        )
        with pytest.raises(ValueError):
            msg.role = MessageRole.AGENT
        with pytest.raises(ValueError):
            msg.timestamp = datetime.now().isoformat()


class TestUserMessage:
    def test_user_message_inherits_from_message(self):
        user_msg = UserMessage(content="User message content")
        assert isinstance(user_msg, Message)
        assert user_msg.role == MessageRole.USER

    def test_user_message_serialization(self):
        user_msg = UserMessage(content="This is a user message.")
        serialized = user_msg.model_dump_json()
        assert "user" in serialized
        assert "This is a user message." in serialized

    def test_user_message_tool_response(self):
        user_msg = UserMessage(
            tool_response=ToolResponse(
                id="123", name="tool1", content=json.dumps({"result": 42})
            )
        )
        if not user_msg.tool_response:
            raise ValueError("Tool response should not be None.")
        assert user_msg.tool_response.id == "123"
        assert user_msg.tool_response.name == "tool1"


class TestAgentMessage:
    def test_agent_message_inherits_from_message(self):
        agent_msg = AgentMessage(content="Agent message content")
        assert isinstance(agent_msg, Message)
        assert agent_msg.role == MessageRole.AGENT

    def test_agent_message_serialization(self):
        agent_msg = AgentMessage(content="This is an agent response.")
        serialized = agent_msg.model_dump_json()
        assert "assistant" in serialized
        assert "This is an agent response." in serialized

    def test_agent_message_tool_request(self):
        tool_request = ToolRequest(id="123", name="tool1", arguments={"arg1": "value"})
        agent_msg = AgentMessage(
            content="Agent message with tool request.", tool_requests=[tool_request]
        )
        assert len(agent_msg.tool_requests) == 1
        assert agent_msg.tool_requests[0].id == "123"
        assert agent_msg.tool_requests[0].name == "tool1"
        assert agent_msg.tool_requests[0].arguments == {"arg1": "value"}
