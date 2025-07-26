# backend/main.py (ВЕРСИЯ С ВАШИМИ ДОКУМЕНТАМИ-СЦЕНАРИЯМИ)

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

# --- Вшитые сценарии (СПИСОК ОБНОВЛЕН) ---
HARDCODED_SCENARIOS = [
    # --- Сценарии из ваших документов ---
    {
        "id": 1,
        "title": "Квалификация клиента (BANT)",
        "goal": "Определить, подходит ли клиент, задавая вопросы о его Бюджете, Полномочиях, Потребностях и Сроках (Budget, Authority, Need, Timeline).",
        "customer_persona": "Потенциальный клиент, оставивший заявку. Он кажется заинтересованным, но может не иметь полномочий для принятия решения или четкого бюджета.",
        "required_keywords": ["бюджет", "сроки", "принимает решение", "потребность"]
    },
    {
        "id": 2,
        "title": "Работа с возражением 'Нет времени'",
        "goal": "Признать занятость клиента, быстро донести ценность и договориться о коротком конкретном следующем шаге (например, звонок на 15 минут в определенное время).",
        "customer_persona": "Очень занятой руководитель, который пытается вежливо закончить разговор, ссылаясь на нехватку времени.",
        "required_keywords": ["всего минута", "ценность", "конкретное время", "календарь"]
    },
    {
        "id": 3,
        "title": "Работа с возражением 'Дорого'",
        "goal": "Не снижая цену, сместить фокус с цены на ценность, окупаемость (ROI) и долгосрочные выгоды от использования продукта.",
        "customer_persona": "Клиент, который сравнивает ваше предложение с более дешевыми аналогами и сфокусирован только на стоимости.",
        "required_keywords": ["окупаемость", "ценность", "инвестиция", "качество"]
    },
    {
        "id": 4,
        "title": "Назначение встречи",
        "goal": "Успешно договориться о конкретной дате и времени для следующей встречи или демонстрации продукта.",
        "customer_persona": "Заинтересованный клиент, который в целом не против, но может быть неорганизованным или уклоняться от прямого назначения времени.",
        "required_keywords": ["удобно", "календарь", "подтверждение", "коллеги"]
    },
    # --- Предыдущие сценарии для разнообразия ---
    {
        "id": 5,
        "title": "Звонок от рассерженного клиента",
        "goal": "Успокоить клиента, решить его проблему и сохранить лояльность к компании.",
        "customer_persona": "Давний клиент, у которого возникла серьезная техническая проблема, и он очень недоволен.",
        "required_keywords": ["сожалею", "решить проблему", "компенсация"]
    }
]

# --- Модели данных ---
class ConversationLine(BaseModel):
    speaker: str
    text: str

class AnalyzeRequest(BaseModel):
    conversation: List[ConversationLine]
    scenario_id: int

class RespondRequest(BaseModel):
    conversation: List[ConversationLine]
    scenario_id: int

# === МАРШРУТЫ API ===
@app.get("/api/scenarios")
def get_scenarios():
    return HARDCODED_SCENARIOS

@app.post("/api/respond")
def respond(request: RespondRequest):
    """Генерирует ответ ИИ в середине диалога."""
    scenario = next((s for s in HARDCODED_SCENARIOS if s["id"] == request.scenario_id), None)
    if not scenario:
        raise HTTPException(status_code=404, detail="Scenario not found")

    conversation_history = "\n".join([f"{line.speaker}: {line.text}" for line in request.conversation])
    
    prompt = f"""
    Ты — ИИ-ассистент, играющий роль клиента в симуляции.
    Твоя роль: {scenario['customer_persona']}
    Твоя цель: вести диалог естественно, отвечать на вопросы продавца (User) и иногда выдвигать возражения, соответствующие твоей роли.

    История диалога:
    {conversation_history}
    AI:
    """
    
    # Здесь должен быть реальный вызов OpenAI
    # response = openai.chat.completions.create(...)
    # ai_response = response.choices[0].message.content.strip()
    
    # А пока используем заглушку
    ai_response = "Понятно. И что вы предлагаете?"
    
    return {"ai_response": ai_response}

@app.post("/api/analyze")
def analyze_simulation(request: AnalyzeRequest):
    """Анализирует диалог на основе выбранного сценария."""
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
    return {"message": "API with custom scenarios is running"}
