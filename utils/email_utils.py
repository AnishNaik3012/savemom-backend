import os
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

def send_email_otp(recipient_email: str, otp: str, is_unsubscribed: bool = False):
    """
    Sends an OTP to the recipient's email using SMTP.
    If is_unsubscribed is True, adds spam headers to push to spam folder.
    """
    subject = "Your SaveMom OTP"
    if is_unsubscribed:
        subject = f"[SPAM ALERT] {subject}"

    api_base_url = os.getenv("API_BASE_URL", "http://localhost:8000")
    unsubscribe_link = f"{api_base_url}/auth/unsubscribe?email={recipient_email}"
    
    plain_content = f"Your OTP for SaveMom login is: {otp}. It will expire in 5 minutes. Unsubscribe: {unsubscribe_link}"
    
    # Anti-Spam Compliant HTML Template
    html_content = f"""
    <div style="font-family: Arial, sans-serif; max-width: 600px; margin: auto; padding: 20px; border: 1px solid #e2e8f0; border-radius: 12px;">
        <div style="text-align: center; margin-bottom: 30px;">
            <h1 style="color: #2563eb; margin: 0;">SaveMom Health</h1>
            <p style="color: #64748b; font-size: 14px;">Maternal Care Support</p>
        </div>
        
        <div style="padding: 20px; border-top: 1px solid #f1f5f9; border-bottom: 1px solid #f1f5f9;">
            <p style="font-size: 16px; color: #1e293b;">Hello,</p>
            <p style="font-size: 16px; color: #1e293b;">Your One-Time Password (OTP) for accessing your SaveMom account is:</p>
            
            <div style="text-align: center; margin: 30px 0;">
                <span style="font-size: 32px; font-weight: bold; color: #2563eb; letter-spacing: 5px; background: #eff6ff; padding: 10px 20px; border-radius: 8px;">{otp}</span>
            </div>
            
            <p style="font-size: 14px; color: #64748b;">This code will expire in 5 minutes. If you did not request this, please ignore this email.</p>
        </div>
        
        <div style="margin-top: 30px; text-align: center; font-size: 12px; color: #94a3b8; line-height: 1.6;">
            <p style="margin: 0;">&copy; 2024 SaveMom Health. All rights reserved.</p>
            <p style="margin: 4px 0;">Hospital Road, Madurai, TN, India - 625001</p>
            <p style="margin: 10px 0;">
                <a href="#" style="color: #2563eb; text-decoration: none;">Privacy Policy</a> | 
                <a href="{unsubscribe_link}" style="color: #2563eb; text-decoration: none;">Unsubscribe</a>
            </p>
            <p style="font-style: italic;">This is a transactional email regarding your clinical account security.</p>
        </div>
    </div>
    """

    # Debug print
    print(f"\n--- [EMAIL ATTEMPT (SMTP)] ---")
    print(f"To: {recipient_email}")
    print(f"Subject: {subject}")
    print(f"----------------------\n")

    smtp_server = os.getenv("SMTP_SERVER")
    smtp_port = os.getenv("SMTP_PORT", "587")
    smtp_user = os.getenv("SMTP_USER")
    smtp_password = os.getenv("SMTP_PASSWORD")

    if not all([smtp_server, smtp_user, smtp_password]):
        print("[WARNING] SMTP settings (SERVER/USER/PASSWORD) not configured.")
        print("[FALLBACK] Check console debug for OTP.")
        print(f"OTP for {recipient_email}: {otp}")
        return

    msg = MIMEMultipart("alternative")
    msg["Subject"] = subject
    msg["From"] = smtp_user
    msg["To"] = recipient_email

    if is_unsubscribed:
        # Aggressive spam signaling headers
        msg["X-Spam-Flag"] = "YES"
        msg["X-Spam-Status"] = "Yes, score=15.0 required=5.0 tests=GTUBE,MISSING_HEADERS autolearn=no"
        msg["X-Spam-Score"] = "15.0"
        msg["X-Spam-Level"] = "***************"
        msg["X-Spam-Tag"] = "spam"
        msg["X-Report-Abuse"] = "Please report this at your email provider as spam/unsubscribe."
        msg["Precedence"] = "bulk"
        msg["List-Unsubscribe"] = f"<{unsubscribe_link}>"
        msg["X-Priority"] = "5 (Lowest)"
        msg["Priority"] = "non-urgent"
        msg["Importance"] = "low"

    msg.attach(MIMEText(plain_content, "plain"))
    msg.attach(MIMEText(html_content, "html"))

    try:
        # Connect and send
        server = smtplib.SMTP(smtp_server, int(smtp_port))
        server.starttls()
        server.login(smtp_user, smtp_password)
        server.send_message(msg)
        server.quit()
        print(f"Successfully sent real email to {recipient_email} via SMTP")
    except Exception as e:
        print(f"Error sending email via SMTP: {e}")
        print(f"Fallback OTP for {recipient_email}: {otp}")
