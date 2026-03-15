import os
import json
from anthropic import Anthropic
from dotenv import load_dotenv
from api.oura_client import OuraClient

load_dotenv()

# Define tools that Claude can call
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


class ToolCallingAgent:
    def __init__(self):
        self.client = Anthropic(api_key=os.getenv("ANTHROPIC_API_KEY"))
        self.oura = OuraClient()

    def _execute_tool(self, tool_name):
        """Execute the requested tool and return results"""
        if tool_name == "get_sleep_data":
            return self.oura.get_sleep()
        elif tool_name == "get_readiness_data":
            return self.oura.get_daily_readiness()
        elif tool_name == "get_activity_data":
            return self.oura.get_daily_activity()
        else:
            raise ValueError(f"Unknown tool: {tool_name}")

    def run(self, user_query):
        """Run the agent with multi-step reasoning"""
        print(f"\n🤔 User Query: {user_query}\n")

        messages = [
            {"role": "user", "content": user_query}
        ]

        # Agentic loop - keeps running until Claude stops calling tools
        while True:
            response = self.client.messages.create(
                model="claude-opus-4-20250514",
                max_tokens=1024,
                tools=TOOLS,
                messages=messages
            )

            # If Claude is done reasoning, return final response
            if response.stop_reason == "end_turn":
                final_response = next(
                    block.text for block in response.content
                    if hasattr(block, "text")
                )
                print(f"\n✅ Final Response:\n{final_response}")
                return final_response

            # If Claude wants to use tools, execute them
            if response.stop_reason == "tool_use":
                # Add Claude's response to message history
                messages.append({
                    "role": "assistant",
                    "content": response.content
                })

                # Process each tool call
                tool_results = []
                for block in response.content:
                    if block.type == "tool_use":
                        print(f"🔧 Claude is calling tool: {block.name}")
                        result = self._execute_tool(block.name)
                        tool_results.append({
                            "type": "tool_result",
                            "tool_use_id": block.id,
                            "content": json.dumps(result)
                        })

                # Add tool results back to message history
                messages.append({
                    "role": "user",
                    "content": tool_results
                })