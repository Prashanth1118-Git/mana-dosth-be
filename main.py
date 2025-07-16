from fastapi import FastAPI
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware
import os
import requests
import json

# 1. API కీని సురక్షితంగా లోడ్ చేయండి
# ఇది ఎన్విరాన్‌మెంట్ వేరియబుల్ 'GEMINI_API_KEY' నుండి కీని లోడ్ చేయడానికి ప్రయత్నిస్తుంది.
# ఒకవేళ ఎన్విరాన్‌మెంట్ వేరియబుల్ సెట్ చేయకపోతే, అది "YOUR_GEMINI_API_KEY" అనే డమ్మీ విలువను ఉపయోగిస్తుంది.
# మీరు మీ నిజమైన API కీని ఎన్విరాన్‌మెంట్ వేరియబుల్‌గా సెట్ చేయాలి.
# మీ ఎర్రర్ మెసేజ్‌లో చూపిన కీ 'AIzaSyA8M_CneC41bskoCqvoBE6ck6C6GGjVCjs' అనేది ఒక ప్లేస్‌హోల్డర్ కీ.
# దయచేసి దీన్ని మీ నిజమైన, పని చేసే API కీతో భర్తీ చేయండి.
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY", "YOUR_GEMINI_API_KEY")

# API కీ సరిగ్గా సెట్ చేయబడిందో లేదో తనిఖీ చేయండి
if GEMINI_API_KEY == "YOUR_GEMINI_API_KEY" or not GEMINI_API_KEY:
    print("WARNING: GEMINI_API_KEY environment variable is not set or is using the default placeholder.")
    print("Please set your actual Gemini API key as an environment variable for production use.")
    print("Example (Linux/macOS): export GEMINI_API_KEY='YOUR_ACTUAL_API_KEY'")
    print("Example (Windows CMD): set GEMINI_API_KEY=YOUR_ACTUAL_API_KEY")
    print("Example (Windows PowerShell): $env:GEMINI_API_KEY='YOUR_ACTUAL_API_KEY'")


app = FastAPI()

# CORS (Cross-Origin Resource Sharing) సెట్టింగ్‌లు
# ఇది మీ ఫ్రంటెండ్ అప్లికేషన్ వేరే డొమైన్ నుండి ఈ APIని కాల్ చేయడానికి అనుమతిస్తుంది.
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # అన్ని మూలాల నుండి అభ్యర్థనలను అనుమతిస్తుంది. నిర్దిష్ట డొమైన్‌లను ఇవ్వడం మంచిది.
    allow_credentials=True,
    allow_methods=["*"],  # అన్ని HTTP పద్ధతులను (GET, POST, PUT, DELETE, etc.) అనుమతిస్తుంది.
    allow_headers=["*"],  # అన్ని హెడర్‌లను అనుమతిస్తుంది.
)

# అభ్యర్థన బాడీ కోసం Pydantic మోడల్
# ఇది ఇన్కమింగ్ JSON డేటాను ధృవీకరించడానికి FastAPIకి సహాయపడుతుంది.
class Question(BaseModel):
    query: str

