# backend/main.py

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

import os
import openai
import json
from fastapi import FastAPI, Depends, HTTPException, APIRouter, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from typing import List

from . import auth, crud, models, schemas
from .database import SessionLocal, engine

models.Base.metadata.create_all(bind=engine)
openai.api_key = os.getenv("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")

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

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# === АУТЕНТИФИКАЦИЯ ===
auth_router = APIRouter()

@auth_router.post("/register", status_code=status.HTTP_201_CREATED)
def register_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    if crud.get_user_by_username(db, username=user.username):
        raise HTTPException(status_code=400, detail="Username already registered")
    crud.create_user(db=db, user=user)
    return {"message": "User created successfully"}

@auth_router.post("/token", response_model=schemas.Token)
def login(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user = crud.get_user_by_username(db, username=form_data.username)
    if not user or not auth.verify_password(form_data.password, user.hashed_password):
        raise HTTPException(status_code=401, detail="Incorrect username or password")
    token = auth.create_access_token(data={"sub": user.username, "user_id": user.id})
    return {"access_token": token, "token_type": "bearer"}

# === АДМИН-ПАНЕЛЬ: УПРАВЛЕНИЕ СЦЕНАРИЯМИ ===
admin_router = APIRouter()

@admin_router.post("/scenarios", response_model=schemas.Scenario)
def handle_create_scenario(scenario: schemas.ScenarioCreate, db: Session = Depends(get_db), u: dict = Depends(auth.get_current_user)):
    return crud.create_scenario(db=db, scenario=scenario)

@admin_router.get("/scenarios", response_model=List[schemas.Scenario])
def handle_get_scenarios(db: Session = Depends(get_db), u: dict = Depends(auth.get_current_user)):
    return crud.get_scenarios(db=db)

# === ОСНОВНОЕ ПРИЛОЖЕНИЕ: СИМУЛЯЦИЯ ===
app_router = APIRouter()

@app_router.post("/simulation/analyze")
def analyze_simulation(request: schemas.AnalyzeRequest, db: Session = Depends(get_db), current_user: dict = Depends(auth.get_current_user)):
    scenario = crud.get_scenario(db, scenario_id=request.scenario_id)
    if not scenario:
        raise HTTPException(status_code=404, detail="Scenario not found")
    
    conversation_log = "\n".join([f"{line.speaker}: {line.text}" for line in request.conversation])
    prompt = f"""
    Analyze a sales call based on a scenario.
    - Scenario Goal: {scenario.goal}
    - Required Keywords: {', '.join(scenario.required_keywords)}
    - Conversation: {conversation_log}
    Provide feedback as a JSON with keys: "goal_achieved" (boolean), "keywords_usage" (list of used keywords), "feedback_on_goal" (string), "overall_assessment" (string).
    """
    # Здесь должен быть реальный вызов OpenAI
    # response = openai.chat.completions.create(...)
    # feedback_json = json.loads(response.choices[0].message.content)
    # А пока используем заглушку:
    feedback_json = {
        "goal_achieved": True,
        "keywords_usage": scenario.required_keywords[:1],
        "feedback_on_goal": "Вы уверенно вели клиента к цели.",
        "overall_assessment": "Отличная работа! Попробуйте быть немного настойчивее в следующий раз."
    }
    user_id = current_user.get("user_id")
    crud.create_simulation_log(db, user_id, request.scenario_id, request.conversation, feedback_json)
    return feedback_json

@app_router.get("/simulation/scenarios", response_model=List[schemas.Scenario])
def get_simulation_scenarios(db: Session = Depends(get_db), u: dict = Depends(auth.get_current_user)):
    return crud.get_scenarios(db=db)

# --- Подключаем все роутеры ---
app.include_router(auth_router, prefix="/api/auth", tags=["Auth"])
app.include_router(admin_router, prefix="/api/admin", tags=["Admin"])
app.include_router(app_router, prefix="/api/app", tags=["App"])
