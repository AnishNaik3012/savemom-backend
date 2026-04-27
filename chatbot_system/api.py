from fastapi import APIRouter, HTTPException, Depends, File, UploadFile
from pydantic import BaseModel
from typing import Optional, Dict, Any, List

from .factory import ChatbotFactory
import os
import sys

# Path setup for prescription module
presc_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "../presc_hybrid/presc_hybrid"))
if presc_path not in sys.path:
    sys.path.append(presc_path)

router = APIRouter()

# --- Request/Response Models ---
class ChatRequest(BaseModel):
    user_id: str
    user_role: str  # In production, this would be extracted from a JWT token
    message: str

class NewChatRequest(BaseModel):
    message: str
    role: str

class ChatResponse(BaseModel):
    response: Any
    metadata: Optional[Dict] = {}
    type: str = "text"
    buttons: Optional[List[Dict]] = None

# --- Dependency Injection for DB (Stub) ---
def get_db_session():
    # In real world: yield SessionLocal()
    return None

# --- Endpoints ---
@router.post("/chat", response_model=ChatResponse)
async def chat_endpoint(payload: ChatRequest, db = Depends(get_db_session)):
    # ... existing logic ...
    try:
        engine = ChatbotFactory.get_engine_for_user(payload.user_role, db)
        bot_response = engine.handle_message(
            user_id=payload.user_id,
            user_role=payload.user_role,
            text=payload.message
        )
        
        if isinstance(bot_response, dict):
            return ChatResponse(**bot_response)
        
        return ChatResponse(response=bot_response)
    except Exception as e:
        print(f"Error processing chat: {e}")
        raise HTTPException(status_code=500, detail="Internal Chatbot Error")

@router.post("/message", response_model=ChatResponse)
async def new_chat_message(payload: NewChatRequest, db = Depends(get_db_session)):
    """
    Endpoint for the new Next.js frontend.
    """
    try:
        # For prototype, we use 'temp-user' since Next.js frontend doesn't pass user_id yet
        user_id = "temp-user"
        
        # 1. Get the Role-Based Engine
        engine = ChatbotFactory.get_engine_for_user(payload.role, db)
        
        # 2. Process Message
        bot_response = engine.handle_message(
            user_id=user_id,
            user_role=payload.role,
            text=payload.message
        )
        
        if isinstance(bot_response, dict):
            return ChatResponse(**bot_response)
            
        return ChatResponse(response=bot_response)

    except Exception as e:
        print(f"Error processing chat: {e}")
        raise HTTPException(status_code=500, detail="Internal Chatbot Error")
@router.post("/upload-report", response_model=ChatResponse)
async def upload_report(file: UploadFile = File(...)):
    """
    Endpoint to receive a medical report (PDF or Image), analyze it, and return structured data.
    """
    try:
        from .report_analyzer import analyze_report_with_ai
        
        # Read file content
        content = await file.read()
        mime_type = file.content_type or "application/pdf"
        
        # 1. Analyze with AI (Gemini or Fallback)
        analysis_result = await analyze_report_with_ai(content, mime_type)
        
        return ChatResponse(
            response=analysis_result.get("summary", "Analysis complete."),
            metadata=analysis_result,
            type="report_analysis"
        )

    except Exception as e:
        print(f"Error analyzing report: {e}")
        raise HTTPException(status_code=500, detail=f"Failed to analyze report: {str(e)}")

@router.post("/upload-prescription", response_model=ChatResponse)
async def upload_prescription(file: UploadFile = File(...)):
    """
    Endpoint to receive a prescription, analyze it, and return structured data.
    """
    print(f"DEBUG: Received prescription upload request: {file.filename}")
    try:
        from src.analyzer import PrescriptionAnalyzer
        analyzer = PrescriptionAnalyzer()
        
        # Save file temporarily or handle bytes if analyzer supports it
        # The analyzer.py expects a file path
        temp_path = f"temp_{file.filename}"
        with open(temp_path, "wb") as f:
            f.write(await file.read())
            
        try:
            analysis_result = analyzer.analyze_prescription(temp_path)
            
            # Convert PrescriptionData to dict
            data = analysis_result.model_dump()
            
            # Format for frontend report_analysis type (reusing the visual components where possible)
            # Or define a new 'prescription_analysis' type if needed.
            # Let's map it to similar metadata structure so the frontend can display it easily.
            
            response_metadata = {
                "report_title": "Prescription Analysis",
                "category": "Prescription",
                "doctor_name": data.get("doctor_name"),
                "patient_name": data.get("patient_name"),
                "date": data.get("date"),
                "summary": data.get("additional_notes") or "Prescription successfully analyzed.",
                "health_status": "Normal", # Default
                "extracted_fields": [
                    {"label": "Doctor", "value": data.get("doctor_name") or "Not found"},
                    {"label": "Patient", "value": data.get("patient_name") or "Not found"},
                    {"label": "Date", "value": data.get("date") or "Not found"}
                ],
                "medications": data.get("medications", []),
                "is_prescription": True
            }
            
            return ChatResponse(
                response=response_metadata["summary"],
                metadata=response_metadata,
                type="prescription_analysis"
            )
        finally:
            if os.path.exists(temp_path):
                os.remove(temp_path)

    except Exception as e:
        print(f"Error analyzing prescription: {e}")
        raise HTTPException(status_code=500, detail=f"Failed to analyze prescription: {str(e)}")