# POST ఎండ్‌పాయింట్: /ask
# ఈ ఎండ్‌పాయింట్ ఒక ప్రశ్నను అంగీకరించి, జెమిని AIని ఉపయోగించి దానికి సమాధానం ఇస్తుంది.
@app.post("/ask")
def ask_question(q: Question):
    # డీబగ్గింగ్ కోసం: అప్లికేషన్ ఏ కీని ఉపయోగిస్తుందో ప్రింట్ చేయండి
    # పూర్తి కీని ప్రింట్ చేయకుండా, దాని మొదటి మరియు చివరి కొన్ని అక్షరాలను మాత్రమే చూపిస్తుంది.
    if GEMINI_API_KEY and len(GEMINI_API_KEY) > 10:
        print(f"DEBUG: Using API Key (partial): {GEMINI_API_KEY[:5]}...{GEMINI_API_KEY[-5:]}")
    else:
        print(f"DEBUG: Using API Key (full): {GEMINI_API_KEY}") # కీ చాలా చిన్నదైతే మొత్తం ప్రింట్ చేయండి

    # జెమిని API ఎండ్‌పాయింట్ URL
    # మోడల్ పేరు 'gemini-pro' మరియు మీ API కీని URL పారామీటర్‌గా ఉపయోగిస్తుంది.
    # API వెర్షన్ v1beta అని నిర్ధారించుకోండి.
    # మోడల్ పేరును 'gemini-pro' నుండి 'gemini-1.0-pro'కి మార్చబడింది.
    url = f"https://generativelanguage.googleapis.com/v1beta/models/gemma-3n-e2b-it:generateContent?key={GEMINI_API_KEY}"
    print(f"DEBUG: Calling URL: {url}") # డీబగ్గింగ్ కోసం: కాల్ చేస్తున్న URLని ప్రింట్ చేయండి
    
    # అభ్యర్థన హెడర్‌లు
    headers = {"Content-Type": "application/json"}
    
    # అభ్యర్థన బాడీ (జెమిని API ఆశించిన ఫార్మాట్‌లో)
    body = {
        "contents": [
            {
                "parts": [{"text": q.query}]
            }
        ]
    }

    try:
        # జెమిని APIకి POST అభ్యర్థనను పంపండి
        res = requests.post(url, headers=headers, data=json.dumps(body))
        
        # HTTP లోపాల కోసం తనిఖీ చేయండి (ఉదా: 4xx లేదా 5xx స్టేటస్ కోడ్‌లు)
        res.raise_for_status() 
        
        # JSON ప్రతిస్పందనను పార్స్ చేయండి
        data = res.json()
        
        # జెమిని ప్రతిస్పందన నుండి టెక్స్ట్ కంటెంట్‌ను సంగ్రహించండి
        # ప్రతిస్పందన నిర్మాణం అంచనా వేసిన విధంగా లేకపోతే లోపాలను నివారించడానికి తనిఖీలు జోడించబడతాయి.
        reply = "No answer found." # డిఫాల్ట్ ప్రతిస్పందన
        if "candidates" in data and len(data["candidates"]) > 0:
            if "content" in data["candidates"][0] and "parts" in data["candidates"][0]["content"] and len(data["candidates"][0]["content"]["parts"]) > 0:
                if "text" in data["candidates"][0]["content"]["parts"][0]:
                    reply = data["candidates"][0]["content"]["parts"][0]["text"]
        
        # విజయవంతమైన ప్రతిస్పందనను తిరిగి ఇవ్వండి
        return {"answer": reply}
    
    except requests.exceptions.RequestException as e:
        # నెట్‌వర్క్-సంబంధిత లేదా HTTP లోపాలను నిర్వహించండి
        print(f"❌ Gemini API Request Error: {e}")
        # API ప్రతిస్పందనను లోప సందేశంలో చేర్చండి, అది అందుబాటులో ఉంటే
        if hasattr(e, 'response') and e.response is not None:
            print(f"API Response Content: {e.response.text}")
            return {"answer": f"❌ Gemini API Request Error: {str(e)}. API Response: {e.response.text}"}
        return {"answer": f"❌ Gemini API Request Error: {str(e)}"}
    except KeyError as e:
        # జెమిని ప్రతిస్పందన నిర్మాణం ఊహించని విధంగా ఉన్నప్పుడు లోపాలను నిర్వహించండి
        print(f"❌ Error parsing Gemini response: Missing key {e}. Response: {data}")
        return {"answer": f"❌ Error parsing Gemini response: Unexpected structure. Details: {str(e)}"}
    except Exception as e:
        # ఏదైనా ఇతర ఊహించని లోపాలను నిర్వహించండి
        print(f"❌ An unexpected error occurred: {e}")
        return {"answer": f"❌ An unexpected error occurred: {str(e)}"}

