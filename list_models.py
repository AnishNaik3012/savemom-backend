import os
from google import genai
from dotenv import load_dotenv

load_dotenv(".env.local")
load_dotenv(".env")

def list_models():
    api_key = os.getenv("GEMINI_API_KEY") or os.getenv("GOOGLE_API_KEY")
    client = genai.Client(api_key=api_key)
    
    print("Listing models...")
    try:
        models = client.models.list()
        for model in models:
             print(f"- {model.name}")
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    list_models()
