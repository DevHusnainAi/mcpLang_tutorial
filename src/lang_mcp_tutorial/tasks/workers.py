from langchain_core.messages import BaseMessage
from langgraph.func import task
from langchain_openai import ChatOpenAI
from langgraph.prebuilt import create_react_agent

model = ChatOpenAI(model="gpt-4o-mini")

@task
async def call_model(messages: list[BaseMessage], client: any):
    # Create the agent
    print("Creating react agent...")
    agent = create_react_agent(model, client.get_tools())
    print("React agent created successfully")

    # Invoke the agent with the formatted message
    print("Invoking agent with message...")
    response = await agent.ainvoke({"messages": messages})
    print("Agent response received", response)

    return response