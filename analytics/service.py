from sqlalchemy.orm import Session
from model import VitalsRecord, User, HealthData
from sqlalchemy import desc

def get_vitals_trends(db: Session, user_id: str):
    # Find the health_id for this user
    user = db.query(User).filter(User.id == user_id).first()
    if not user or not user.HealthDataID:
        return []
    
    # Fetch last 30 vitals records
    vitals = db.query(VitalsRecord)\
        .filter(VitalsRecord.health_id == user.HealthDataID)\
        .order_by(desc(VitalsRecord.createdAt))\
        .limit(30)\
        .all()
    
    return [
        {
            "id": str(v.id),
            "bloodPressureH": v.bloodPressureH,
            "bloodPressureL": v.bloodPressureL,
            "heartRate": v.heartRate,
            "bloodGlucose": v.bloodGlucose,
            "bloodSaturation": v.bloodSaturation,
            "temperature": v.temperature,
            "riskStatus": v.riskStatus,
            "createdAt": v.createdAt.isoformat() if v.createdAt else None
        }
        for v in reversed(vitals) # Reverse to get chronological order for charts
    ]

def get_health_summary(db: Session, user_id: str):
    vitals = get_vitals_trends(db, user_id)
    if not vitals:
        return {
            "status": "No data",
            "message": "Start recording your vitals to see analytics."
        }
    
    latest = vitals[-1]
    
    # Simple aggregation (could be more complex)
    avg_hr = sum(v["heartRate"] for v in vitals if v["heartRate"]) / len([v for v in vitals if v["heartRate"]]) if any(v["heartRate"] for v in vitals) else 0
    
    return {
        "latest": latest,
        "averages": {
            "heartRate": round(avg_hr, 1),
        },
        "count": len(vitals)
    }
