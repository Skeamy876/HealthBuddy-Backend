
import os
from fastapi import FastAPI, UploadFile, File
from data_type import DiagnosisResult, SymptomInput
from agent import compiled_workflow
from utils.tools import icd10_search_tool

import uvicorn
from copilotkit.integrations.fastapi import add_fastapi_endpoint
from copilotkit import CopilotKitRemoteEndpoint, LangGraphAgent

app = FastAPI(title="HealthBuddy AI Symptom Checker")



@app.get("/")
def root():
    return {"message": "Welcome to HealthBuddy AI Symptom Checker API!"}

sdk = CopilotKitRemoteEndpoint(
    agents=[
        LangGraphAgent(
            name="health_buddy_agent",
            description="An agent that does health check ups.",
            graph=compiled_workflow,
        )
    ],
)

add_fastapi_endpoint(app, sdk, "/copilotkit")

def main():
    """Run the uvicorn server."""
    port = int(os.getenv("PORT", "8000"))
    uvicorn.run(
        "healthybuddy:app",
        host="localhost",
        port=port,
        reload=True,
    )

