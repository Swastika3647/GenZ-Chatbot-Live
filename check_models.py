import google.generativeai as genai
import os

# --- SAFE WAY: LOAD FROM ENVIRONMENT ---
# On Mac/Linux terminal, run this before the script: 
# export GEMINI_API_KEY="your_new_key_here"
api_key = os.getenv("GEMINI_API_KEY")

if not api_key:
    print("❌ Error: GEMINI_API_KEY not found in environment variables.")
else:
    genai.configure(api_key=api_key)
    print("Available models:")
    try:
        for m in genai.list_models():
            if 'generateContent' in m.supported_generation_methods:
                print(f" - {m.name}")
    except Exception as e:
        print(f"Error listing models: {e}")