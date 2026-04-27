import os
from dotenv import load_dotenv
from utils.email_utils import send_email_otp

# Load environment variables from .env.local
load_dotenv(".env.local")

def test_sendgrid_integration():
    test_email = os.getenv("TEST_RECIPIENT_EMAIL", "test@example.com")
    test_otp = "123456"
    
    print(f"Testing SendGrid integration with email: {test_email}")
    send_email_otp(test_email, test_otp)
    print("\nCheck the console output above for status codes.")
    print("If you see Status Code 202, it means SendGrid accepted the request.")

if __name__ == "__main__":
    test_sendgrid_integration()
