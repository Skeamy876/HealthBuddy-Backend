from dotenv import load_dotenv
from langgraph.prebuilt import ToolNode

from health_buddy_agent.utils.tools import icd10_search_tool
from health_buddy_agent.utils.state import AgentState
from langchain_core.messages import SystemMessage
from health_buddy_agent.utils.prompts import system_prompt
from health_buddy_agent.utils.models import _get_model_name

load_dotenv()

def should_continue(state):
    messages = state["messages"]
    last_message = messages[-1]
    # If there are no tool calls, then we finish
    if not last_message.tool_calls:
        return "end"
    # Otherwise if there is, we continue
    else:
        return "continue"

def call_llm(state: AgentState, config):
    model = _get_model_name()
    messages = state['messages']
    messages = [SystemMessage(content=system_prompt)] + messages
    
    return {'messages': [model.invoke(messages)]}

tool_node = ToolNode([icd10_search_tool])
