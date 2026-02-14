import pytest

from utils.emails import *


class TestUtilsEmails:
    
    @pytest.mark.asyncio
    async def test_send_email_async(
        self,
        mocker
    ):
        mock_settings = mocker.patch('utils.emails.settings')
        mock_settings.SMTP_SERVER = 'smtp.test.com'
        mock_settings.SMTP_PORT = 587
        mock_settings.SMTP_USERNAME = 'test@example.com'
        mock_settings.SMTP_PASSWORD = 'password123'
        
        mock_message = mocker.Mock()
        mock_message.__setitem__ = mocker.Mock()
        mocker.patch('utils.emails.MIMEText', return_value=mock_message)
        
        mock_send = mocker.patch('utils.emails.aiosmtplib.send', return_value=None)
        
        await send_email_async(
            to_email='Email',
            subject='Subject',
            body='Body'
        )
        
        mock_send.assert_awaited_once_with(
            mock_message,
            hostname='smtp.test.com',
            port=587,
            username='test@example.com',
            password='password123'
        )
        
        
        
        