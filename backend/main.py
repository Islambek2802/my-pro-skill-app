# backend/main.py (ВЕРСИЯ С ГЕНЕРАЦИЕЙ ГОЛОСА)

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
    {
        "id": 1,
        "title": "Handling the Price Objection",
        "goal": "Convince the client that the price is justified.",
        "customer_persona": "A potential client who thinks your product is too expensive.",
    },
    {
        "id": 2,
        "title": "Getting Past the Gatekeeper",
        "goal": "Persuade the secretary to connect you with the decision-maker.",
        "customer_persona": "An experienced secretary whose job is to filter unimportant calls.",
    }
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
    # ... (эта функция остается без изменений) ...
    scenario = next((s for s in HARDCODED_SCENARIOS if s["id"] == request.scenario_id), None)
    if not scenario: raise HTTPException(status_code=404, detail="Scenario not found")
    conversation_history = "\n".join([f"{line.speaker}: {line.text}" for line in request.conversation])
    prompt = f"You are an AI assistant playing the role of a customer: {scenario['customer_persona']}. Maintain a natural dialogue and respond to the salesperson (User). Dialogue history:\n{conversation_history}\nAI:"
    try:
        response = openai.chat.completions.create(model="gpt-4o-mini", messages=[{"role": "system", "content": prompt}], temperature=0.7, max_tokens=100)
        ai_response = response.choices[0].message.content.strip()
    except Exception as e:
        print(f"OPENAI API ERROR: {e}")
        ai_response = "Sorry, I'm having a technical issue."
    return {"ai_response": ai_response}

# --- НОВЫЙ МАРШРУТ ДЛЯ ГЕНЕРАЦИИ ГОЛОСА ---
@app.post("/api/synthesize-speech")
def synthesize_speech(request: SynthesizeRequest):
    """Превращает текст в аудиофайл с помощью OpenAI TTS."""
    try:
        response = openai.audio.speech.create(
            model="tts-1",      # Стандартная, быстрая модель
            voice="nova",       # 'nova' - один из самых естественных женских голосов. Другие варианты: 'alloy', 'echo', 'fable', 'onyx', 'shimmer'
            input=request.text
        )
        # Возвращаем аудиофайл напрямую
        return Response(content=response.content, media_type="audio/mpeg")
    except Exception as e:
        print(f"OpenAI TTS Error: {e}")
        raise HTTPException(status_code=500, detail="Failed to synthesize speech")

@app.post("/api/analyze")
def analyze_simulation(request: AnalyzeRequest):
    # ... (код для анализа остается таким же) ...
    pass

@app.get("/")
def read_root():
    return {"message": "API with Voice Synthesis is running"}
