# backend/main.py (МАКСИМАЛЬНО ОПТИМИЗИРОВАННАЯ ВЕРСИЯ)

# --- Импортируем только самое необходимое ---
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List
import openai
import os

# --- Настройка OpenAI API ключа ---
# (Сервер возьмет его из переменных окружения, которые вы задали на хостинге)
openai.api_key = os.getenv("OPENAI_API_KEY")

# --- Создание приложения ---
app = FastAPI()

# --- CORS ---
# Разрешаем всем сайтам обращаться к нашему API для простоты
origins = ["*"]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# --- Вшитые сценарии (наши данные) ---
HARDCODED_SCENARIOS = [
    {
        "id": 1,
        "title": "Квалификация клиента (BANT)",
        "goal": "Определить, подходит ли клиент, задавая вопросы о его Бюджете, Полномочиях, Потребностях и Сроках.",
        "customer_persona": "Потенциальный клиент, оставивший заявку. Он кажется заинтересованным, но может не иметь полномочий для принятия решения или четкого бюджета.",
    },
    {
        "id": 2,
        "title": "Работа с возражением 'Нет времени'",
        "goal": "Признать занятость клиента, быстро донести ценность и договориться о коротком конкретном следующем шаге.",
        "customer_persona": "Очень занятой руководитель, который пытается вежливо закончить разговор, ссылаясь на нехватку времени.",
    },
    {
        "id": 3,
        "title": "Работа с возражением 'Дорого'",
        "goal": "Не снижая цену, сместить фокус с цены на ценность и окупаемость (ROI).",
        "customer_persona": "Клиент, который сравнивает ваше предложение с более дешевыми аналогами и сфокусирован только на стоимости.",
    },
]

# --- Модели данных для проверки входящих запросов ---
class ConversationLine(BaseModel):
    speaker: str
    text: str

class RespondRequest(BaseModel):
    conversation: List[ConversationLine]
    scenario_id: int

# === МАРШРУТЫ API (точки входа в наше приложение) ===

@app.get("/api/scenarios")
def get_scenarios():
    """Отдает список готовых сценариев."""
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
    Твоя цель: вести диалог естественно, отвечать на вопросы продавца (User).

    История диалога:
    {conversation_history}
    AI:
    """
    
    # --- Вызов OpenAI ---
    # Если ключ OpenAI не задан или неверный, этот блок вызовет ошибку в логах.
    # Но само приложение не должно "упасть" из-за этого.
    try:
        response = openai.chat.completions.create(
            model="gpt-3.5-turbo", # Используем быструю и дешевую модель
            messages=[{"role": "system", "content": prompt}],
            temperature=0.7,
            max_tokens=100
        )
        ai_response = response.choices[0].message.content.strip()
    except Exception as e:
        print(f"ОШИБКА ВЫЗОВА OpenAI: {e}")
        ai_response = "Извините, у меня технические неполадки. Можете повторить?"
    
    return {"ai_response": ai_response}

@app.get("/")
def read_root():
    return {"message": "Optimized API is running"}
