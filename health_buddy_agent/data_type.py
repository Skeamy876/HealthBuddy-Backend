from typing_extensions import Annotated
from pydantic import BaseModel
from typing import List, Optional, TypedDict



class SymptomInput(BaseModel):
    symptoms: str
    user_id: Optional[str] = None

class DiagnosisResult(BaseModel):
    probable_conditions: List[str]
    icd10_codes: List[str]
    urgency_score: float
    recommendations: List[str]


