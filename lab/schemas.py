from pydantic import BaseModel, ConfigDict
from uuid import UUID
from datetime import datetime
from typing import List, Optional

class LabReportTypeBase(BaseModel):
    name: str

class LabReportTypeOut(LabReportTypeBase):
    model_config = ConfigDict(from_attributes=True)
    id: UUID
    entityID: Optional[UUID] = None

class MedicalReadingBase(BaseModel):
    report_name: Optional[str] = None
    value: Optional[float] = None
    unit: Optional[str] = None
    riskStatus: Optional[str] = None
    riskCategory: Optional[str] = None
    reason: Optional[str] = None
    medical_term: Optional[str] = None
    typical_min_value: Optional[str] = None
    typical_max_value: Optional[str] = None

class MedicalReadingCreate(MedicalReadingBase):
    health_id: UUID
    report_id: Optional[UUID] = None

class MedicalReadingOut(MedicalReadingBase):
    model_config = ConfigDict(from_attributes=True)
    id: int
    health_id: UUID
    report_id: Optional[UUID]
    createdAt: datetime
    updatedAt: datetime
