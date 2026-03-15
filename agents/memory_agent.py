import os
import json
from anthropic import Anthropic
from dotenv import load_dotenv
from api.oura_client import OuraClient

load_dotenv()

TOOLS = [
    {
        "name": "get_sleep_data",
        "description": "Fetches the user's sleep data including score, duration, REM, deep sleep and efficiency",
        "input_schema": {
            "type": "object",
            "properties": {},
            "required": []
        }
    },
    {
        "name": "get_readiness_data",
        "description": "Fetches the user's readiness data including score, HRV balance and recovery index",
        "input_schema": {
            "type": "object",
            "properties": {},
            "required": []
        }
    },
    {
        "name": "get_activity_data",
        "description": "Fetches the user's activity data including steps, calories and active time",
        "input_schema": {
            "type": "object",
            "properties": {},
            "required": []
        }
    }
]


class MemoryAgent:
    def __init__(self):
        self.client = Anthropic(api_key=os.getenv("ANTHROPIC_API_KEY"))
        self.oura = OuraClient()
        self.conversation_history = []

    def _execute_tool(self, tool_name):
        if tool_name == "get_sleep_data":
            return self.oura.get_sleep()
        elif tool_name == "get_readiness_data":
            return self.oura.get_daily_readiness()
        elif tool_name == "get_activity_data":
            return self.oura.get_daily_activity()
        else:
            raise ValueError(f"Unknown tool: {tool_name}")

    def reset_memory(self):
        """Clear conversation history to start fresh"""
        self.conversation_history = []
        print("🧹 Memory cleared")

    def run(self, user_query):
        """Run the agent maintaining conversation history"""
        print(f"\n🤔 You: {user_query}\n")

        # Add user message to history
        self.conversation_history.append({
            "role": "user",
            "content": user_query
        })

        # Agentic loop
        while True:
            response = self.client.messages.create(
                model="claude-opus-4-20250514",
                max_tokens=1024,
                system="You are a personal health analyst. You have memory of the entire conversation. Reference previous answers when relevant.",
                tools=TOOLS,
                messages=self.conversation_history
            )

            if response.stop_reason == "end_turn":
                final_response = next(
                    block.text for block in response.content
                    if hasattr(block, "text")
                )
                # Add assistant response to history
                self.conversation_history.append({
                    "role": "assistant",
                    "content": final_response
                })
                print(f"🤖 Agent: {final_response}")
                return final_response

            if response.stop_reason == "tool_use":
                self.conversation_history.append({
                    "role": "assistant",
                    "content": response.content
                })

                tool_results = []
                for block in response.content:
                    if block.type == "tool_use":
                        print(f"🔧 Calling tool: {block.name}")
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