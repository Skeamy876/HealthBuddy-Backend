
import os
from typing import Literal, TypedDict
from langgraph.graph import StateGraph, END

from health_buddy_agent.utils.nodes import call_llm, tool_node, should_continue
from health_buddy_agent.utils.state import AgentState
from dotenv import load_dotenv


load_dotenv()



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

from langgraph.checkpoint.memory import MemorySaver
checkpointer = MemorySaver()
compiled_workflow = workflow.compile(checkpointer=checkpointer).with_config(
    {
        "configurable": {
            "thread_id": "1",
        }
    }
)

# is_langgraph_api = (
#     os.environ.get("LANGGRAPH_API", "false").lower() == "true" or
#     os.environ.get("LANGGRAPH_API_DIR") is not None
# )

# if is_langgraph_api:
#     # When running in LangGraph API/dev, don't use a custom checkpointer
# compiled_workflow = workflow.compile()
# else:
#     # For CopilotKit and other contexts, use MemorySaver
#     from langgraph.checkpoint.memory import MemorySaver
#     memory = MemorySaver()
#     compiled_workflow = workflow.compile(checkpointer=memory)




