from pydantic import BaseModel
from typing import List, Optional

class Medication(BaseModel):
    name: str
    dosage: Optional[str] = None
    frequency: Optional[str] = None
    instructions: Optional[str] = None
    side_effects: Optional[List[str]] = []

class PrescriptionData(BaseModel):
    doctor_name: Optional[str] = None
    patient_name: Optional[str] = None
    date: Optional[str] = None
    medications: List[Medication] = []
    additional_notes: Optional[str] = None

class AnalysisResponse(BaseModel):
    prescription: PrescriptionData
    context_answer: Optional[str] = None
