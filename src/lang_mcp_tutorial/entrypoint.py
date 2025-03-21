# Create server parameters for stdio connection
from langchain_mcp_adapters.client import MultiServerMCPClient
from langgraph.func import entrypoint
import os
import logging
from src.lang_mcp_tutorial.state import LangMCPAgentState
from langchain_openai import ChatOpenAI
from langgraph.graph import add_messages
from langchain_core.messages import ToolMessage, HumanMessage, AIMessage, BaseMessage
from langgraph.checkpoint.memory import MemorySaver
from src.lang_mcp_tutorial.tasks.workers import call_model
import uuid

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

model = ChatOpenAI(model="gpt-4o-mini")

checkpointer = MemorySaver()

def convert_to_message_object(msg):
    """Convert a dictionary to a proper message object."""
    if isinstance(msg, (AIMessage, HumanMessage, ToolMessage)):
        return msg
    
    if isinstance(msg, dict):
        if msg.get('type') == 'ai':
            return AIMessage(
                content=msg.get('content', ''),
                additional_kwargs=msg.get('additional_kwargs', {}),
                response_metadata=msg.get('response_metadata', {})
            )
        elif msg.get('type') == 'human':
            return HumanMessage(
                content=msg.get('content', ''),
                additional_kwargs=msg.get('additional_kwargs', {}),
                response_metadata=msg.get('response_metadata', {})
            )
        elif msg.get('type') == 'tool':
            return ToolMessage(
                content=msg.get('content', ''),
                tool_call_id=msg.get('tool_call_id', str(uuid.uuid4())),
                name=msg.get('name', 'unknown_tool'),
                additional_kwargs=msg.get('additional_kwargs', {}),
                response_metadata=msg.get('response_metadata', {})
            )
        elif msg.get('role') == 'assistant':
            return AIMessage(content=msg.get('content', ''))
        elif msg.get('role') == 'user':
            return HumanMessage(content=msg.get('content', ''))
        elif msg.get('role') == 'tool':
            return ToolMessage(
                content=msg.get('content', ''),
                tool_call_id=msg.get('tool_call_id', str(uuid.uuid4())),
                name=msg.get('name', 'unknown_tool')
            )
    return HumanMessage(content=str(msg))

@entrypoint(checkpointer=checkpointer)
async def lang_mcp_tutorial(state: LangMCPAgentState, *, previous: list[BaseMessage]):
    # Convert previous messages if they exist
    if previous:
        if isinstance(previous, dict) and 'messages' in previous:
            previous_messages = previous['messages']
        else:
            previous_messages = previous
        
        # Convert messages and add to state
        converted_messages = [convert_to_message_object(msg) for msg in previous_messages]
        state["messages"] = state.get("messages", []) + converted_messages

    print("Starting lang_mcp_tutorial execution")
    client = MultiServerMCPClient()
    current_dir = os.path.dirname(os.path.abspath(__file__))
    print("Initial state:", state)
    
    # Initialize messages if not present
    if not state.get("messages"):
        state["messages"] = []
    
    # Get current messages and convert them to proper message objects
    current_messages = [convert_to_message_object(msg) for msg in state.get('messages', [])]
    print("Current messages:", current_messages)

    try:
        # Connect to math server
        print("Connecting to math server...")
        await client.connect_to_server(
            "math",
            command="python",
            args=[os.path.join(current_dir, "mcp/maths/maths_server.py")]
        )
        print("Successfully connected to math server")

        await client.connect_to_server(
            "postgres_db",
            command="python",
            args=[os.path.join(current_dir, "mcp/database/db_server.py")]
        )
        print("Successfully connected to database server")

        # Call the model with proper async handling and full message history
        response = await call_model(messages=current_messages, client=client)
        print("Model response:", response)

        # Process response and update messages
        if response is not None:
            if isinstance(response, dict) and 'messages' in response:
                new_messages = [convert_to_message_object(msg) for msg in response['messages']]
            else:
                new_messages = [convert_to_message_object(response)]
            
            # Update state with new messages
            state["messages"] = state.get("messages", []) + new_messages
            
            return entrypoint.final(value={"messages": new_messages}, save=state)
        else:
            return entrypoint.final(value={"messages": current_messages}, save=state)

    except Exception as e:
        logger.error(f"Error in lead_flow_agent: {str(e)}", exc_info=True)
        error_message = AIMessage(content=f"Error occurred: {str(e)}")
        state["messages"] = state.get("messages", []) + [error_message]
        return entrypoint.final(
            value={"messages": [error_message]},
            save=state
        )
    finally:
        print("Closing client connection...")
        await client.exit_stack.aclose()
        print("Client connection closed")

lang_mcp_tutorial.name = "lang_mcp_tutorial" 