# import openai
# from fastapi import FastAPI
# from pydantic import BaseModel
# from fastapi.middleware.cors import CORSMiddleware
# import os

# # TEMP: Hardcoded API key for local testing
# openai.api_key = "Jma4FpgT3BlbkFJdQzBLVnDw9uVX1r1-OCqGREjQ78982v84cliq_LZ1vIcejhVvGO7AEtIgmAH3HSd8cWNw11h4A"

# app = FastAPI()

# app.add_middleware(
#     CORSMiddleware,
#     allow_origins=["*"],
#     allow_credentials=True,
#     allow_methods=["*"],
#     allow_headers=["*"],
# )

# class Question(BaseModel):
#     query: str

# @app.post("/ask")
# def ask_question(q: Question):
#     prompt = f"""
#     You are Mana Dosth 🧑🏻‍🤝‍🧑🏻 – a friendly multilingual assistant.
#     Respond like a local native from user's region.
#     Question: "{q.query}"
#     Reply in the same language in a warm, natural tone.
#     """

#     try:
#         response = openai.ChatCompletion.create(
#             model="gpt-3.5-turbo",
#             messages=[
#                 {"role": "system", "content": "You are a helpful and native-sounding assistant."},
#                 {"role": "user", "content": prompt}
#             ],
#             temperature=0.7
#         )
#         answer = response.choices[0].message.content.strip()
#         return {"answer": answer}

#     except Exception as e:
#         print("❌ ERROR contacting AI service:", str(e))  # 👈 SHOW FULL ERROR
#         return {"answer": f"❌ Error contacting AI service: {str(e)}"}  # Return error in response


from fastapi import FastAPI
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

# Enable CORS for frontend communication
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # You can restrict to frontend URL later
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Request body model
class Question(BaseModel):
    query: str

# Chat route — no OpenAI, just local response logic
@app.post("/ask")
def ask_question(q: Question):
    query = q.query.lower()

    # Sample multilingual friendly replies
    if "telugu" in query or "తెలుగు" in query:
        return {"answer": "అన్నా! మీకు ఏమయింది? చెబు నేను ఉన్నాను."}
    elif "hindi" in query or "हिंदी" in query:
        return {"answer": "भाई! कैसे हो? मैं यहाँ हूँ, बताओ।"}
    elif "tamil" in query or "தமிழ்" in query:
        return {"answer": "அண்ணா! எப்படி இருக்கிறீர்கள்? என்ன உதவி வேண்டும்?"}
    elif "kannada" in query or "ಕನ್ನಡ" in query:
        return {"answer": "ಅಣ್ಣಾ! ಹೇಗಿದ್ದೀಯ? ನಾನಿಲ್ಲಿ ಇದ್ದೀನಿ."}
    elif "dosth" in query or "anna" in query:
        return {"answer": "అన్నా నేనొక్కడినే ఉన్నాను! చెప్పు ఏం కావాలి?"}
    elif "hello" in query or "hi" in query:
        return {"answer": "Hi dosth! ఎలా ఉన్నావు?"}
    else:
        return {"answer": "😄 Dosth is thinking... tell me more clearly!"}

