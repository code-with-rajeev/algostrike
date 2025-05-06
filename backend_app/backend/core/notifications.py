"""
This code demonstrates how to send notifications via email.
"""

import smtplib
from email.mime.text import MIMEText
import os

# Email configuration
SMTP_SERVER = "smtp.gmail.com"
SMTP_PORT = 587
EMAIL_USER = os.environ.get("HOST_MAIL")
EMAIL_PASS = os.environ.get("HOST_MAIL_PASSWORD")

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

        #print(f"Email sent to {to_email}")

    except Exception as e:
        # Email doesn't exist error ?
        raise
        #print(f"Failed to send email: {str(e)}")

def authentication_otp_mail(username, to_email, otp):
    """
    Sends an OTP via email notification.
    """
    message = f"Dear {username},\nYour One-Time Password(OTP) for Algostrike is {otp}.\nThis OTP is valid for 5 minutes. Please keep it confidenial for security reasons.\nIf you did not request this code, you can safely ignore this email.\nBest regards,\nTeam Algostrike\nwww.algostrike.com"
    try:
        msg = MIMEText(message)
        msg["Subject"] = "Your AlgoStrike verification OTP"
        msg["From"] = EMAIL_USER
        msg["To"] = to_email

        with smtplib.SMTP(SMTP_SERVER, SMTP_PORT) as server:
            server.starttls()
            server.login(EMAIL_USER, EMAIL_PASS)
            server.sendmail(EMAIL_USER, to_email, msg.as_string())

        #print(f"Email sent to {to_email}")

        # OTP sent successfully!

    except Exception as e:
        raise
        #print(f"Failed to send email: {str(e)}")