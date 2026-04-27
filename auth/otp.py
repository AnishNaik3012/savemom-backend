from utils.email_utils import send_email_otp
from auth.service import unsubscribe_user_db, is_user_unsubscribed

otp_store = {}


def generate_otp(identifier: str) -> str:
    # TEMP fixed OTP for testing, but let's make it a bit more dynamic for demo
    import random
    otp = str(random.randint(100000, 999999))
    
    otp_store[identifier] = otp
    print(f"[OTP DEBUG] {identifier} -> {otp}")
    return otp

def send_otp_email(email: str, otp: str):
    """Bridge for background task sending"""
    unsubscribed = is_user_unsubscribed(email)
    send_email_otp(email, otp, is_unsubscribed=unsubscribed)

def unsubscribe_user(email: str):
    unsubscribe_user_db(email)



def verify_otp(identifier: str, otp: str) -> bool:
    return otp_store.get(identifier) == otp
