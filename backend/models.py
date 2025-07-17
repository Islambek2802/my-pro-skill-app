# backend/models.py

from sqlalchemy import Column, Integer, String, Text, JSON, ForeignKey
from sqlalchemy.orm import relationship
from .database import Base

class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True)
    hashed_password = Column(String)
    logs = relationship("SimulationLog", back_populates="user")

class Scenario(Base):
    __tablename__ = "scenarios"
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True)
    goal = Column(Text)
    customer_persona = Column(Text)
    required_keywords = Column(JSON)

class SimulationLog(Base):
    __tablename__ = "simulation_logs"
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    scenario_id = Column(Integer, ForeignKey("scenarios.id"))
    conversation_history = Column(JSON)
    feedback = Column(JSON)
    user = relationship("User", back_populates="logs")
