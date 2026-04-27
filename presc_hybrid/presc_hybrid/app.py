import os
import uvicorn
from fastapi import FastAPI, UploadFile, File, Form, HTTPException
from fastapi.responses import JSONResponse
from src.analyzer import PrescriptionAnalyzer
from src.models import AnalysisResponse, PrescriptionData

app = FastAPI(title="Prescription Analysis API")

# Initialize Analyzer (Lazy load or startup)
# In production, check for API key
analyzer = None
latest_analysis_result = None

@app.get("/")
async def root():
    return {"status": "running", "message": "Prescription Analysis API is active. Go to /docs for interactive documentation."}

@app.on_event("startup")
async def startup_event():
    global analyzer
    try:
        analyzer = PrescriptionAnalyzer()
        print("Prescription Analyzer initialized.")
    except Exception as e:
        print(f"Warning: Analyzer failed to initialize (likely missing API key): {e}")

@app.post("/analyze", response_model=PrescriptionData)
async def analyze_prescription(file: UploadFile = File(...)):
    global latest_analysis_result
    if not analyzer:
        raise HTTPException(status_code=500, detail="Analyzer not initialized. Check server logs/API Key.")
    
    # Save temp file
    temp_filename = f"temp_{file.filename}"
    with open(temp_filename, "wb") as buffer:
        buffer.write(await file.read())
        
    try:
        result = analyzer.analyze_prescription(temp_filename)
        latest_analysis_result = result # Store context for /ask
        return result
    finally:
        if os.path.exists(temp_filename):
            os.remove(temp_filename)

@app.post("/ask")
async def ask_question(question: str = Form(...), context_json: str = Form(None)):
    global latest_analysis_result
    if not analyzer:
        raise HTTPException(status_code=500, detail="Analyzer not initialized.")
    
    context = None
    if context_json:
        try:
            import json
            data = json.loads(context_json)
            context = PrescriptionData(**data)
        except:
            pass # Ignore invalid context
    elif latest_analysis_result:
        context = latest_analysis_result
            
    answer = analyzer.ask_medical_question(question, context)
    return {"question": question, "answer": answer}

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
