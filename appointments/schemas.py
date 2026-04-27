from pydantic import BaseModel, ConfigDict
from datetime import datetime
from uuid import UUID

class AppointmentCreate(BaseModel):
    doctor_name: str
    appointment_time: datetime
    reason: str | None = None

class AppointmentOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    doctor_name: str | None
    appointment_time: datetime | None
    reason: str | None
    status: str
