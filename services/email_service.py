import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import os
import logging

logger = logging.getLogger(__name__)

class EmailService:
    @staticmethod
    def send_contact_email(
        sender_email: str,
        name: str,
        message: str
    ):
        try:
            smtp_host = os.getenv("SMTP_HOST")
            smtp_port = int(os.getenv("SMTP_PORT", 587))
            smtp_user = os.getenv("SMTP_USER")
            smtp_password = os.getenv("SMTP_PASSWORD")
            receiver_email = os.getenv("CONTACT_RECEIVER_EMAIL")

            # Validate environment variables
            if not all([smtp_host, smtp_user, smtp_password, receiver_email]):
                missing = []
                if not smtp_host: missing.append("SMTP_HOST")
                if not smtp_user: missing.append("SMTP_USER")
                if not smtp_password: missing.append("SMTP_PASSWORD")
                if not receiver_email: missing.append("CONTACT_RECEIVER_EMAIL")
                raise ValueError(f"Missing required environment variables: {', '.join(missing)}")

            logger.info(f"Attempting to send email via {smtp_host}:{smtp_port}")

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

            with smtplib.SMTP(smtp_host, smtp_port, timeout=30) as server:
                logger.info("Connected to SMTP server")
                server.starttls()
                logger.info("TLS started")
                server.login(smtp_user, smtp_password)
                logger.info("Login successful")
                server.send_message(msg)
                logger.info(f"Email sent successfully to {receiver_email}")

        except smtplib.SMTPAuthenticationError as e:
            logger.error(f"SMTP Authentication failed: {str(e)}")
            raise
        except smtplib.SMTPException as e:
            logger.error(f"SMTP error occurred: {str(e)}")
            raise
        except Exception as e:
            logger.error(f"Unexpected error sending email: {str(e)}", exc_info=True)
            raise