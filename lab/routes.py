from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from db import SessionLocal
from . import schemas, service
from uuid import UUID
from typing import List

router = APIRouter(tags=["Lab"])

# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.get("/types", response_model=List[schemas.LabReportTypeOut])
def get_lab_report_types(entity_id: UUID = None, db: Session = Depends(get_db)):
    return service.get_lab_report_types(db, entity_id)

@router.post("/record", response_model=schemas.MedicalReadingOut)
def record_lab_test(reading: schemas.MedicalReadingCreate, db: Session = Depends(get_db)):
    return service.add_medical_reading(db, reading)

@router.get("/history/{health_id}", response_model=List[schemas.MedicalReadingOut])
def get_patient_lab_history(health_id: UUID, db: Session = Depends(get_db)):
    return service.get_patient_lab_history(db, health_id)
