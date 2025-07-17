# backend/crud.py

from sqlalchemy.orm import Session
from . import models, schemas, auth

# --- Пользователи ---
def get_user_by_username(db: Session, username: str):
    return db.query(models.User).filter(models.User.username == username).first()

def create_user(db: Session, user: schemas.UserCreate):
    hashed_password = auth.get_password_hash(user.password)
    db_user = models.User(username=user.username, hashed_password=hashed_password)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

# --- Сценарии ---
def create_scenario(db: Session, scenario: schemas.ScenarioCreate):
    db_scenario = models.Scenario(**scenario.dict())
    db.add(db_scenario)
    db.commit()
    db.refresh(db_scenario)
    return db_scenario

def get_scenarios(db: Session):
    return db.query(models.Scenario).all()

def get_scenario(db: Session, scenario_id: int):
    return db.query(models.Scenario).filter(models.Scenario.id == scenario_id).first()

# --- Журнал Симуляций ---
def create_simulation_log(db: Session, user_id: int, scenario_id: int, conversation: list, feedback: dict):
    db_log = models.SimulationLog(
        user_id=user_id,
        scenario_id=scenario_id,
        conversation_history=[line.dict() for line in conversation],
        feedback=feedback
    )
    db.add(db_log)
    db.commit()
    db.refresh(db_log)
    return db_log
