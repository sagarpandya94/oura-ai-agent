import pytest
from agents.health_agent import HealthAgent
from agents.tool_calling_agent import ToolCallingAgent
from agents.memory_agent import MemoryAgent


@pytest.mark.integration
class TestHealthAgentIntegration:
    def test_claude_returns_health_insight(self):
        agent = HealthAgent(provider="claude")
        result = agent.analyze()
        assert isinstance(result, str)
        assert len(result) > 100

    def test_claude_insight_mentions_sleep(self):
        agent = HealthAgent(provider="claude")
        result = agent.analyze()
        assert any(word in result.lower() for word in ["sleep", "rest", "recovery"])

    def test_claude_insight_mentions_activity(self):
        agent = HealthAgent(provider="claude")
        result = agent.analyze()
        assert any(word in result.lower() for word in ["activity", "steps", "active"])


@pytest.mark.integration
class TestToolCallingAgentIntegration:
    def test_sleep_query_returns_response(self):
        agent = ToolCallingAgent()
        result = agent.run("How was my sleep last night?")
        assert isinstance(result, str)
        assert len(result) > 100

    def test_workout_query_returns_response(self):
        agent = ToolCallingAgent()
        result = agent.run("Am I ready for an intense workout today?")
        assert isinstance(result, str)
        assert len(result) > 100

    def test_full_summary_returns_response(self):
        agent = ToolCallingAgent()
        result = agent.run("Give me a full health summary")
        assert isinstance(result, str)
        assert len(result) > 100


@pytest.mark.integration
class TestMemoryAgentIntegration:
    def test_multi_turn_conversation(self):
        agent = MemoryAgent()
        response1 = agent.run("How was my sleep last night?")
        assert isinstance(response1, str)
        assert len(response1) > 100

        response2 = agent.run("How does that compare to my activity?")
        assert isinstance(response2, str)
        assert len(response2) > 100

    def test_memory_resets_correctly(self):
        agent = MemoryAgent()
        agent.run("How was my sleep?")
        assert len(agent.conversation_history) > 0

        agent.reset_memory()
        assert len(agent.conversation_history) == 0

        agent.run("How was my activity?")
        assert len(agent.conversation_history) > 0