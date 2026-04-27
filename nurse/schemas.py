from pydantic import BaseModel, ConfigDict
from datetime import datetime
from uuid import UUID
from typing import List, Optional

class VitalsCreate(BaseModel):
    bloodPressureH: Optional[int] = None
    bloodPressureL: Optional[int] = None
    bloodSaturation: Optional[float] = None
    temperature: Optional[float] = None
    temperatureMetric: Optional[str] = "C"
    heartRate: Optional[int] = None
    bloodGlucose: Optional[float] = None
    bloodGlucoseUnit: Optional[str] = "mg/dL"
    bmiHeight: Optional[int] = None
    bmiWeight: Optional[float] = None
    respiratoryRate: Optional[int] = None
    hB: Optional[float] = None

class VitalsOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    health_id: Optional[UUID]
    bloodPressureH: Optional[int]
    bloodPressureL: Optional[int]
    bloodSaturation: Optional[float]
    temperature: Optional[float]
    temperatureMetric: Optional[str]
    heartRate: Optional[int]
    bloodGlucose: Optional[float]
    bloodGlucoseUnit: Optional[str]
    bmiHeight: Optional[int]
    bmiWeight: Optional[float]
    respiratoryRate: Optional[int]
    hB: Optional[float]
    createdAt: datetime
    riskStatus: Optional[str]

class PatientSummary(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    
    id: UUID
    name: Optional[str]
    email: Optional[str]
    phone: Optional[str]
    last_vitals: Optional[VitalsOut] = None
    riskStatus: Optional[str] = "Normal"

class TaskOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    
    id: UUID
    requestType: str
    priority: str
    status: str
    reason: Optional[str]
    createdAt: datetime
    patient_name: Optional[str] = None

class RiskStatusUpdate(BaseModel):
    riskStatus: str

class NurseProfileOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    
    id: UUID
    name: Optional[str]
    email: Optional[str]
    phone: Optional[str]
    gender: Optional[str]
    dob: Optional[datetime]
    city: Optional[str]
    pincode: Optional[str]
