"""Defines the state structure for the learning agent."""

from typing import Annotated, Sequence, TypedDict
# from typing_extensions import TypedDict
from langchain_core.messages import BaseMessage
from langgraph.graph import add_messages

class LeadFlowAgentState(TypedDict):
    """Defines the state structure for the learning agent."""

    messages: Annotated[Sequence[BaseMessage], add_messages]