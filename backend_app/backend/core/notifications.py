"""
This code demonstrates how to send notifications via email.
"""

import smtplib
from email.mime.text import MIMEText
import os

# Email configuration
SMTP_SERVER = "smtp.gmail.com"
SMTP_PORT = 587
EMAIL_USER =os.environ.get("TEST_MAIL")
EMAIL_PASS = os.environ.get("TEST_MAIL_PASSWORD")

def send_email(to_email, subject, message):
    """
    Sends an email notification.
    """
    try:
        msg = MIMEText(message)
        msg["Subject"] = subject
        msg["From"] = EMAIL_USER
        msg["To"] = to_email

        with smtplib.SMTP(SMTP_SERVER, SMTP_PORT) as server:
            server.starttls()
            server.login(EMAIL_USER, EMAIL_PASS)
            server.sendmail(EMAIL_USER, to_email, msg.as_string())

        print(f"Email sent to {to_email}")

    except Exception as e:
        print(f"Failed to send email: {str(e)}")