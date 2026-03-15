"""
Demo script to showcase the Oura AI Agent capabilities.
Run individual demos by commenting/uncommenting sections below.
"""
from agents.health_agent import HealthAgent
from agents.tool_calling_agent import ToolCallingAgent
from agents.memory_agent import MemoryAgent


def demo_health_agent():
    print("\n" + "="*50)
    print("DEMO 1: Health Agent (Single Shot Analysis)")
    print("="*50)
    agent = HealthAgent(provider="claude")
    print(agent.analyze())


def demo_tool_calling_agent():
    print("\n" + "="*50)
    print("DEMO 2: Tool Calling Agent (Multi-Step Reasoning)")
    print("="*50)
    agent = ToolCallingAgent()
    agent.run("How was my sleep last night?")
    agent.run("Am I ready for an intense workout today?")
    agent.run("Give me a full health summary")


def demo_memory_agent():
    print("\n" + "="*50)
    print("DEMO 3: Memory Agent (Multi-Turn Conversation)")
    print("="*50)
    agent = MemoryAgent()
    agent.run("How was my sleep last night?")
    agent.run("How does that compare to my activity?")
    agent.run("What should I focus on improving?")


if __name__ == "__main__":
    demo_health_agent()
    demo_tool_calling_agent()
    demo_memory_agent()