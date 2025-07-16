import openai
from fastapi import FastAPI
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware
import os

openai.api_key = os.getenv("OPENAI_API_KEY")  # Add to Render env

app = FastAPI()

# CORS for frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class Question(BaseModel):
    query: str

@app.post("/ask")
def ask_question(q: Question):
    prompt = f"""
    You are Mana Dosth 🧑🏻‍🤝‍🧑🏻 – a friendly multilingual assistant.
    Respond like a local native from user's region.
    Question: "{q.query}"
    Reply in the same language in a warm, natural tone.
    """

    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",  # or gpt-4
            messages=[
                {"role": "system", "content": "You are a helpful and native-sounding assistant."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.7
        )

        answer = response.choices[0].message.content.strip()
        return {"answer": answer}

    except Exception as e:
        return {"answer": "❌ Error contacting AI service."}
