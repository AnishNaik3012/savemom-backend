
import os
import asyncio
from dotenv import load_dotenv
import google.generativeai as genai

# Load env
load_dotenv(".env.local")

api_key = os.getenv("GEMINI_API_KEY")
print(f"API Key loaded: {api_key[:5]}...{api_key[-5:] if api_key else 'None'}")

if not api_key:
    print("ERROR: No API Key found.")
    exit(1)

genai.configure(api_key=api_key)

async def test_gemini():
    try:
        print("Attempting to connect to Gemini-Flash-Latest...")
        model = genai.GenerativeModel('gemini-flash-latest')
        response = await model.generate_content_async("Hello, can you confirm you are online?")
        print("\nSuccess! Response:")
        print(response.text)
    except Exception as e:
        print(f"\nERROR FAILED: {e}")
        # Try fallback model
        try:
            print("\nRetrying with 'gemini-pro'...")
            model = genai.GenerativeModel('gemini-pro')
            response = await model.generate_content_async("Hello?")
            print("Success with gemini-pro!")
        except Exception as e2:
             print(f"Fallback failed too: {e2}")

if __name__ == "__main__":
    asyncio.run(test_gemini())
