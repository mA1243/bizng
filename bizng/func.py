import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from dotenv import load_dotenv
from os import getenv

load_dotenv()

SMTP_SERVER = "smtp.gmail.com"  # Corrected SMTP server for Gmail
SMTP_PORT = 465  # SSL port
EMAIL = getenv("EMAIL_USERNAME")
PASSWORD = getenv("EMAIL_PASSWORD")  # Your Gmail password or app-specific password

def send_email(from_email, name, subject, message):
    try:
        msg = MIMEMultipart()
        # Set the "From" field to your Gmail account
        msg["From"] = EMAIL
        msg["To"] = EMAIL
        msg["Subject"] = subject
        # Add the "Reply-To" field to reflect the sender's email
        msg["Reply-To"] = from_email

        # Format the email body
        formatted_message = f"Good day Jammy,\n\n{message}\n\nRegards,\n{name}"
        msg.attach(MIMEText(formatted_message, "plain"))

        # Use SMTP_SSL for SSL connection
        with smtplib.SMTP_SSL(SMTP_SERVER, SMTP_PORT) as server:
            server.login(EMAIL, PASSWORD)
            server.sendmail(EMAIL, EMAIL, msg.as_string())

        return True
    except Exception as e:
        print(f"Error: {e}")
        return False