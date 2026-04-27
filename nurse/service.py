from sqlalchemy.orm import Session
from model import User, HealthData, VitalsRecord, UserRequest, Role
from uuid import UUID
import uuid
from typing import List, Optional
from datetime import datetime

def get_assigned_patients(db: Session, nurse_id: UUID):
    # This is a simplified logic. In a real app, there might be a mapping table
    # or a field in User/HealthData to link patients to a specific nurse.
    # For now, we'll return users with role "Mother" as a placeholder for patients.
    mother_role = db.query(Role).filter(Role.name == "Mother").first()
    if not mother_role:
        return []
    
    patients = db.query(User).filter(
        User.roleId == mother_role.id,
        (User.isDeleted == False) | (User.isDeleted == None)
    ).all()
    
    result = []
    for p in patients:
        # Get latest vitals if available
        latest_vital = None
        if p.HealthDataID:
            latest_vital = db.query(VitalsRecord).filter(
                VitalsRecord.health_id == p.HealthDataID
            ).order_by(VitalsRecord.createdAt.desc()).first()
        
        result.append({
            "id": p.id,
            "name": p.name,
            "email": p.email,
            "phone": p.phone,
            "last_vitals": latest_vital,
            "riskStatus": p.healthData.riskStatus if p.healthData else "Normal"
        })
    return result

def get_patient_vitals(db: Session, patient_id: UUID):
    user = db.query(User).filter(User.id == patient_id).first()
    if not user or not user.HealthDataID:
        return []
    
    return db.query(VitalsRecord).filter(
        VitalsRecord.health_id == user.HealthDataID
    ).order_by(VitalsRecord.createdAt.desc()).all()

def record_vitals(db: Session, patient_id: UUID, vitals_data: dict):
    user = db.query(User).filter(User.id == patient_id).first()
    if not user:
        return None
    
    # Ensure HealthData exists
    if not user.HealthDataID:
        health_data = HealthData(id=uuid.uuid4(), UserID=user.id)
        db.add(health_data)
        db.commit()
        db.refresh(health_data)
        user.HealthDataID = health_data.id
        db.commit()

    new_vitals = VitalsRecord(
        id=uuid.uuid4(),
        health_id=user.HealthDataID,
        **vitals_data,
        createdAt=datetime.now()
    )
    db.add(new_vitals)
    db.commit()
    db.refresh(new_vitals)
    return new_vitals

def get_nurse_tasks(db: Session, nurse_id: UUID):
    # Retrieve requests assigned to this nurse or general nurse-type requests
    tasks = db.query(UserRequest).filter(
        (UserRequest.toUserID == nurse_id) | (UserRequest.requestType == "Nurse"),
        UserRequest.status != "Completed"
    ).order_by(UserRequest.priority.desc(), UserRequest.createdAt.desc()).all()
    
    result = []
    for t in tasks:
        patient_name = None
        if t.healthID:
            hd = db.query(HealthData).filter(HealthData.id == t.healthID).first()
            if hd and hd.user:
                patient_name = hd.user.name
        
        result.append({
            "id": t.id,
            "requestType": t.requestType,
            "priority": t.priority,
            "status": t.status,
            "reason": t.reason,
            "createdAt": t.createdAt,
            "patient_name": patient_name
        })
    return result

def complete_task(db: Session, task_id: UUID):
    task = db.query(UserRequest).filter(UserRequest.id == task_id).first()
    if task:
        task.status = "Completed"
        task.updatedAt = datetime.now()
        db.commit()
        db.refresh(task)
    return task

def get_patient_summary(db: Session, patient_id: UUID):
    user = db.query(User).filter(User.id == patient_id).first()
    if not user:
        return None
    
    latest_vital = None
    risk_status = "Normal"
    if user.HealthDataID:
        latest_vital = db.query(VitalsRecord).filter(
            VitalsRecord.health_id == user.HealthDataID
        ).order_by(VitalsRecord.createdAt.desc()).first()
        
        hd = db.query(HealthData).filter(HealthData.id == user.HealthDataID).first()
        if hd and hd.riskStatus:
            risk_status = hd.riskStatus
            
    return {
        "id": user.id,
        "name": user.name,
        "email": user.email,
        "phone": user.phone,
        "last_vitals": latest_vital,
        "riskStatus": risk_status
    }

def update_patient_risk_status(db: Session, patient_id: UUID, risk_status: str):
    user = db.query(User).filter(User.id == patient_id).first()
    if not user:
        return None
        
    # Ensure HealthData exists
    if not user.HealthDataID:
        health_data = HealthData(id=uuid.uuid4(), UserID=user.id, riskStatus=risk_status)
        db.add(health_data)
        db.commit()
        db.refresh(health_data)
        user.HealthDataID = health_data.id
        db.commit()
    else:
        health_data = db.query(HealthData).filter(HealthData.id == user.HealthDataID).first()
        if health_data:
            health_data.riskStatus = risk_status
            db.commit()
            db.refresh(health_data)
            
    return get_patient_summary(db, patient_id)

def get_nurse_profile(db: Session, nurse_id: UUID):
    return db.query(User).filter(User.id == nurse_id).first()
