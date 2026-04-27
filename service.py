from sqlalchemy.orm import Session
from model import Appointment

def create_appointment(db: Session, user_id: str, data):
    appointment = Appointment(
        user_id=user_id,
        doctor_name=data.doctor_name,
        appointment_time=data.appointment_time,
        reason=data.reason
    )
    db.add(appointment)
    db.commit()
    db.refresh(appointment)
    return appointment

def get_user_appointments(db: Session, user_id: str):
    return db.query(Appointment).filter(
        Appointment.user_id == user_id
    ).all()
