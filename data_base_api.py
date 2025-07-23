from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field
from typing import List, Optional
import json
import os

app = FastAPI(title="HR Bot Candidate Database API")

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATABASE_FILE = os.path.join(BASE_DIR, "candidates.json")

# --------- Models ----------
class Candidate(BaseModel):
    id: int
    name: str
    skills: List[str]
    experience_years: int = Field(ge=0)
    projects: List[str]
    availability: str

# --------- Utility Functions ----------
def load_data():
    if not os.path.exists(DATABASE_FILE):
        return {"employees": []}
    with open(DATABASE_FILE, "r") as f:
        return json.load(f)

def save_data(data):
    with open(DATABASE_FILE, "w") as f:
        json.dump(data, f, indent=2)

# --------- Endpoints ----------

@app.get("/candidates", response_model=List[Candidate])
def get_candidates():
    data = load_data()
    return data["employees"]

@app.post("/candidates", response_model=Candidate)
def add_candidate(candidate: Candidate):
    data = load_data()
    for emp in data["employees"]:
        if emp["id"] == candidate.id:
            raise HTTPException(status_code=400, detail="Candidate with this ID already exists.")
    data["employees"].append(candidate.dict())
    save_data(data)
    return candidate

@app.put("/candidates/{candidate_id}", response_model=Candidate)
def update_candidate(candidate_id: int, candidate: Candidate):
    data = load_data()
    for idx, emp in enumerate(data["employees"]):
        if emp["id"] == candidate_id:
            data["employees"][idx] = candidate.dict()
            save_data(data)
            return candidate
    raise HTTPException(status_code=404, detail="Candidate not found.")

