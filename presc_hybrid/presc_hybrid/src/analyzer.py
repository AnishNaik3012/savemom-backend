import os
import json
import time
import google.generativeai as genai
from PIL import Image
from dotenv import load_dotenv
from tenacity import retry, stop_after_attempt, wait_exponential, retry_if_exception_type, RetryError
from .models import PrescriptionData
from .loader import load_image, load_pdf_images, extract_text_from_pdf
from .rag_engine import MedicalRAGEngine

# Load environment variables, prefer .env.local if present
env_path = os.path.join(os.path.dirname(__file__), "../.env")
if os.path.exists(env_path):
    load_dotenv(env_path)

class PrescriptionAnalyzer:
    def __init__(self, api_key: str = None):
        self.api_key = api_key or os.getenv("GEMINI_API_KEY") or os.getenv("GOOGLE_API_KEY")
        if not self.api_key:
            # Try loading from the project root .env.local as a last resort
            root_env = os.path.abspath(os.path.join(os.path.dirname(__file__), "../../../.env.local"))
            if os.path.exists(root_env):
                load_dotenv(root_env)
                self.api_key = os.getenv("GEMINI_API_KEY") or os.getenv("GOOGLE_API_KEY")
        
        if not self.api_key:
            raise ValueError("Gemini/Google API Key not found. Please set GEMINI_API_KEY or GOOGLE_API_KEY.")
        
        genai.configure(api_key=self.api_key)
        self.rag_engine = MedicalRAGEngine()
        
        # Initialize with dummy data if needed (for demonstration)
        # In production, this would be a separate ingestion pipeline
        if not self.rag_engine.documents:
            print("Initializing RAG with dummy medical knowledge...")
            dummy_text = "\n".join([
                "Amoxicillin is a penicillin antibiotic tailored to fight bacteria.",
                "Common side effects of Amoxicillin include nausea and rash.",
                "Paracetamol is used for pain relief and fever reduction.",
                "Ibuprofen is a non-steroidal anti-inflammatory drug (NSAID).",
                "Metformin is the first-line medication for the treatment of type 2 diabetes.",
                "Lisinopril is used to treat high blood pressure and heart failure."
            ])
            self.rag_engine.ingest_text(dummy_text)

    @retry(
        retry=retry_if_exception_type(Exception), 
        wait=wait_exponential(multiplier=2, min=4, max=60),
        stop=stop_after_attempt(5)
    )
    def _generate_with_retry(self, model_name: str, contents: list, system_instruction: str = None):
        """Helper to call Gemini with retry logic for rate limits."""
        print(f"DEBUG: Calling Gemini {model_name} with {len(contents)} parts")
        try:
            model = genai.GenerativeModel(
                model_name=model_name,
                system_instruction=system_instruction
            )
            return model.generate_content(contents)
        except Exception as e:
            print(f"DEBUG: Gemini API call failed: {e}")
            raise e

    def analyze_prescription(self, file_path: str) -> PrescriptionData:
        """Analyze a prescription file (image or PDF) and return structured data."""
        
        # 1. Load File content
        try:
            with open(file_path, "rb") as f:
                file_bytes = f.read()
        except FileNotFoundError:
            raise FileNotFoundError(f"File not found: {file_path}")

        file_ext = os.path.splitext(file_path)[1].lower()
        parts = []

        if file_ext in [".jpg", ".jpeg", ".png", ".webp"]:
            mime_type = f"image/{file_ext[1:]}" if file_ext != ".jpg" else "image/jpeg"
            parts = [{"mime_type": mime_type, "data": file_bytes}]
        elif file_ext == ".pdf":
            # For robustness, we'll extract text and send it. 
            # report_analyzer sends PDF directly, we can do that too if we want vision on full PDF.
            # But here we'll follow the existing multimodal intent.
            parts = [{"mime_type": "application/pdf", "data": file_bytes}]
        else:
             raise ValueError("Unsupported file format. Use JPG, PNG, or PDF.")

        # 2. Prompt Engineering
        system_prompt = """
        You are a highly expert medical assistant specializing in analyzing prescriptions.
        Your task is to extract structured data from the provided prescription image or text.
        
        Return ONLY a valid JSON object matching this structure:
        {
            "doctor_name": "string or null",
            "patient_name": "string or null",
            "date": "string or null",
            "medications": [
                {
                    "name": "string",
                    "dosage": "string or null",
                    "frequency": "string or null",
                    "instructions": "string or null",
                    "side_effects": ["string"]
                }
            ],
            "additional_notes": "string or null"
        }
        
        Notes:
        - If side effects are not listed on the prescription, LEAVE THE LIST EMPTY []. Do not hallucinate side effects yet.
        - Be precise with dosage and frequency.
        """
        
        # Prepare contents (just the file part, prompt goes to system_instruction)
        contents = parts

        # 3. Call Gemini
        try:
            response = self._generate_with_retry(
                model_name='gemini-flash-latest',
                contents=contents,
                system_instruction=system_prompt
            )
            
            # 4. Parse Response
            # Cleanup Markdown code blocks if present
            text = response.text.replace("```json", "").replace("```", "").strip()
            data_dict = json.loads(text)
            
            # Auto-fill side effects using RAG if missing (Hybrid Logic)
            for med in data_dict.get("medications", []):
                if not med.get("side_effects"):
                    # Query RAG for side effects
                    rag_info = self.rag_engine.retrieve(f"side effects of {med['name']}")
                    
                    if rag_info:
                         # OPTIMIZATION: Use raw RAG text instead of calling LLM again to save quota
                         # We take the top result to keep it concise
                         med["side_effects"] = [rag_info[0]]
            
            return PrescriptionData(**data_dict)
            
        except json.JSONDecodeError:
            print(f"Failed to parse JSON: {response.text}")
            return PrescriptionData(additional_notes="Failed to parse prescription data.")
        except RetryError as re:
             print(f"DEBUG: Max retries reached for Prescription. Error: {re}")
             return PrescriptionData(additional_notes="Error: Service is currently busy (Rate Limit Exceeded). Please wait a minute and try again.")
        except Exception as e:
            print(f"DEBUG: Unexpected error in analyze_prescription: {e}")
            import traceback
            traceback.print_exc()
            return PrescriptionData(additional_notes=f"Error: {str(e)}")

    def ask_medical_question(self, question: str, prescription_context: PrescriptionData = None) -> str:
        """Answer a medical question using RAG and optionally prescription context."""
        
        # 1. Retrieve Knowledge
        retrieved_docs = self.rag_engine.retrieve(question)
        context_str = "\n".join(retrieved_docs)
        
        # 2. Build Prompt
        prompt = f"""
        You are a medical assistant. Answer the user's question.
        
        Context from Medical Knowledge Base:
        {context_str}
        
        Context from Current Prescription:
        {prescription_context.model_dump_json() if prescription_context else "None"}
        
        User Question: {question}
        
        Answer concisely and accurately. If you don't know, say so.
        """
        
        try:
            response = self._generate_with_retry(
                model_name='gemini-flash-latest',
                contents=[prompt],
                system_instruction="You are a helpful medical assistant."
            )
            return response.text
        except RetryError:
            return "Error: Service is currently busy (Rate Limit Exceeded). Please try again in a minute."
        except Exception as e:
            return f"Error answering question: {str(e)}"
