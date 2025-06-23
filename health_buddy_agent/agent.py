
from typing import Literal, TypedDict
from langgraph.graph import StateGraph, END
from health_buddy_agent.utils.nodes import call_llm, tool_node, should_continue
from health_buddy_agent.utils.state import AgentState



class GraphConfig(TypedDict):
    model_name: Literal["gemini-2.5-Pro", "openai"]


workflow = StateGraph(AgentState, config_schema=GraphConfig)

workflow.add_node("agent", call_llm)
workflow.add_node("action", tool_node)

workflow.set_entry_point("agent")

workflow.add_conditional_edges("agent",should_continue,{
    "continue": "action",
    "end": END
})
workflow.add_edge("action", "agent")

compiled_workflow = workflow.compile()



