from fastapi import APIRouter, Header, HTTPException, Depends
from pydantic import BaseModel
from typing import Optional, Dict, Any
import os

from .rag_service import rag_service

router = APIRouter()

# Simple API Key mapping (Mock)
# In production, these would be in a DB table
API_KEYS = {
    "savemom-dev-123": "Developer Key",
    "savemom-client-abc": "Mobile App Client"
}

def verify_api_key(x_api_key: str = Header(None)):
    """
    Dependency to verify the API key in headers.
    """
    if not x_api_key:
        raise HTTPException(status_code=401, detail="API Key is missing (X-API-KEY header)")
    
    if x_api_key not in API_KEYS:
        # Check environment variable as well
        env_key = os.getenv("RAG_API_KEY")
        if env_key and x_api_key == env_key:
            return API_KEYS.get(x_api_key, "Environmental Key")
            
        raise HTTPException(status_code=403, detail="Invalid API Key")
    
    return API_KEYS[x_api_key]

class HybridChatRequest(BaseModel):
    query: str
    use_rag: bool = True

@router.post("/ask")
async def hybrid_ask(
    payload: HybridChatRequest, 
    client_name: str = Depends(verify_api_key)
):
    """
    Hybrid Endpoint: Retrieves context if requested, then calls LLM.
    Protected by API Key.
    """
    context = ""
    if payload.use_rag:
        # Step 1: Retrieve context from RAG service
        context = rag_service.retrieve_context(payload.query)
        print(f"RAG Retrieval for '{client_name}': {len(context)} chars found.")

    # Step 2: Generate response via LLM service
    response = await rag_service.generate_hybrid_response(payload.query, context if payload.use_rag else None)
    
    return {
        "query": payload.query,
        "response": response,
        "rag_used": bool(context),
        "client": client_name
    }

@router.get("/status")
def get_status(client_name: str = Depends(verify_api_key)):
    """Small status health check for the RAG system."""
    return {
        "status": "online",
        "service": "Hybrid RAG LLM Model",
        "client_authenticated": client_name,
        "knowledge_entries": len(rag_service._knowledge_base)
    }

@router.post("/wellness-insight")
async def get_wellness_insight(
    payload: Optional[Dict[str, Any]] = None,
    client_name: str = Depends(verify_api_key)
):
    """
    Experimental: Generates a Maternal Wellness Insight and Score.
    """
    insight_data = await rag_service.generate_wellness_insight(payload)
    return {
        "client": client_name,
        "data": insight_data
    }
