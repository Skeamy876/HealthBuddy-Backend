
from fastapi import FastAPI, UploadFile, File
from data_type import DiagnosisResult, SymptomInput
# from health_buddy_agent.agent import compiled_workflow
from utils.tools import icd10_search_tool



app = FastAPI(title="HealthBuddy AI Symptom Checker")


@app.post("/testicd10")
def test_icd10(search_term: str):
    return icd10_search_tool(search_term)




@app.post("/diagnose", response_model=DiagnosisResult)
def diagnose(input: SymptomInput):
    initial_state = {
        "messages": [
            {
                "role": "user",
                "content": f"""
                    You are a helpful AI health agent that takes in a list of symptoms and outputs a structured diagnosis. You can use the following tools to help you:

                    TOOLS HAVE BEEN binded to the model, so you can call them directly in your reasoning.

                    Your job is to:
                    1. Identify probable medical conditions from the symptoms.
                    2. Retrieve relevant ICD-10 codes for each condition.
                    3. Estimate the urgency of the symptoms on a scale of 0.0 (not urgent) to 1.0 (very urgent).
                    4. Provide actionable recommendations based on medical best practices.

                    Use the following ReAct-style format:

                    Question: the input symptoms to analyze  
                    Thought: reason about what you should do next  
                    Action: the action to take, should be one of [icd10_search]  
                    Action Input: the input to the action  
                    Observation: the result of the action  
                    ... (you can repeat Thought/Action/Observation blocks as needed)  
                    Thought: I now know the final answer  
                    Final Answer: the final structured diagnosis result
                """
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
