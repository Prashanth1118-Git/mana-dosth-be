from fastapi import FastAPI
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

# CORS setup to allow frontend calls
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # or replace * with your Vercel domain for security
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class Question(BaseModel):
    query: str

@app.post("/ask")
def ask_question(q: Question):
    # Replace this dummy logic with your model call
    user_input = q.query

    # Example model response (for now)
    response = f"Meeku telisina samadhanam: '{user_input}' ane prashnaku work chestondi."

    return {"answer": response}
