from langchain.chat_models import init_chat_model
from langchain_google_genai import ChatGoogleGenerativeAI 
from dotenv import load_dotenv
from langgraph.prebuilt import ToolNode
from google.ai.generativelanguage_v1beta.types import Tool as GenAITool


from utils.tools import icd10_search_tool
from utils.state import AgentState
from langchain_core.messages import SystemMessage

import os


load_dotenv()

system_prompt = """ 
    You are a board‑certified AI Health Diagnostic Agent.  
    You take in a list of patient symptoms and deliver a full‑blown differential diagnosis, coded findings, urgency scoring, and clear recommendations.  
    You have access to exactly one tool:

    • icd10_search_tool – returns ICD‑10 codes and descriptions.


    Your objectives:
    1. Carefully analyze the patient's symptoms.
    2. For each symptom, call icd10_search_tool to fetch the official ICD‑10 code.
    3. Parse and prioritize the most likely conditions based on symptoms and any information gathered from tools.
    4. Assign an urgency score between 0.0 (non‑urgent) and 1.0 (emergency).
    5. Generate specific, evidence‑based recommendations (e.g., “seek ER within 2 h,” “start NSAID,” “schedule telehealth follow‑up”).

    Your reasoning style: ReAct  
    —️ You MUST show your chain of thought.  
    —️ Always alternate Thought/Action/Observation until you’ve exhausted tool calls.  
    —️ Conclude with a single Final Answer block.

    """


# removed implementation of google_search_tool as it was not defined in the original code
# google_search_tool = GenAITool(google_search={})

def _get_model_name():
    model = ChatGoogleGenerativeAI(temperature=0,model="gemini-2.5-flash",google_api_key=os.environ.get("GOOGLE_API_KEY") )
    return model.bind_tools([icd10_search_tool])





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
    messages= [SystemMessage(content=system_prompt)] + messages
    
    return {'messages': [model.invoke(messages)]}




tool_node = ToolNode([icd10_search_tool])
