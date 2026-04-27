import os
from dotenv import load_dotenv
from utils.email_utils import send_email_otp

# Load environment variables
load_dotenv()
load_dotenv(".env.local")

recipient = "anishnaik307@gmail.com"
test_otp = "123456"

print(f"Testing SMTP with recipient: {recipient}")
send_email_otp(recipient, test_otp)
print("Test complete.")
