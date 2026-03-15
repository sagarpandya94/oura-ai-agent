import pytest
from unittest.mock import MagicMock, patch
from agents.health_agent import HealthAgent


class TestHealthAgentErrorHandling:
    @patch("agents.health_agent.Anthropic")
    def test_llm_exception_raises_runtime_error(self, mock_anthropic):
        mock_anthropic.return_value.messages.create.side_effect = Exception(
            "Connection timeout"
        )
        agent = HealthAgent(provider="claude")
        with pytest.raises(RuntimeError) as exc_info:
            agent.analyze()
        assert "Failed to get response from claude" in str(exc_info.value)

    @patch("agents.health_agent.Anthropic")
    def test_empty_llm_response_raises_runtime_error(self, mock_anthropic):
        mock_message = MagicMock()
        mock_message.content[0].text = ""
        mock_anthropic.return_value.messages.create.return_value = mock_message
        agent = HealthAgent(provider="claude")
        with pytest.raises(RuntimeError) as exc_info:
            agent.analyze()
        assert "empty response" in str(exc_info.value)

    @patch("agents.health_agent.Anthropic")
    def test_fixture_error_propagates(self, mock_anthropic):
        agent = HealthAgent(provider="claude")
        with patch.object(agent.oura, "get_sleep", side_effect=RuntimeError("Fixture not found")):
            with pytest.raises(RuntimeError) as exc_info:
                agent.analyze()
            assert "Fixture not found" in str(exc_info.value)

    def test_unsupported_provider_raises_value_error(self):
        with pytest.raises(ValueError) as exc_info:
            HealthAgent(provider="openai")
        assert "Unsupported provider" in str(exc_info.value)


class TestToolCallingAgentErrorHandling:
    @patch("agents.tool_calling_agent.Anthropic")
    def test_llm_exception_raises_runtime_error(self, mock_anthropic):
        mock_anthropic.return_value.messages.create.side_effect = Exception(
            "Connection timeout"
        )
        from agents.tool_calling_agent import ToolCallingAgent
        agent = ToolCallingAgent()
        with pytest.raises(RuntimeError) as exc_info:
            agent.run("How was my sleep?")
        assert "Failed to get response from Claude" in str(exc_info.value)

    @patch("agents.tool_calling_agent.Anthropic")
    def test_unknown_tool_raises_value_error(self, mock_anthropic):
        from agents.tool_calling_agent import ToolCallingAgent
        agent = ToolCallingAgent()
        with pytest.raises(ValueError) as exc_info:
            agent._execute_tool("get_unknown_tool")
        assert "Unknown tool" in str(exc_info.value)

    @patch("agents.tool_calling_agent.Anthropic")
    def test_tool_runtime_error_propagates(self, mock_anthropic):
        from agents.tool_calling_agent import ToolCallingAgent
        agent = ToolCallingAgent()
        with patch.object(agent.oura, "get_sleep", side_effect=RuntimeError("Fixture not found")):
            with pytest.raises(RuntimeError):
                agent._execute_tool("get_sleep_data")


class TestMemoryAgentErrorHandling:
    @patch("agents.memory_agent.Anthropic")
    def test_llm_exception_raises_runtime_error(self, mock_anthropic):
        mock_anthropic.return_value.messages.create.side_effect = Exception(
            "Connection timeout"
        )
        from agents.memory_agent import MemoryAgent
        agent = MemoryAgent()
        with pytest.raises(RuntimeError) as exc_info:
            agent.run("How was my sleep?")
        assert "Failed to get response from Claude" in str(exc_info.value)

    @patch("agents.memory_agent.Anthropic")
    def test_unknown_tool_raises_value_error(self, mock_anthropic):
        from agents.memory_agent import MemoryAgent
        agent = MemoryAgent()
        with pytest.raises(ValueError) as exc_info:
            agent._execute_tool("get_unknown_tool")
        assert "Unknown tool" in str(exc_info.value)