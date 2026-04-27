import os
from google import genai
from dotenv import load_dotenv

load_dotenv()

api_key = os.getenv("GOOGLE_API_KEY")
if not api_key:
    print("Error: GOOGLE_API_KEY not found in .env")
    exit(1)

try:
    client = genai.Client(api_key=api_key)
    print("Listing available models...")
    # The new SDK might have a different way to list models, checking documentation pattern
    # Usually it's client.models.list()
    for model in client.models.list():
        print(f"Model: {model.name}")
        print(f"  Supported generation methods: {model.supported_generation_methods}")
        
except Exception as e:
    print(f"Error listing models: {e}")
