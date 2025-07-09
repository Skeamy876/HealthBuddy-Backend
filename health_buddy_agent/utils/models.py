import os
from langchain_google_genai import ChatGoogleGenerativeAI
from health_buddy_agent.utils.tools import icd10_search_tool
from dotenv import load_dotenv

load_dotenv()

def _get_model_name():
    model_name = os.environ.get("MODEL_NAME", "gemini-2.0-flash")
    model = ChatGoogleGenerativeAI(temperature=0,model=model_name,google_api_key=os.environ.get("GOOGLE_API_KEY") )
    return model.bind_tools([icd10_search_tool])
