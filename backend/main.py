from fastapi import FastAPI, UploadFile, File
from agent import HealthBuddyAgent
from data_type import DiagnosisResult, SymptomInput
import json

app = FastAPI(title="HealthBuddy AI Symptom Checker")




@app.post("/diagnose", response_model=DiagnosisResult)
def diagnose(input: SymptomInput):
    initial_state = {
        "messages": [
            {
                "role": "user",
                "content": f"Patient symptoms: {input.symptoms}. Return probable conditions, ICD-10 codes, urgency, and recommendations as a JSON object with keys: probable_conditions, icd10_codes, urgency_score, recommendations. Use the matching tools to provide accurate results."
            }
        ]
    }

    health_agent = HealthBuddyAgent()

    result = health_agent.invoke(initial_state)

    print(result)

    final_message = result['messages'][-1]
    response_text = final_message.content

    try:
        diagnosis_data = json.loads(response_text)
        return DiagnosisResult(
            probable_conditions=diagnosis_data.get("probable_conditions", []),
            icd10_codes=diagnosis_data.get("icd10_codes", []),
            urgency_score=diagnosis_data.get("urgency_score", 0.0),
            recommendations=diagnosis_data.get("recommendations", [])
        )
    except Exception:
        # Fallback if parsing fails or JSON is not as expected
        return DiagnosisResult(
            probable_conditions=[response_text if response_text else "Could not parse diagnosis."],
            icd10_codes=[],
            urgency_score=0.5,
            recommendations=["See a doctor if symptoms worsen or if you have concerns."]
        )

@app.post("/voice", response_model=DiagnosisResult)
def diagnose_voice(file: UploadFile = File(...)):
    # TODO: Integrate Whisper STT
    # TODO: Pass transcribed text to diagnosis pipeline
    return DiagnosisResult(
        probable_conditions=["Voice input not yet supported"],
        icd10_codes=[],
        urgency_score=0.0,
        recommendations=["Please use text input for now."]
    )

@app.get("/")
def root():
    return {"message": "Welcome to HealthBuddy AI Symptom Checker API!"}

def main():
    print("Hello from healthbuddyagentapi!")


if __name__ == "__main__":
    main()
