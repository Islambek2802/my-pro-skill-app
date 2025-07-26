# backend/main.py (ВЕРСИЯ С РАСШИРЕННЫМИ СЦЕНАРИЯМИ)

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

# --- Вшитые сценарии (РАСШИРЕННЫЙ СПИСОК) ---
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
    },
    {
        "id": 3,
        "title": "Проход через 'привратника' (секретаря)",
        "goal": "Убедить секретаря соединить вас с лицом, принимающим решения (ЛПР), не раскрывая всех деталей.",
        "customer_persona": "Опытный секретарь, чья работа — отфильтровывать неважные звонки.",
        "required_keywords": ["помощь", "рекомендация", "важный вопрос"]
    },
    {
        "id": 4,
        "title": "Мы уже работаем с конкурентами",
        "goal": "Выяснить недостатки текущего решения клиента и предложить ваше как лучшую альтернативу.",
        "customer_persona": "В целом довольный клиент вашего конкурента, но открытый к новым идеям.",
        "required_keywords": ["сравнение", "улучшить", "альтернатива"]
    },
    {
        "id": 5,
        "title": "Звонок от рассерженного клиента",
        "goal": "Успокоить клиента, решить его проблему и сохранить лояльность к компании.",
        "customer_persona": "Давний клиент, у которого возникла серьезная техническая проблема, и он очень недоволен.",
        "required_keywords": ["сожалею", "решить проблему", "компенсация"]
    },
    {
        "id": 6,
        "title": "Клиент просит большую скидку",
        "goal": "Обосновать ценность продукта, чтобы избежать скидки, или предложить неденежный бонус.",
        "customer_persona": "Клиент, который готов купить, но пытается получить максимально возможную скидку.",
        "required_keywords": ["инвестиция", "полная стоимость", "дополнительная ценность"]
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
    Твоя цель: вести диалог естественно, отвечать на вопросы продавца (User) и иногда выдвигать возражения.

    История диалога:
    {conversation_history}
    AI:
    """
    
    # Здесь должен быть реальный вызов OpenAI
    # response = openai.chat.completions.create(...)
    # ai_response = response.choices[0].message.content.strip()
    
    # А пока используем заглушку
    ai_response = "Хорошо, я вас понял. Что вы можете предложить?"
    
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
    return {"message": "Simplified API with extended scenarios is running"}
