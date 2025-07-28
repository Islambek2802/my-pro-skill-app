# backend/main.py (ENGLISH VERSION WITH ANALYSIS)

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List
import openai
import os
import json

# --- Configure OpenAI API Key ---
openai.api_key = os.getenv("OPENAI_API_KEY")

# --- Create the Application ---
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

# --- Hardcoded Scenarios (in English) ---
HARDCODED_SCENARIOS = [
    {
        "id": 1,
        "title": "Handling the Price Objection",
        "goal": "Convince the client that the price is justified and offer a product demonstration.",
        "customer_persona": "A potential client who thinks your product is too expensive compared to competitors.",
    },
    {
        "id": 2,
        "title": "Working with the 'I need to think' Objection",
        "goal": "Acknowledge the client's need to think, uncover the real reason for hesitation, and agree on a clear next step.",
        "customer_persona": "A client who is trying to politely end the conversation by saying they need to think it over.",
    },
    {
        "id": 3,
        "title": "Getting Past the Gatekeeper",
        "goal": "Persuade the secretary or assistant to connect you with the decision-maker.",
        "customer_persona": "An experienced secretary whose job is to filter out unimportant calls.",
    },
]

# --- Data models for request validation ---
class ConversationLine(BaseModel):
    speaker: str
    text: str

class RespondRequest(BaseModel):
    conversation: List[ConversationLine]
    scenario_id: int
    
class AnalyzeRequest(BaseModel):
    conversation: List[ConversationLine]
    scenario_id: int

# === API ROUTES ===

@app.get("/api/scenarios")
def get_scenarios():
    return HARDCODED_SCENARIOS

@app.post("/api/respond")
def respond(request: RespondRequest):
    scenario = next((s for s in HARDCODED_SCENARIOS if s["id"] == request.scenario_id), None)
    if not scenario: raise HTTPException(status_code=404, detail="Scenario not found")

    conversation_history = "\n".join([f"{line.speaker}: {line.text}" for line in request.conversation])
    
    prompt = f"""
    You are an AI assistant playing the role of a customer in a sales simulation.
    Your role: {scenario['customer_persona']}
    Your goal: maintain a natural dialogue, respond to the salesperson's (User) questions.
    Dialogue history:
    {conversation_history}
    AI:
    """
    
    try:
        response = openai.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "system", "content": prompt}],
            temperature=0.7, max_tokens=100
        )
        ai_response = response.choices[0].message.content.strip()
    except Exception as e:
        print(f"OPENAI API ERROR: {e}")
        ai_response = "Sorry, I'm having a technical issue. Could you repeat that?"
    
    return {"ai_response": ai_response}

@app.post("/api/analyze")
def analyze_simulation(request: AnalyzeRequest):
    """Analyzes the dialogue based on the chosen scenario."""
    scenario = next((s for s in HARDCODED_SCENARIOS if s["id"] == request.scenario_id), None)
    if not scenario: raise HTTPException(status_code=404, detail="Scenario not found")

    conversation_history = "\n".join([f"{line.speaker}: {line.text}" for line in request.conversation if line.speaker == 'User'])
    
    prompt = f"""
    You are an expert sales coach. Analyze the performance of the User in the following sales conversation.
    The user's goal was: "{scenario['goal']}"
    
    Here is what the User said during the conversation:
    {conversation_history}
    
    Provide your feedback in a JSON format with the following keys:
    - "goal_achieved": (boolean) Did the user make a clear attempt to achieve their goal?
    - "clarity_score": (integer from 1 to 10) How clear and concise was the user's speech?
    - "persuasion_score": (integer from 1 to 10) How persuasive were the user's arguments?
    - "overall_assessment": (string) A short, constructive feedback paragraph summarizing their performance and giving one key tip for improvement.
    """
    
    try:
        response = openai.chat.completions.create(
            model="gpt-4", # Using a more powerful model for better analysis
            messages=[{"role": "system", "content": prompt}]
        )
        feedback_str = response.choices[0].message.content
        feedback_json = json.loads(feedback_str)
        return feedback_json
    except Exception as e:
        print(f"OPENAI ANALYSIS ERROR: {e}")
        raise HTTPException(status_code=500, detail="Failed to get analysis from AI")


@app.get("/")
def read_root():
    return {"message": "Optimized English API with Analysis is running"}
