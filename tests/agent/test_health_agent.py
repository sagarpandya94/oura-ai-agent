import pytest
from unittest.mock import MagicMock, patch
from agents.health_agent import HealthAgent


class TestHealthAgentInit:
    def test_claude_provider_initializes(self):
        with patch("agents.health_agent.Anthropic"):
            agent = HealthAgent(provider="claude")
            assert agent.provider == "claude"

    def test_gemini_provider_initializes(self):
        with patch("agents.health_agent.genai.Client"):
            agent = HealthAgent(provider="gemini")
            assert agent.provider == "gemini"

    def test_invalid_provider_raises_error(self):
        with pytest.raises(ValueError) as exc_info:
            HealthAgent(provider="openai")
        assert "Unsupported provider" in str(exc_info.value)


class TestHealthAgentAnalyze:
    @patch("agents.health_agent.Anthropic")
    def test_claude_returns_string(self, mock_anthropic):
        mock_message = MagicMock()
        mock_message.content[0].text = "You slept well. Go for a walk."
        mock_anthropic.return_value.messages.create.return_value = mock_message

        agent = HealthAgent(provider="claude")
        result = agent.analyze()

        assert isinstance(result, str)
        assert len(result) > 0

    @patch("agents.health_agent.genai.Client")
    def test_gemini_returns_string(self, mock_genai):
        mock_response = MagicMock()
        mock_response.text = "Your readiness is moderate. Rest today."
        mock_genai.return_value.models.generate_content.return_value = mock_response

        agent = HealthAgent(provider="gemini")
        result = agent.analyze()

        assert isinstance(result, str)
        assert len(result) > 0

    @patch("agents.health_agent.Anthropic")
    def test_claude_calls_correct_model(self, mock_anthropic):
        mock_message = MagicMock()
        mock_message.content[0].text = "Some insight"
        mock_anthropic.return_value.messages.create.return_value = mock_message

        agent = HealthAgent(provider="claude")
        agent.analyze()

        call_kwargs = mock_anthropic.return_value.messages.create.call_args.kwargs
        assert call_kwargs["model"] == "claude-opus-4-20250514"

    @patch("agents.health_agent.Anthropic")
    def test_analyze_includes_all_health_data(self, mock_anthropic):
        mock_message = MagicMock()
        mock_message.content[0].text = "Some insight"
        mock_anthropic.return_value.messages.create.return_value = mock_message

        agent = HealthAgent(provider="claude")
        agent.analyze()

        call_kwargs = mock_anthropic.return_value.messages.create.call_args.kwargs
        prompt = call_kwargs["messages"][0]["content"]
        assert "Sleep Data" in prompt
        assert "Readiness Data" in prompt
        assert "Activity Data" in prompt