from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from db import SessionLocal
from appointments.schemas import AppointmentCreate, AppointmentOut
from appointments.service import create_appointment, get_user_appointments
from core.dependencies import get_current_user

router = APIRouter(tags=["Appointments"])

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/book", response_model=AppointmentOut)
def book_appointment(
    data: AppointmentCreate,
    db: Session = Depends(get_db),
    user_id: str = Depends(get_current_user)
):
    return create_appointment(db, user_id, data)

@router.get("/my", response_model=list[AppointmentOut])
def my_appointments(
    db: Session = Depends(get_db),
    user_id: str = Depends(get_current_user)
):
    return get_user_appointments(db, user_id)
