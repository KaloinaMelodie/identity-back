import os
import logging
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail

logger = logging.getLogger(__name__)

class EmailService:
    @staticmethod
    def send_contact_email(
        sender_email: str,
        name: str,
        message: str
    ):
        try:
            sendgrid_api_key = os.getenv("SENDGRID_API_KEY")
            receiver_email = os.getenv("CONTACT_RECEIVER_EMAIL")
            from_email = os.getenv("FROM_EMAIL")
            
            if not all([sendgrid_api_key, receiver_email, from_email]):
                raise ValueError("Missing SendGrid configuration")

            logger.info("Sending email via SendGrid API")

            message_obj = Mail(
                from_email=from_email,
                to_emails=receiver_email,
                subject="New Contact Message",
                html_content=f"""
                    <h2>New contact received</h2>
                    <p><strong>Name:</strong> {name}</p>
                    <p><strong>Email:</strong> {sender_email}</p>
                    <p><strong>Message:</strong></p>
                    <p>{message}</p>
                """
            )
            
            sg = SendGridAPIClient(sendgrid_api_key)
            response = sg.send(message_obj)
            logger.info(f"Email sent via SendGrid: {response.status_code}")

        except Exception as e:
            logger.error(f"Failed to send email via SendGrid: {str(e)}", exc_info=True)
            raise