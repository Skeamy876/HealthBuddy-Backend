from langchain.chat_models import init_chat_model
from langchain_google_genai import ChatGoogleGenerativeAI 
from dotenv import load_dotenv
from langgraph.prebuilt import ToolNode


from health_buddy_agent.utils import tools
from health_buddy_agent.utils.tools import icd10_search_tool, recommendation_tool, urgency_scorer
from health_buddy_agent.utils.state import AgentState
import os


load_dotenv()


def _get_model_name(model_name: str):
    if model_name == "gemini-2.5-Pro":
        model = ChatGoogleGenerativeAI(temperature=0,model="gemini-2.0-flash",google_api_key=os.environ.get("GOOGLE_API_KEY") )
    # elif model_name == "openai":
    #     model = init_chat_model("gpt-4o", model_provider="openai", openai_api_key=os.environ.get("OPENAI_API_KEY"))
    else:
        raise ValueError(f"Unsupported model name: {model_name}")
    
    model = model.bind_tools([icd10_search_tool, recommendation_tool, urgency_scorer])

    return model



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
    model_name = config.get('configurable', {}).get("model_name","gemini-2.5-Pro")
    model = _get_model_name(model_name)
    messages = state['messages']
    return {'messages': [model.invoke(messages)]}



tool_node = ToolNode([icd10_search_tool, recommendation_tool, urgency_scorer])
