import argparse
import sys
import os
from src.analyzer import PrescriptionAnalyzer

def main():
    parser = argparse.ArgumentParser(description="Prescription Analysis CLI")
    parser.add_argument("--image", type=str, help="Path to prescription image or PDF")
    parser.add_argument("--question", type=str, help="Medical question to ask (optional context from image)")
    
    args = parser.parse_args()
    
    try:
        analyzer = PrescriptionAnalyzer()
    except ValueError as e:
        print(f"Error: {e}")
        print("Please set your GOOGLE_API_KEY in the .env file.")
        return

    context = None
    if args.image:
        print(f"Analyzing {args.image}...")
        try:
            context = analyzer.analyze_prescription(args.image)
            print("\n--- Prescription Data ---")
            print(context.model_dump_json(indent=2))
        except Exception as e:
            print(f"Analysis failed: {e}")

    if args.question:
        print(f"\nQuestion: {args.question}")
        answer = analyzer.ask_medical_question(args.question, context)
        print(f"Answer: {answer}")
    
    if not args.image and not args.question:
        print("Usage: python main.py --image <path> [--question <text>]")
        print("       python main.py --question <text>")

if __name__ == "__main__":
    main()
