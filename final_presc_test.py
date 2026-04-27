import os
import sys
from dotenv import load_dotenv

# Add module to path
current_dir = os.path.dirname(os.path.abspath(__file__))
presc_path = os.path.join(current_dir, "presc_hybrid/presc_hybrid")
if presc_path not in sys.path:
    sys.path.append(presc_path)

# Force load from root .env.local for standard testing
load_dotenv(".env.local")

from src.analyzer import PrescriptionAnalyzer
import json

def final_test():
    print("Starting final end-to-end test...")
    try:
        analyzer = PrescriptionAnalyzer()
        image_path = os.path.join(presc_path, "sample_prescription.jpg")
        
        if not os.path.exists(image_path):
            print(f"Error: Sample image not found at {image_path}")
            return

        print(f"Analyzing {image_path}...")
        result = analyzer.analyze_prescription(image_path)
        
        print("\n--- ANALYSIS RESULT ---")
        print(json.dumps(result.model_dump(), indent=2))
        print("------------------------\n")
        
        if result.doctor_name or result.medications:
            print("SUCCESS: Data extracted correctly!")
        else:
            print("WARNING: Extraction returned empty or 'Not found' values, but call succeeded.")

    except Exception as e:
        print(f"FINAL TEST FAILED: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    final_test()
