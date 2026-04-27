from pydantic import BaseModel
from typing import Optional, List

class SendOTPRequest(BaseModel):
    email: Optional[str] = None
    phone: Optional[str] = None

class VerifyOTPRequest(BaseModel):
    email: Optional[str] = None
    phone: Optional[str] = None
    otp: str

class RoleInfo(BaseModel):
    role_id: Optional[str]
    role_name: str

class AuthResponse(BaseModel):
    access_token: Optional[str] = None
    is_new_user: bool
    roles: List[RoleInfo] = []

class RoleSelectionRequest(BaseModel):
    email: Optional[str] = None
    phone: Optional[str] = None
    role_id: str
