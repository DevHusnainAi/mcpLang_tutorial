# Create server parameters for stdio connection
from langchain_mcp_adapters.client import MultiServerMCPClient
from langgraph.func import entrypoint
import os
import logging
from src.lead_flow_agent.state import LeadFlowAgentState
from langchain_openai import ChatOpenAI
from langgraph.prebuilt import create_react_agent
from langgraph.graph import add_messages
from langchain_core.messages import ToolMessage, HumanMessage, AIMessage, BaseMessage
from typing import Dict, Any, List
from langgraph.checkpoint.memory import MemorySaver

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

api_key="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"

model = ChatOpenAI(model="gpt-4o-mini", api_key=api_key)

@entrypoint(checkpointer=MemorySaver())
async def lead_flow_agent(state: LeadFlowAgentState) -> Dict[str, Any]:
    print("Starting lead_flow_agent execution")
    client = MultiServerMCPClient()
    current_dir = os.path.dirname(os.path.abspath(__file__))
    print("State: ", state)

    message = state.get('messages', [])
    last_message_content = None  # Initialize to None

    if message and isinstance(message, list) and len(message) > 0:
        last_message = message[-1]

        if isinstance(last_message, dict) and 'content' in last_message:
            last_message_content = last_message['content']
        elif isinstance(last_message, str):
            last_message_content = last_message

    try:
        # Connect to math server
        print("Connecting to math server...")
        await client.connect_to_server(
            "math",
            command="python",
            args=[os.path.join(current_dir, "maths_server.py")]
        )
        print("Successfully connected to math server")

        # Create the agent
        print("Creating react agent...")
        agent = create_react_agent(model, client.get_tools())
        print("React agent created successfully")

        # Invoke the agent with the formatted message
        print("Invoking agent with message...")
        response = await agent.ainvoke({"messages": last_message_content})
        print("Agent response received", response)
        
        if response is not None and "messages" in response and isinstance(response["messages"], list):
            # Extract the messages from the response
            new_messages = response["messages"]

            # Convert the dictionaries to message objects
            message_objects: List[BaseMessage] = []

            for msg in new_messages:
                if isinstance(msg, dict): # check if the msg is a dictionary.
                    if msg["type"] == "ai":
                        message_objects.append(AIMessage(content=msg["content"], additional_kwargs=msg["additional_kwargs"], response_metadata=msg["response_metadata"], tool_calls = msg.get("tool_calls",[])))
                    elif msg["type"] == "human":
                        message_objects.append(HumanMessage(content=msg["content"], additional_kwargs=msg["additional_kwargs"], response_metadata=msg["response_metadata"]))
                    elif msg["type"] == "tool":
                        message_objects.append(ToolMessage(content=msg["content"], additional_kwargs=msg["additional_kwargs"], response_metadata=msg["response_metadata"], tool_call_id=msg["tool_call_id"]))
                elif isinstance(msg, AIMessage):
                    message_objects.append(msg)
                elif isinstance(msg, HumanMessage):
                    message_objects.append(msg)
                elif isinstance(msg, ToolMessage):
                    message_objects.append(msg)

            messages = add_messages(state["messages"], message_objects)
        else:
            messages = state["messages"]

        print("Lead flow agent execution completed successfully", messages)
        return {
            "messages": messages,
        }

    except Exception as e:
        logger.error(f"Error in lead_flow_agent: {str(e)}", exc_info=True)
        error_message = AIMessage(content=f"Error occurred: {str(e)}")
        messages = add_messages(state["messages"], [error_message])
        return {
            "messages": messages,
            "status": "error",
            "error": str(e)
        }
    finally:
        print("Closing client connection...")
        await client.exit_stack.aclose()
        print("Client connection closed")

lead_flow_agent.name = "lead_flow_agent" 