from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from db import SessionLocal
from nurse import schemas, service
from uuid import UUID
from typing import List
from .nlp import nlp_service
from pydantic import BaseModel

router = APIRouter()

# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.get("/patients", response_model=List[schemas.PatientSummary])
def get_patients(nurse_id: UUID, db: Session = Depends(get_db)):
    return service.get_assigned_patients(db, nurse_id)

@router.get("/patients/{patient_id}/vitals", response_model=List[schemas.VitalsOut])
def get_vitals(patient_id: UUID, db: Session = Depends(get_db)):
    return service.get_patient_vitals(db, patient_id)

@router.post("/patients/{patient_id}/vitals", response_model=schemas.VitalsOut)
def record_vitals(patient_id: UUID, vitals: schemas.VitalsCreate, db: Session = Depends(get_db)):
    new_vitals = service.record_vitals(db, patient_id, vitals.model_dump(exclude_unset=True))
    if not new_vitals:
        raise HTTPException(status_code=404, detail="Patient not found")
    return new_vitals

@router.get("/tasks", response_model=List[schemas.TaskOut])
def get_tasks(nurse_id: UUID, db: Session = Depends(get_db)):
    return service.get_nurse_tasks(db, nurse_id)

@router.post("/tasks/{task_id}/complete", response_model=schemas.TaskOut)
def complete_task(task_id: UUID, db: Session = Depends(get_db)):
    task = service.complete_task(db, task_id)
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    return task

@router.get("/patients/{patient_id}/summary", response_model=schemas.PatientSummary)
def get_patient_summary(patient_id: UUID, db: Session = Depends(get_db)):
    summary = service.get_patient_summary(db, patient_id)
    if not summary:
        raise HTTPException(status_code=404, detail="Patient not found")
    return summary

@router.patch("/patients/{patient_id}/risk_status", response_model=schemas.PatientSummary)
def update_patient_risk_status(patient_id: UUID, risk_update: schemas.RiskStatusUpdate, db: Session = Depends(get_db)):
    summary = service.update_patient_risk_status(db, patient_id, risk_update.riskStatus)
    if not summary:
        raise HTTPException(status_code=404, detail="Patient not found")
    return summary

@router.get("/profile", response_model=schemas.NurseProfileOut)
def get_nurse_profile(nurse_id: UUID, db: Session = Depends(get_db)):
    profile = service.get_nurse_profile(db, nurse_id)
    if not profile:
        raise HTTPException(status_code=404, detail="Nurse profile not found")
    return profile

class PredictRequest(BaseModel):
    text: str

@router.post("/predict")
async def predict_nurse_intent(request: PredictRequest):
    intent, confidence = nlp_service.predict_intent(request.text)
    if not intent:
        raise HTTPException(status_code=500, detail="NLP prediction failed")
    return {
        "intent_name": intent,
        "confidence": confidence
    }
