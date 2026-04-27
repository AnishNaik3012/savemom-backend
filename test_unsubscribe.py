
import unittest
from unittest.mock import MagicMock, patch
import os
import sys

# Setup paths
current_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, current_dir)

from auth.otp import send_otp_email, unsubscribe_user
from auth.service import is_user_unsubscribed

class TestUnsubscribe(unittest.TestCase):
    def test_unsubscription_flow(self):
        email = "test@example.com"
        
        print("\nTesting Unsubscription Flow...")
        
        # Mock DB session for service.py
        with patch('auth.service.SessionLocal') as MockSession:
            # Mock for is_user_unsubscribed (Initial: False)
            mock_db = MockSession.return_value
            mock_db.query.return_value.filter.return_value.first.return_value = None
            
            self.assertFalse(is_user_unsubscribed(email))
            
            # Mock for unsubscribe_user (Simulate setting flag)
            mock_user = MagicMock()
            mock_user.email = email
            mock_user.isUnsubscribed = False
            
            mock_db.query.return_value.filter.return_value.all.return_value = [mock_user]
            
            unsubscribe_user(email)
            self.assertTrue(mock_user.isUnsubscribed)
            print("  User marked as unsubscribed in DB.")

    def test_spam_headers(self):
        email = "unsub@example.com"
        otp = "123456"
        
        print("\nTesting Spam Headers...")
        
        with patch('auth.otp.is_user_unsubscribed', return_value=True):
            with patch('smtplib.SMTP') as MockSMTP:
                def mock_getenv(key, default=None):
                    if key == "SMTP_SERVER": return "smtp.test.com"
                    if key == "SMTP_PORT": return "587"
                    if key == "SMTP_USER": return "test@test.com"
                    if key == "SMTP_PASSWORD": return "pass"
                    return os.environ.get(key, default)

                # We want to check what message was passed to send_message
                with patch('utils.email_utils.os.getenv', side_effect=mock_getenv):
                    from utils.email_utils import send_email_otp
                    
                    # Catch the message sent
                    instance = MockSMTP.return_value
                    
                    send_email_otp(email, otp, is_unsubscribed=True)
                    
                    # Get the 'msg' passed to send_message
                    self.assertTrue(instance.send_message.called)
                    args, kwargs = instance.send_message.call_args
                    msg = args[0]
                    
                    print(f"  Subject: {msg['Subject']}")
                    print(f"  X-Spam-Flag: {msg['X-Spam-Flag']}")
                    
                    self.assertIn("[SPAM ALERT]", msg['Subject'])
                    self.assertEqual(msg['X-Spam-Flag'], "YES")
                    self.assertEqual(msg['X-Spam-Status'], "Yes, score=15.0 required=5.0 tests=GTUBE,MISSING_HEADERS autolearn=no")
                    self.assertEqual(msg['Precedence'], "bulk")
                    
                    print("SUCCESS: Spam headers verified.")

if __name__ == "__main__":
    unittest.main()
