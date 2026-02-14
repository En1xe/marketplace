import aiosmtplib

from email.mime.text import MIMEText

from core.exceptions import SMTPException
from core.config import settings
from core.logging import get_logger


logger = get_logger(__name__)

async def send_email_async(
        to_email: str,
        subject: str,
        body: str,
    ):
        """Sends email asynchronously via an SMTP server"""
        logger.info('Sending an email')
        
        message = MIMEText(body)
        message['From'] = settings.SMTP_USERNAME
        message['To'] = to_email
        message['Subject'] = subject

        try:
            await aiosmtplib.send(
                message,
                hostname=settings.SMTP_SERVER,
                port=settings.SMTP_PORT,
                username=settings.SMTP_USERNAME,
                password=settings.SMTP_PASSWORD,
                use_tls=True,
            )
            logger.info('The email was sent successfully')
        except:
            logger.error('The email was not sent')
            raise SMTPException
        