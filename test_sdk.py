import os
from google import genai
from dotenv import load_dotenv

load_dotenv(".env.local")
load_dotenv(".env")

def test_sdk():
    api_key = os.getenv("GEMINI_API_KEY") or os.getenv("GOOGLE_API_KEY")
    if not api_key:
        print("API Key not found!")
        return

    print(f"Testing Gemini SDK with key: {api_key[:10]}...")
    
    try:
        client = genai.Client(api_key=api_key)
        print("Calling gemini-flash-latest...")
        response = client.models.generate_content(
            model='gemini-flash-latest',
            contents=['Say "SDK Test Success"']
        )
        print(f"Success! Response: {response.text}")
    except Exception as e:
        print(f"Failed with error type: {type(e)}")
        print(f"Error message: {e}")

if __name__ == "__main__":
    test_sdk()
