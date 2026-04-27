import asyncio
import os
from dotenv import load_dotenv
from chatbot_system.report_analyzer import summarize_report_rule_based, analyze_report_with_ai

# Load env
load_dotenv(".env.local")

async def test_wellness_insights():
    print("--- Testing Wellness Insights (Rule-based Fallback) ---")
    # Test Ultrasound fallback
    result_us = summarize_report_rule_based("This is an ultrasound scan notice.", "image/jpeg")
    print(f"Report Title: {result_us['report_title']}")
    print(f"Wellness Score: {result_us.get('wellness_score', 'MISSING')}")
    print(f"Metric Comparisons: {result_us.get('metric_comparisons', 'MISSING')}")
    assert "wellness_score" in result_us
    assert "metric_comparisons" in result_us

    # Test Hemoglobin fallback
    result_hb = summarize_report_rule_based("Hemoglobin level is 11.2 g/dL", "application/pdf")
    print(f"\nReport Title: {result_hb['report_title']}")
    print(f"Wellness Score: {result_hb.get('wellness_score', 'MISSING')}")
    print(f"Metric Comparisons: {result_hb.get('metric_comparisons', 'MISSING')}")
    assert "wellness_score" in result_hb
    assert "metric_comparisons" in result_hb
    assert len(result_hb["metric_comparisons"]) > 0


    print("\n--- Testing Wellness Insights (AI Analysis - requires API Key) ---")
    api_key = os.getenv("GEMINI_API_KEY")
    if api_key:
        # Mock file content
        dummy_content = b"Mock report content"
        try:
            result_ai = await analyze_report_with_ai(dummy_content, "application/pdf")
            print(f"AI Report Title: {result_ai['report_title']}")
            print(f"AI Wellness Insights: {result_ai.get('wellness_insights', 'MISSING')}")
            # Note: Depending on AI response, it might be empty if AI failed, 
            # but our code ensures a default [] or fallback.
        except Exception as e:
            print(f"AI Analysis failed (expected if no real file): {e}")
    else:
        print("Skipping AI test - No GEMINI_API_KEY found.")

    print("\nVerification Complete!")

if __name__ == "__main__":
    asyncio.run(test_wellness_insights())
