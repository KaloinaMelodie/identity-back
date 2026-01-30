import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import os

class EmailService:
    @staticmethod
    def send_contact_email(
        sender_email: str,
        name: str,
        message: str
    ):
        smtp_host = os.getenv("SMTP_HOST")
        smtp_port = int(os.getenv("SMTP_PORT", 587))
        smtp_user = os.getenv("SMTP_USER")
        smtp_password = os.getenv("SMTP_PASSWORD")
        receiver_email = os.getenv("CONTACT_RECEIVER_EMAIL")

        msg = MIMEMultipart()
        msg["From"] = smtp_user
        msg["To"] = receiver_email
        msg["Subject"] = "New Contact Message"

        body = f"""
New contact received:

Name: {name}
Email: {sender_email}

Message:
{message}
        """

        msg.attach(MIMEText(body, "plain"))

        with smtplib.SMTP(smtp_host, smtp_port) as server:
            server.starttls()
            server.login(smtp_user, smtp_password)
            server.send_message(msg)
