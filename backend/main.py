# backend/main.py (ФИНАЛЬНАЯ ОПТИМИЗИРОВАННАЯ ВЕРСИЯ)

from fastapi import FastAPI, HTTPException, Response
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List
import openai
import os
import json

# --- Настройка OpenAI API ключа ---
openai.api_key = os.getenv("OPENAI_API_KEY")

# --- Создание приложения ---
app = FastAPI()

# --- CORS ---
origins = ["*"]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# --- Вшитые сценарии ---
HARDCODED_SCENARIOS = [
    {"id": 1, "title": "Handling the Price Objection", "goal": "Convince the client the price is justified.", "customer_persona": "A client who thinks your product is too expensive."},
    {"id": 2, "title": "Getting Past the Gatekeeper", "goal": "Persuade the secretary to connect you with the decision-maker.", "customer_persona": "An experienced secretary who filters unimportant calls."},
    {"id": 3, "title": "Handling 'I need to think' Objection", "goal": "Uncover the real reason for hesitation and set a next step.", "customer_persona": "A client trying to politely end the conversation."}
]

# --- Модели данных ---
class ConversationLine(BaseModel): speaker: str; text: str
class RespondRequest(BaseModel): conversation: List[ConversationLine]; scenario_id: int
class AnalyzeRequest(BaseModel): conversation: List[ConversationLine]; scenario_id: int
class SynthesizeRequest(BaseModel): text: str

# === МАРШРУТЫ API ===
@app.get("/api/scenarios")
def get_scenarios():
    return HARDCODED_SCENARIOS

@app.post("/api/respond")
def respond(request: RespondRequest):
    scenario = next((s for s in HARDCODED_SCENARIOS if s["id"] == request.scenario_id), None)
    if not scenario: raise HTTPException(status_code=404, detail="Scenario not found")
    conversation_history = "\n".join([f"{line.speaker}: {line.text}" for line in request.conversation])
    prompt = f"You are an AI assistant playing the role of: {scenario['customer_persona']}. Keep your responses brief and natural. Dialogue history:\n{conversation_history}\nAI:"
    try:
        response = openai.chat.completions.create(model="gpt-4o-mini", messages=[{"role": "system", "content": prompt}], temperature=0.7, max_tokens=100)
        ai_response = response.choices[0].message.content.strip()
    except Exception as e:
        print(f"OPENAI API ERROR: {e}")
        ai_response = "Sorry, a technical issue occurred."
    return {"ai_response": ai_response}

@app.post("/api/analyze")
def analyze_simulation(request: AnalyzeRequest):
    scenario = next((s for s in HARDCODED_SCENARIOS if s["id"] == request.scenario_id), None)
    if not scenario: raise HTTPException(status_code=404, detail="Scenario not found")
    user_transcript = "\n".join([f"{line.text}" for line in request.conversation if line.speaker == 'User'])
    prompt = f"You are a sales coach. The user's goal was: '{scenario['goal']}'. Here is what the user said: '{user_transcript}'. Provide feedback in a JSON format with keys: 'goal_achieved' (boolean), 'clarity_score' (1-10), and 'overall_assessment' (string)."
    try:
        response = openai.chat.completions.create(model="gpt-4o", messages=[{"role": "system", "content": prompt}])
        feedback_json = json.loads(response.choices[0].message.content)
        return feedback_json
    except Exception as e:
        print(f"OPENAI ANALYSIS ERROR: {e}")
        raise HTTPException(status_code=500, detail="Failed to get analysis from AI")

@app.post("/api/synthesize-speech")
def synthesize_speech(request: SynthesizeRequest):
    try:
        response = openai.audio.speech.create(model="tts-1", voice="nova", input=request.text)
        return Response(content=response.content, media_type="audio/mpeg")
    except Exception as e:
        print(f"OPENAI TTS Error: {e}")
        raise HTTPException(status_code=500, detail="Failed to synthesize speech")

@app.get("/")
def read_root():
    return {"message": "Optimized API is running"}
