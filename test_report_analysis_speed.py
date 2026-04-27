
import asyncio
import time
import unittest
from unittest.mock import MagicMock, patch
import os
import sys

# Add the parent directory to sys.path
current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir)
sys.path.insert(0, parent_dir)
sys.path.insert(0, current_dir)

from chatbot_system.report_analyzer import analyze_report_with_ai

class TestReportAnalysisSpeed(unittest.IsolatedAsyncioTestCase):
    async def test_parallel_execution_medical(self):
        print("\nRunning Parallel Execution Test (Medical)...")
        AI_DELAY = 1.0
        IMG_DELAY = 0.5
        
        mock_response = MagicMock()
        mock_response.text = '{"is_medical": true, "summary": "Medical Summary"}'
        
        async def mock_generate_content_async(*args, **kwargs):
            await asyncio.sleep(AI_DELAY)
            return mock_response
            
        def mock_convert_to_image(*args, **kwargs):
            time.sleep(IMG_DELAY)
            return b"fake_image_bytes"

        with patch('google.generativeai.GenerativeModel') as MockModel:
            instance = MockModel.return_value
            instance.generate_content_async.side_effect = mock_generate_content_async
            
            with patch('chatbot_system.report_analyzer.convert_pdf_to_image', side_effect=mock_convert_to_image):
                with patch.dict(os.environ, {"GEMINI_API_KEY": "fake_key"}):
                    start_time = time.time()
                    result = await analyze_report_with_ai(b"%PDF-...", "application/pdf")
                    duration = time.time() - start_time
                    
                    print(f"  Duration: {duration:.4f}s (Expected ~{max(AI_DELAY, IMG_DELAY)}s)")
                    self.assertLess(duration, AI_DELAY + IMG_DELAY - 0.2)
                    self.assertTrue(result.get("is_medical"))

    async def test_non_medical_rejection(self):
        print("\nRunning Non-Medical Rejection Test...")
        AI_DELAY = 0.1
        
        mock_response = MagicMock()
        mock_response.text = '{"is_medical": false, "error_message": "Not medical"}'
        
        async def mock_generate_content_async(*args, **kwargs):
            await asyncio.sleep(AI_DELAY)
            return mock_response
            
        with patch('google.generativeai.GenerativeModel') as MockModel:
            instance = MockModel.return_value
            instance.generate_content_async.side_effect = mock_generate_content_async
            
            # We don't care about image conversion speed here, just result
            with patch('chatbot_system.report_analyzer.convert_pdf_to_image', return_value=b""):
                with patch.dict(os.environ, {"GEMINI_API_KEY": "fake_key"}):
                    result = await analyze_report_with_ai(b"non_medical_data", "application/pdf")
                    
                    print(f"  Result: {result}")
                    self.assertFalse(result.get("is_medical"))
                    self.assertIn("error_message", result)

if __name__ == "__main__":
    unittest.main()
