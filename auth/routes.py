from fastapi import APIRouter, HTTPException, BackgroundTasks, Response
from fastapi.responses import HTMLResponse
from auth.schemas import SendOTPRequest, VerifyOTPRequest, AuthResponse, RoleSelectionRequest
from auth.otp import generate_otp, verify_otp, send_otp_email, unsubscribe_user
from auth.security import create_token
from auth.service import is_new_user, get_user_roles, get_all_roles, register_user

router = APIRouter()


@router.post("/send-otp")
def send_otp(data: SendOTPRequest, background_tasks: BackgroundTasks):
    identifier = data.email or data.phone

    if not identifier:
        raise HTTPException(status_code=422, detail="Email or phone required")

    # Sanitize identifier (remove accidental whitespace or backticks)
    identifier = identifier.strip().lower().replace("`", "")
    
    otp = generate_otp(identifier)
    
    # Send email in background if it's an email identifier
    if "@" in identifier:
        background_tasks.add_task(send_otp_email, identifier, otp)
        
    return {"message": "OTP sent"}


@router.post("/verify-otp", response_model=AuthResponse)
def verify_otp_route(data: VerifyOTPRequest):
    identifier = data.email or data.phone

    if not identifier:
        raise HTTPException(status_code=422, detail="Email or phone required")

    if not data.otp:
        raise HTTPException(status_code=422, detail="OTP required")

    if not verify_otp(identifier, data.otp):
        raise HTTPException(status_code=401, detail="Invalid OTP")

    # Get existing roles for this identifier
    roles = get_user_roles(identifier)
    new_user = is_new_user(identifier)

    # Return roles and is_new_user flag
    return {
        "access_token": None,
        "is_new_user": new_user,
        "roles": roles
    }

@router.post("/select-role")
def select_role(data: RoleSelectionRequest):
    identifier = data.email or data.phone
    if not identifier:
        raise HTTPException(status_code=422, detail="Email or phone required")
    
    # If new user, register them with this role
    if is_new_user(identifier):
        register_user(identifier, data.role_id)
    
    # Create token for this identifier
    # Note: In a real app, the token should probably encode the role/user ID too
    token = create_token(identifier)
    return {"access_token": token}

@router.get("/roles")
def get_roles():
    return get_all_roles()

@router.get("/unsubscribe", response_class=HTMLResponse)
def unsubscribe(email: str):
    if not email:
        raise HTTPException(status_code=400, detail="Email is required")
    
    # Sanitize
    email = email.strip().lower().replace("`", "")
    
    unsubscribe_user(email)
    
    return """
    <html>
        <head><title>Unsubscribed</title></head>
        <body style="font-family: Arial, sans-serif; text-align: center; padding: 50px;">
            <h1 style="color: #2563eb;">You have been unsubscribed</h1>
            <p>You will no longer receive transactional emails in your primary folder.</p>
            <p style="color: #64748b; font-size: 14px;">(Emails will be redirected to your spam folder as per your request)</p>
        </body>
    </html>
    """
