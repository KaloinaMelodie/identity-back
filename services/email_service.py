import os
import logging
import resend

logger = logging.getLogger(__name__)

class EmailService:
    @staticmethod
    def send_contact_email(
        sender_email: str,
        name: str,
        message: str
    ):
        try:
            resend_api_key = os.getenv("RESEND_API_KEY")
            receiver_email = os.getenv("CONTACT_RECEIVER_EMAIL")
            
            if not all([resend_api_key, receiver_email]):
                missing = []
                if not resend_api_key: missing.append("RESEND_API_KEY")
                if not receiver_email: missing.append("CONTACT_RECEIVER_EMAIL")
                raise ValueError(f"Missing required environment variables: {', '.join(missing)}")

            logger.info(f"Sending email via Resend API")

            resend.api_key = resend_api_key
            
            params = {
                # Use Resend's test email for FROM - no verification needed!
                "from": "onboarding@resend.dev",
                "to": [receiver_email],
                "subject": "New Contact Message",
                "html": f"""
                    <h2>New contact received</h2>
                    <p><strong>Name:</strong> {name}</p>
                    <p><strong>Email:</strong> {sender_email}</p>
                    <p><strong>Message:</strong></p>
                    <p>{message}</p>
                """,
            }

            email = resend.Emails.send(params)
            logger.info(f"Email sent successfully via Resend: {email}")

        except Exception as e:
            logger.error(f"Failed to send email via Resend: {str(e)}", exc_info=True)
            raise