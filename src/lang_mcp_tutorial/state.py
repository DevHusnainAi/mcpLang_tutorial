"""Defines the state structure for the learning agent."""

from typing import Annotated, Sequence, TypedDict, Optional
# from typing_extensions import TypedDict
from langchain_core.messages import BaseMessage
from langgraph.graph import add_messages

class LangMCPAgentState(TypedDict):
    """Defines the state structure for the learning agent."""

    messages: Annotated[Sequence[BaseMessage], add_messages]

    def __init__(self):
        """Initialize the state with default values."""
        self.messages = []