# backend/main.py (УПРОЩЕННАЯ ВЕРСИЯ)

import os
import openai
import json
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List

# --- Настройка ---
app = FastAPI()

# --- CORS ---
origins = [
    "http://localhost:3000",
    # Сюда вы позже добавите адрес вашего запущенного сайта
]
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
        "id": 1,
        "title": "Работа с возражением о цене",
        "goal": "Убедить клиента, что цена оправдана, и предложить демонстрацию продукта.",
        "customer_persona": "Клиент, который считает, что ваш продукт слишком дорогой по сравнению с конкурентами.",
        "required_keywords": ["ценность", "долгосрочная выгода", "качество поддержки"]
    },
    {
        "id": 2,
        "title": "Назначение повторной встречи",
        "goal": "Завершить первый звонок с четкой договоренностью о следующей встрече с техническими специалистами.",
        "customer_persona": "Заинтересованный, но очень занятой менеджер, у которого мало времени.",
        "required_keywords": ["удобное время", "календарь", "коллеги"]
    }
]

# --- Модели данных (Pydantic) ---
class ConversationLine(BaseModel):
    speaker: str
    text: str

class AnalyzeRequest(BaseModel):
    conversation: List[ConversationLine]
    scenario_id: int


# === МАРШРУТЫ API ===

@app.get("/api/scenarios")
def get_scenarios():
    """Отдает список вшитых сценариев."""
    return HARDCODED_SCENARIOS

@app.post("/api/analyze")
def analyze_simulation(request: AnalyzeRequest):
    """Анализирует диалог на основе выбранного сценария."""
    scenario = next((s for s in HARDCODED_SCENARIOS if s["id"] == request.scenario_id), None)
    
    if not scenario:
        raise HTTPException(status_code=404, detail="Scenario not found")

    # Здесь будет логика вызова OpenAI с промптом, как и раньше
    # Для примера вернем заглушку
    feedback_json = {
        "goal_achieved": True,
        "keywords_usage": scenario["required_keywords"][:1],
        "feedback_on_goal": "Вы хорошо следовали цели сценария.",
        "overall_assessment": "Отличная работа!"
    }
    return feedback_json


@app.get("/")
def read_root():
    return {"message": "Welcome to the Simplified Skill Improvement Platform API"}
