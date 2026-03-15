from agents.tool_calling_agent import ToolCallingAgent

agent = ToolCallingAgent()

# Ask different questions and watch Claude decide which tools to call
agent.run("How was my sleep last night?")
agent.run("Am I ready for an intense workout today?")
agent.run("Give me a full health summary")