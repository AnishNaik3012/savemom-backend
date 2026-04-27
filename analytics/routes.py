import uuid
from fastapi import APIRouter, Depends, Header, HTTPException, status, Request
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlalchemy.orm import Session
from db import SessionLocal
from analytics.service import get_vitals_trends, get_health_summary
from core.dependencies import get_current_user
from auth.security import SECRET_KEY, ALGORITHM
from jose import jwt, JWTError
from typing import Optional

router = APIRouter(tags=["Analytics"])
security = HTTPBearer(auto_error=False) # Important: auto_error=False

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Security Constant for Dev Bypass
DEV_BYPASS_KEY = "dev-bypass-savemom-2026"
# Target Data for Testing (as UUID)
TEST_USER_ID = uuid.UUID("3664c19c-d9ae-4619-a297-74b3f6849c75")

def get_user_with_bypass(
    request: Request,
    credentials: Optional[HTTPAuthorizationCredentials] = Depends(security),
):
    # Case-insensitive header check
    bypass_header = request.headers.get('x-dev-bypass')
    if bypass_header == DEV_BYPASS_KEY:
        return TEST_USER_ID
    
    if not credentials:
        raise HTTPException(status_code=401, detail="Not authenticated")
    
    token = credentials.credentials
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return payload.get("sub")
    except JWTError:
        raise HTTPException(status_code=401, detail="Invalid token")

@router.get("/vitals")
def fetch_vitals_trends(
    db: Session = Depends(get_db),
    user_id: str = Depends(get_user_with_bypass)
):
    """
    Fetch historical vitals trends for the current user.
    Supports dev bypass for testing.
    """
    return get_vitals_trends(db, user_id)

@router.get("/summary")
def fetch_health_summary(
    db: Session = Depends(get_db),
    user_id: str = Depends(get_user_with_bypass)
):
    """
    Fetch a summary of health metrics for the current user.
    Supports dev bypass for testing.
    """
    return get_health_summary(db, user_id)
