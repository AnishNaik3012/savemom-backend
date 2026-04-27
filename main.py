from fastapi import FastAPI
from dotenv import load_dotenv
import os

# Load environment variables early
load_dotenv()
load_dotenv(".env.local")

from chatbot_system.api import router as chat_router
from auth.routes import router as auth_router
from appointments.routes import router as appointment_router
from db import Base, engine
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(
    title="SaveMom Chatbot API",
    description="Role-Based Chatbot Backend for Maternal Healthcare",
    version="1.0.0"
)

# Enable CORS (Cross-Origin Resource Sharing)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # DEV MODE — allow all
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Register/Include Routers
from chatbot_system.rag.hybrid_routes import router as rag_router


app.include_router(chat_router, prefix="/chat", tags=["Chat"])
app.include_router(auth_router, prefix="/auth", tags=["Auth"])
app.include_router(appointment_router, prefix="/appointments", tags=["Appointments"])
app.include_router(rag_router, prefix="/rag", tags=["RAG"])
app.include_router(chat_router, prefix="/api/v1", tags=["Legacy Chat"]) 

# Initialize DB
Base.metadata.create_all(bind=engine)

@app.get("/")
def health_check():
    return {"status": "ok", "service": "SaveMom Chatbot Backend"}

if __name__ == "__main__":
    import uvicorn
    # Run the server
    # Command: python main.py
    print("Starting SaveMom Chatbot Server...")
    uvicorn.run(app, host="0.0.0.0", port=8000)
