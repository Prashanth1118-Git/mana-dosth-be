import google.generativeai as genai
import os

# మీ API కీని ఎన్విరాన్‌మెంట్ వేరియబుల్ నుండి లోడ్ చేయండి
# మీరు ఈ స్క్రిప్ట్‌ను రన్ చేసే ముందు మీ టెర్మినల్‌లో GEMINI_API_KEYని సెట్ చేశారని నిర్ధారించుకోండి.
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

if not GEMINI_API_KEY:
    print("Error: GEMINI_API_KEY environment variable is not set.")
    print("Please set it using: export GEMINI_API_KEY='YOUR_ACTUAL_API_KEY' (Linux/macOS) or set GEMINI_API_KEY=YOUR_ACTUAL_API_KEY (Windows)")
    exit()

try:
    genai.configure(api_key=GEMINI_API_KEY)
except Exception as e:
    print(f"Error configuring API key: {e}")
    print("Please ensure your API key is valid and correctly formatted.")
    exit()

print("Fetching available Gemini models...")

try:
    # అందుబాటులో ఉన్న మోడల్‌లను జాబితా చేయండి
    # generateContent పద్ధతికి మద్దతు ఇచ్చే మోడల్‌లను మాత్రమే ఫిల్టర్ చేయండి
    for m in genai.list_models():
        if "generateContent" in m.supported_generation_methods:
            print(f"Model Name: {m.name}, Supported Methods: {m.supported_generation_methods}")
except Exception as e:
    print(f"An error occurred while listing models: {e}")
    print("Please check your internet connection and API key permissions.")

