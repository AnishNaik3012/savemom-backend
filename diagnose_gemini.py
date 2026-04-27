import os
import sys
from dotenv import load_dotenv

# Add module to path
current_dir = os.path.dirname(os.path.abspath(__file__))
presc_path = os.path.join(current_dir, "presc_hybrid/presc_hybrid")
if presc_path not in sys.path:
    sys.path.append(presc_path)

load_dotenv()

from src.analyzer import PrescriptionAnalyzer
import traceback

def diagnostic():
    print(f"Testing with API Key: {os.getenv('GOOGLE_API_KEY')[:10]}...")
    try:
        analyzer = PrescriptionAnalyzer()
        # Test with a dummy prompt (no image needed to test key/model/rate limit basics)
        print("Initial testing generating text...")
        # We'll bypass analyze_prescription and call the internal retry helper
        try:
            res = analyzer._generate_with_retry(
                model='gemini-1.5-flash',
                contents=["Hi, say test."]
            )
            print(f"Success! Response: {res.text}")
        except Exception as e:
            print("Direct call failed!")
            traceback.print_exc()
            
    except Exception as e:
        print(f"Initialization failed: {e}")
        traceback.print_exc()

if __name__ == "__main__":
    diagnostic()
