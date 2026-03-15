import pytest
from unittest.mock import MagicMock, patch
from agents.tool_calling_agent import ToolCallingAgent


@pytest.fixture
def agent():
    with patch("agents.tool_calling_agent.Anthropic"):
        return ToolCallingAgent()


def make_tool_use_block(tool_name, tool_id):
    """Helper to create a mock tool use block"""
    block = MagicMock()
    block.type = "tool_use"
    block.name = tool_name
    block.id = tool_id
    return block


def make_text_block(text):
    """Helper to create a mock text block"""
    block = MagicMock()
    block.type = "text"
    block.text = text
    return block


class TestToolExecution:
    def test_execute_sleep_tool(self, agent):
        result = agent._execute_tool("get_sleep_data")
        assert "data" in result

    def test_execute_readiness_tool(self, agent):
        result = agent._execute_tool("get_readiness_data")
        assert "data" in result

    def test_execute_activity_tool(self, agent):
        result = agent._execute_tool("get_activity_data")
        assert "data" in result

    def test_execute_unknown_tool_raises_error(self, agent):
        with pytest.raises(ValueError) as exc_info:
            agent._execute_tool("get_unknown_tool")
        assert "Unknown tool" in str(exc_info.value)


class TestAgentRun:
    def test_agent_returns_string_response(self, agent):
        # Simulate Claude returning a final response directly
        mock_response = MagicMock()
        mock_response.stop_reason = "end_turn"
        mock_response.content = [make_text_block("Your sleep was great!")]

        agent.client.messages.create.return_value = mock_response

        result = agent.run("How was my sleep?")
        assert isinstance(result, str)
        assert len(result) > 0

    def test_agent_calls_tool_then_returns_response(self, agent):
        # First response: Claude calls a tool
        tool_response = MagicMock()
        tool_response.stop_reason = "tool_use"
        tool_response.content = [make_tool_use_block("get_sleep_data", "tool_1")]

        # Second response: Claude returns final answer
        final_response = MagicMock()
        final_response.stop_reason = "end_turn"
        final_response.content = [make_text_block("Your sleep score was 82.")]

        agent.client.messages.create.side_effect = [tool_response, final_response]

        result = agent.run("How was my sleep?")
        assert isinstance(result, str)

    def test_agent_calls_multiple_tools(self, agent):
        # First response: Claude calls two tools
        tool_response = MagicMock()
        tool_response.stop_reason = "tool_use"
        tool_response.content = [
            make_tool_use_block("get_sleep_data", "tool_1"),
            make_tool_use_block("get_readiness_data", "tool_2")
        ]

        # Second response: Claude returns final answer
        final_response = MagicMock()
        final_response.stop_reason = "end_turn"
        final_response.content = [make_text_block("Based on sleep and readiness data...")]

        agent.client.messages.create.side_effect = [tool_response, final_response]

        result = agent.run("Am I ready for a workout?")
        assert isinstance(result, str)

    def test_agent_makes_multiple_api_calls_when_using_tools(self, agent):
        # First response: tool call
        tool_response = MagicMock()
        tool_response.stop_reason = "tool_use"
        tool_response.content = [make_tool_use_block("get_activity_data", "tool_1")]

        # Second response: final answer
        final_response = MagicMock()
        final_response.stop_reason = "end_turn"
        final_response.content = [make_text_block("Your activity was moderate.")]

        agent.client.messages.create.side_effect = [tool_response, final_response]

        agent.run("How active was I?")

        # Claude should have been called twice — once for tool, once for final answer
        assert agent.client.messages.create.call_count == 2