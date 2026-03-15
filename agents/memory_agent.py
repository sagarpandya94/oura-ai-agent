import os
import json
from anthropic import Anthropic
from dotenv import load_dotenv
from api.oura_client import OuraClient
from core.config import CLAUDE_MODEL, MAX_TOKENS
from tenacity import retry, stop_after_attempt, wait_exponential, retry_if_exception_type
from anthropic import InternalServerError

load_dotenv()

from core.logger import get_logger
logger = get_logger(__name__)

TOOLS = [
    {
        "name": "get_sleep_data",
        "description": "Fetches the user's sleep data including score, duration, REM, deep sleep and efficiency",
        "input_schema": {"type": "object", "properties": {}, "required": []}
    },
    {
        "name": "get_readiness_data",
        "description": "Fetches the user's readiness data including score, HRV balance and recovery index",
        "input_schema": {"type": "object", "properties": {}, "required": []}
    },
    {
        "name": "get_activity_data",
        "description": "Fetches the user's activity data including steps, calories and active time",
        "input_schema": {"type": "object", "properties": {}, "required": []}
    }
]


class MemoryAgent:
    def __init__(self):
        self.client = Anthropic(api_key=os.getenv("ANTHROPIC_API_KEY"))
        self.oura = OuraClient()
        self.conversation_history = []

    def _execute_tool(self, tool_name):
        try:
            if tool_name == "get_sleep_data":
                return self.oura.get_sleep()
            elif tool_name == "get_readiness_data":
                return self.oura.get_daily_readiness()
            elif tool_name == "get_activity_data":
                return self.oura.get_daily_activity()
            else:
                raise ValueError(f"Unknown tool: {tool_name}")
        except RuntimeError as e:
            logger.error(f"Tool execution failed for {tool_name}: {e}")
            raise

    def reset_memory(self):
        self.conversation_history = []
        logger.info("Memory cleared")

    def run(self, user_query):
        logger.info(f"User query: {user_query}")
        self.conversation_history.append({
            "role": "user",
            "content": user_query
        })

        while True:
            try:
                response = self._call_llm(self.conversation_history)
            except Exception as e:
                logger.error(f"LLM call failed: {e}")
                raise RuntimeError(f"Failed to get response from Claude: {e}")

            if response.stop_reason == "end_turn":
                final_response = next(
                    (block.text for block in response.content if hasattr(block, "text")),
                    None
                )
                if not final_response:
                    raise RuntimeError("Claude returned an empty response")
                self.conversation_history.append({
                    "role": "assistant",
                    "content": final_response
                })
                logger.info("Agent completed successfully")
                return final_response

            if response.stop_reason == "tool_use":
                self.conversation_history.append({
                    "role": "assistant",
                    "content": response.content
                })
                tool_results = []
                for block in response.content:
                    if block.type == "tool_use":
                        logger.debug(f"Calling tool: {block.name}")
                        result = self._execute_tool(block.name)
                        tool_results.append({
                            "type": "tool_result",
                            "tool_use_id": block.id,
                            "content": json.dumps(result)
                        })
                self.conversation_history.append({
                    "role": "user",
                    "content": tool_results
                })

    @retry(
        retry=retry_if_exception_type(InternalServerError),
        stop=stop_after_attempt(3),
        wait=wait_exponential(multiplier=1, min=2, max=10)
    )
    def _call_llm(self, messages):
        return self.client.messages.create(
            model=CLAUDE_MODEL,
            max_tokens=MAX_TOKENS,
            system="You are a personal health analyst. You have memory of the entire conversation. Reference previous answers when relevant.",
            tools=TOOLS,
            messages=messages
        )