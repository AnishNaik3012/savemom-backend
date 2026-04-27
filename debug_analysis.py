
import asyncio
import os
from chatbot_system.report_analyzer import analyze_report_with_ai
from dotenv import load_dotenv

load_dotenv(".env.local")

async def test():
    # Mock some ultrasound text
    text = "Obstetric Ultrasound. Fetal Heart Rate 141 bpm. Normal amniotic fluid. Single live fetus."
    # We'll just test the fallback/parsing logic by mocking a response or using the real one if API key exists
    print("Testing analyze_report_with_ai with mock text...")
    
    # Since we can't easily mock the AI response here without monkeypatching, 
    # let's just test the return of the function with a dummy file
    # and see if it has our new keys.
    
    result = await analyze_report_with_ai(b"dummy content", "image/jpeg")
    print(f"Keys in result: {result.keys()}")
    print(f"Wellness Score: {result.get('wellness_score')}")
    print(f"Metric Comparisons: {result.get('metric_comparisons')}")
    print(f"Wellness Insights: {result.get('wellness_insights')}")

if __name__ == "__main__":
    asyncio.run(test())
