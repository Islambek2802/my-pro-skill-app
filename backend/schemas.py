# backend/schemas.py

from pydantic import BaseModel
from typing import List, Optional

# --- Пользователи и Токены ---
class UserCreate(BaseModel):
    username: str
    password: str

class Token(BaseModel):
    access_token: str
    token_type: str

# --- Сценарии ---
class ScenarioCreate(BaseModel):
    title: str
    goal: str
    customer_persona: str
    required_keywords: List[str]

class Scenario(ScenarioCreate):
    id: int
    class Config:
        orm_mode = True

# --- Симуляция и Аналитика ---
class ConversationLine(BaseModel):
    speaker: str
    text: str

class AnalyzeRequest(BaseModel):
    conversation: List[ConversationLine]
    scenario_id: int
