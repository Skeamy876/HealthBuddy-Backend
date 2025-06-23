
from fastapi import FastAPI, UploadFile, File
from data_type import DiagnosisResult, SymptomInput
from health_buddy_agent.agent import compiled_workflow



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


    result = compiled_workflow.invoke(initial_state, config={"configurable": {"gemini-2.5-Pro": "gemini-2.5-Pro"}})

    final_message = result['messages'][-1]
    response_text = final_message.content

    try:
              # Clean the response text by removing markdown fences if present
        cleaned_response_text = response_text.strip()
        if cleaned_response_text.startswith("```json"):
            cleaned_response_text = cleaned_response_text[len("```json"):].strip()
        if cleaned_response_text.endswith("```"):
            cleaned_response_text = cleaned_response_text[:-len("```")].strip()

        # Corrected: Parse the cleaned response_text directly
        diagnosis_data = json.loads(cleaned_response_text)

        if not isinstance(diagnosis_data, dict):
            raise ValueError("Response is not a valid JSON object")

        return DiagnosisResult(
            probable_conditions=diagnosis_data.get("probable_conditions", []),
            icd10_codes=diagnosis_data.get("icd10_codes", []),
            urgency_score=diagnosis_data.get("urgency_score", 0.0),
            recommendations=diagnosis_data.get("recommendations", [])
        )
    except Exception as e:
        print(f"Error parsing response: {e}")
        print(f"Response text: {response_text}")
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
