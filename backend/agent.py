from langchain.chat_models import init_chat_model
from dotenv import load_dotenv

from langchain_core.messages import HumanMessage, AIMessage
from langgraph.graph import StateGraph, END

from tools import icd10_search_tool, recommendation_tool, urgency_scorer
from data_type import AgentState
import os


load_dotenv()


class HealthBuddyAgent:
    def __init__(self):
        def call_llm(state: AgentState):
            model = init_chat_model("gemini-2.5-flash", model_provider="google_genai", google_api_key=os.environ.get("GOOGLE_API_KEY") )
            messages = state['messages']
            tools =[icd10_search_tool, recommendation_tool, urgency_scorer]
            model.bind_tools(tools)
            return {'messages': [model.invoke(messages)]}

        workflow = StateGraph(AgentState)

        workflow.add_node("llm", call_llm)

        workflow.set_entry_point("llm")

        workflow.add_edge("llm", END)

        self.compiled_workflow = workflow.compile()

    def invoke(self, state: AgentState):
        return self.compiled_workflow.invoke(state)


