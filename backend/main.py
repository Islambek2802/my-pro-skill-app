# backend/main.py (ФИНАЛЬНАЯ УПРОЩЕННАЯ ВЕРСИЯ)

import os
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List

# --- Настройка ---
app = FastAPI()

# --- CORS ---
origins = ["*"] # Разрешаем все источники для простоты
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# --- Вшитые сценарии (вместо базы данных) ---
HARDCODED_SCENARIOS = [
    {
        "id": 1, "title": "Работа с возражением о цене",
        "goal": "Убедить клиента, что цена оправдана.",
        "required_keywords": ["ценность", "долгосрочная выгода"]
    },
    {
        "id": 2, "title": "Назначение повторной встречи",
        "goal": "Завершить звонок с договоренностью о следующей встрече.",
        "required_keywords": ["удобное время", "календарь"]
    }
]

# --- Модели данных ---
class ConversationLine(BaseModel):
    speaker: str
    text: str

class AnalyzeRequest(BaseModel):
    conversation: List[ConversationLine]
    scenario_id: int

# === МАРШРУТЫ API ===
@app.get("/api/scenarios")
def get_scenarios():
    return HARDCODED_SCENARIOS

@app.post("/api/analyze")
def analyze_simulation(request: AnalyzeRequest):
    scenario = next((s for s in HARDCODED_SCENARIOS if s["id"] == request.scenario_id), None)
    if not scenario:
        raise HTTPException(status_code=404, detail="Scenario not found")
    
    # Заглушка для обратной связи
    feedback_json = {
        "goal_achieved": True, "keywords_usage": scenario["required_keywords"],
        "feedback_on_goal": "Вы хорошо следовали цели сценария.",
        "overall_assessment": "Отличная работа!"
    }
    return feedback_json

@app.get("/")
def read_root():
    return {"message": "Simplified API is running"}
