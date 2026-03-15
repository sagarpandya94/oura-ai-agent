import pytest
from unittest.mock import MagicMock, patch
from agents.memory_agent import MemoryAgent


@pytest.fixture
def agent():
    with patch("agents.memory_agent.Anthropic"):
        return MemoryAgent()


def make_tool_use_block(tool_name, tool_id):
    block = MagicMock()
    block.type = "tool_use"
    block.name = tool_name
    block.id = tool_id
    return block


def make_text_block(text):
    block = MagicMock()
    block.type = "text"
    block.text = text
    return block


def make_end_turn_response(text):
    response = MagicMock()
    response.stop_reason = "end_turn"
    response.content = [make_text_block(text)]
    return response


def make_tool_use_response(tool_name, tool_id):
    response = MagicMock()
    response.stop_reason = "tool_use"
    response.content = [make_tool_use_block(tool_name, tool_id)]
    return response


class TestMemoryAgentInit:
    def test_conversation_history_starts_empty(self, agent):
        assert agent.conversation_history == []

    def test_reset_memory_clears_history(self, agent):
        agent.conversation_history = [
            {"role": "user", "content": "How was my sleep?"},
            {"role": "assistant", "content": "Your sleep was great!"}
        ]
        agent.reset_memory()
        assert agent.conversation_history == []


class TestMemoryPersistence:
    def test_history_grows_after_each_turn(self, agent):
        agent.client.messages.create.return_value = make_end_turn_response(
            "Your sleep was great!"
        )

        agent.run("How was my sleep?")
        assert len(agent.conversation_history) == 2  # user + assistant

        agent.client.messages.create.return_value = make_end_turn_response(
            "Your activity was moderate."
        )

        agent.run("How was my activity?")
        assert len(agent.conversation_history) == 4  # 2 more added

    def test_history_contains_user_messages(self, agent):
        agent.client.messages.create.return_value = make_end_turn_response(
            "Your sleep was great!"
        )

        agent.run("How was my sleep?")

        user_messages = [
            m for m in agent.conversation_history if m["role"] == "user"
        ]
        assert len(user_messages) == 1
        assert user_messages[0]["content"] == "How was my sleep?"

    def test_history_contains_assistant_messages(self, agent):
        agent.client.messages.create.return_value = make_end_turn_response(
            "Your sleep was great!"
        )

        agent.run("How was my sleep?")

        assistant_messages = [
            m for m in agent.conversation_history if m["role"] == "assistant"
        ]
        assert len(assistant_messages) == 1
        assert assistant_messages[0]["content"] == "Your sleep was great!"

    def test_history_passed_to_claude_on_second_turn(self, agent):
        agent.client.messages.create.return_value = make_end_turn_response(
            "Your sleep was great!"
        )
        agent.run("How was my sleep?")

        agent.client.messages.create.return_value = make_end_turn_response(
            "Your activity was moderate."
        )
        agent.run("How was my activity?")

        second_call_messages = agent.client.messages.create.call_args.kwargs["messages"]
        # All 4 messages are passed proving memory persists across turns
        assert len(second_call_messages) == 4
        assert second_call_messages[0]["content"] == "How was my sleep?"
        assert second_call_messages[1]["content"] == "Your sleep was great!"
        assert second_call_messages[2]["content"] == "How was my activity?"
        assert second_call_messages[3]["content"] == "Your activity was moderate."


class TestMemoryAgentRun:
    def test_returns_string_response(self, agent):
        agent.client.messages.create.return_value = make_end_turn_response(
            "Your sleep was great!"
        )
        result = agent.run("How was my sleep?")
        assert isinstance(result, str)
        assert len(result) > 0

    def test_tool_call_then_final_response(self, agent):
        agent.client.messages.create.side_effect = [
            make_tool_use_response("get_sleep_data", "tool_1"),
            make_end_turn_response("Your sleep score was 82.")
        ]

        result = agent.run("How was my sleep?")
        assert isinstance(result, str)
        assert agent.client.messages.create.call_count == 2

    def test_reset_then_run_starts_fresh(self, agent):
        agent.client.messages.create.return_value = make_end_turn_response(
            "Your sleep was great!"
        )
        agent.run("How was my sleep?")
        assert len(agent.conversation_history) == 2

        agent.reset_memory()
        assert len(agent.conversation_history) == 0

        agent.client.messages.create.return_value = make_end_turn_response(
            "Your activity was moderate."
        )
        agent.run("How was my activity?")

        # Should only have 2 messages, not 4
        assert len(agent.conversation_history) == 2