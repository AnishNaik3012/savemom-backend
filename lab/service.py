from sqlalchemy.orm import Session
from uuid import UUID
from model import LabReportType, MedicalReading
from . import schemas

def get_lab_report_types(db: Session, entity_id: UUID = None):
    query = db.query(LabReportType)
    if entity_id:
        query = query.filter(LabReportType.entityID == entity_id)
    return query.all()

def add_medical_reading(db: Session, reading_data: schemas.MedicalReadingCreate):
    new_reading = MedicalReading(**reading_data.model_dump())
    db.add(new_reading)
    db.commit()
    db.refresh(new_reading)
    return new_reading

def get_patient_lab_history(db: Session, health_id: UUID):
    return db.query(MedicalReading).filter(MedicalReading.health_id == health_id).order_by(MedicalReading.createdAt.desc()).all()

def format_lab_history_for_chat(db: Session, health_id: UUID):
    history = get_patient_lab_history(db, health_id)
    if not history:
        return "No lab results found in your records."
    
    summary = "Here are your recent lab results:\n"
    for record in history[:5]: # Last 5 records
        date_str = record.createdAt.strftime("%Y-%m-%d")
        summary += f"- **{record.report_name or 'Lab Test'}** ({date_str}): {record.value} {record.unit} ({record.riskStatus or 'Normal'})\n"
    
    return summary
