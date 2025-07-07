from typing import Annotated, Sequence, TypedDict
from langgraph.graph.message import add_messages
from langchain_core.messages import BaseMessage
from copilotkit import CopilotKitState





class AgentState(CopilotKitState):
    messages: Annotated[Sequence[BaseMessage], add_messages]