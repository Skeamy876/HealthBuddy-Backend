from typing_extensions import Annotated
from pydantic import BaseModel
from typing import List, Optional, TypedDict
from langgraph.graph.message import add_messages



class SymptomInput(BaseModel):
    symptoms: str
    user_id: Optional[str] = None

class DiagnosisResult(BaseModel):
    probable_conditions: List[str]
    icd10_codes: List[str]
    urgency_score: float
    recommendations: List[str]

class AgentState(TypedDict):
    messages: Annotated[list, add_messages]
