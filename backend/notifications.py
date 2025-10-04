"""
Email and SMS notification service
"""

import os
import logging
from typing import Optional
import aiosmtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from twilio.rest import Client as TwilioClient
from config import settings

logger = logging.getLogger(__name__)

class EmailService:
    """Email notification service using SMTP"""
    
    def __init__(self):
        self.enabled = settings.email_enabled
        if not self.enabled:
            logger.warning("Email service disabled - SMTP credentials not configured")
    
    async def send_email( 
        self,
        to_email: str,
        subject: str,
        body: str,
        html_body: Optional[str] = None
    ) -> bool:
        """Send email notification"""
        if not self.enabled:
            logger.info(f"Email not sent (disabled): {subject} to {to_email}")
            return False
        
        try:
            message = MIMEMultipart('alternative')
            message['From'] = settings.SMTP_FROM
            message['To'] = to_email
            message['Subject'] = subject
            
            # Add plain text part
            text_part = MIMEText(body, 'plain')
            message.attach(text_part)
            
            # Add HTML part if provided
            if html_body:
                html_part = MIMEText(html_body, 'html')
                message.attach(html_part)
            
            # Send email
            await aiosmtplib.send(
                message,
                hostname=settings.SMTP_HOST,
                port=settings.SMTP_PORT,
                username=settings.SMTP_USER,
                password=settings.SMTP_PASSWORD,
                start_tls=True,
            )
            
            logger.info(f"Email sent successfully to {to_email}")
            return True
        
        except Exception as e:
            logger.error(f"Failed to send email to {to_email}: {e}")
            return False

class SMSService:
    """SMS notification service using Twilio"""
    
    def __init__(self):
        self.enabled = settings.sms_enabled
        if self.enabled:
            self.client = TwilioClient(
                settings.TWILIO_ACCOUNT_SID,
                settings.TWILIO_AUTH_TOKEN
            )
        else:
            logger.warning("SMS service disabled - Twilio credentials not configured")
    
    async def send_sms(self, to_phone: str, message: str) -> bool:
        """Send SMS notification"""
        if not self.enabled:
            logger.info(f"SMS not sent (disabled): {message[:50]}... to {to_phone}")
            return False
        
        try:
            self.client.messages.create(
                body=message,
                from_=settings.TWILIO_PHONE_NUMBER,
                to=to_phone
            )
            
            logger.info(f"SMS sent successfully to {to_phone}")
            return True
        
        except Exception as e:
            logger.error(f"Failed to send SMS to {to_phone}: {e}")
            return False

class NotificationService:
    """Unified notification service"""
    
    def __init__(self):
        self.email_service = EmailService()
        self.sms_service = SMSService()
    
    async def notify_ticket_created(
        self,
        ticket_id: str,
        employee: str,
        subject: str,
        priority: str,
        category: str,
        assigned_team: str,
        from_email: Optional[str] = None
    ):
        """Send notification when ticket is created"""
        # Extract email from employee string (format: "Name (ID)")
        email = self._extract_email(employee)
        
        # Email notification
        email_subject = f"Ticket Created: {subject}"
        email_body = f"""
Hello,

Your IT support ticket has been created successfully.

Ticket ID: {ticket_id}
Subject: {subject}
Priority: {priority.upper()}
Category: {category.title()}
Assigned Team: {assigned_team}

You will receive updates as your ticket progresses.

To view your ticket status, please visit the IT Support Portal.

Thank you,
POWERGRID IT Support Team
        """
        
        html_body = f"""
        <html>
        <body style="font-family: Arial, sans-serif; line-height: 1.6; color: #333;">
            <h2 style="color: #6366f1;">Ticket Created Successfully</h2>
            <p>Hello,</p>
            <p>Your IT support ticket has been created successfully.</p>
            
            <div style="background-color: #f5f5f5; padding: 15px; border-radius: 5px; margin: 20px 0;">
                <p style="margin: 5px 0;"><strong>Ticket ID:</strong> {ticket_id}</p>
                <p style="margin: 5px 0;"><strong>Subject:</strong> {subject}</p>
                <p style="margin: 5px 0;"><strong>Priority:</strong> <span style="color: {'#ef4444' if priority == 'high' else '#f59e0b' if priority == 'medium' else '#10b981'};">{priority.upper()}</span></p>
                <p style="margin: 5px 0;"><strong>Category:</strong> {category.title()}</p>
                <p style="margin: 5px 0;"><strong>Assigned Team:</strong> {assigned_team}</p>
            </div>
            
            <p>You will receive updates as your ticket progresses.</p>
            <p>To view your ticket status, please visit the IT Support Portal.</p>
            
            <p style="margin-top: 30px;">Thank you,<br>POWERGRID IT Support Team</p>
        </body>
        </html>
        """
        # If a specific From address is provided (e.g., chatbot), use it
        if from_email:
            # Temporarily override the SMTP_FROM for this message
            original_from = settings.SMTP_FROM
            settings.SMTP_FROM = from_email

        try:
            await self.email_service.send_email(email, email_subject, email_body, html_body)
            logger.info(f"Ticket creation notification sent for {ticket_id}")
        finally:
            if from_email:
                # Restore original
                settings.SMTP_FROM = original_from
    
    async def notify_ticket_updated(
        self,
        ticket_id: str,
        employee: str,
        subject: str,
        old_status: str,
        new_status: str
    ):
        """Send notification when ticket status is updated"""
        email = self._extract_email(employee)
        
        email_subject = f"Ticket Updated: {subject}"
        email_body = f"""
Hello,

Your IT support ticket status has been updated.

Ticket ID: {ticket_id}
Subject: {subject}
Previous Status: {old_status.replace('_', ' ').title()}
New Status: {new_status.replace('_', ' ').title()}

To view your ticket details, please visit the IT Support Portal.

Thank you,
POWERGRID IT Support Team
        """
        
        html_body = f"""
        <html>
        <body style="font-family: Arial, sans-serif; line-height: 1.6; color: #333;">
            <h2 style="color: #6366f1;">Ticket Status Updated</h2>
            <p>Hello,</p>
            <p>Your IT support ticket status has been updated.</p>
            
            <div style="background-color: #f5f5f5; padding: 15px; border-radius: 5px; margin: 20px 0;">
                <p style="margin: 5px 0;"><strong>Ticket ID:</strong> {ticket_id}</p>
                <p style="margin: 5px 0;"><strong>Subject:</strong> {subject}</p>
                <p style="margin: 5px 0;"><strong>Previous Status:</strong> {old_status.replace('_', ' ').title()}</p>
                <p style="margin: 5px 0;"><strong>New Status:</strong> <span style="color: #10b981;">{new_status.replace('_', ' ').title()}</span></p>
            </div>
            
            <p>To view your ticket details, please visit the IT Support Portal.</p>
            
            <p style="margin-top: 30px;">Thank you,<br>POWERGRID IT Support Team</p>
        </body>
        </html>
        """

        await self.email_service.send_email(email, email_subject, email_body, html_body)

        # Send SMS for resolved tickets
        if new_status == 'resolved':
            phone = self._extract_phone(employee)
            if phone:
                sms_message = f"POWERGRID IT: Your ticket #{ticket_id[:8]} has been resolved. Thank you!"
                await self.sms_service.send_sms(phone, sms_message)

        logger.info(f"Ticket update notification sent for {ticket_id}")
    
    def _extract_email(self, employee: str) -> str:
        """Extract email from employee string or generate default"""
        # If a test override is configured, always send to that address
        if getattr(settings, 'TEST_NOTIFICATION_EMAIL', None):
            return settings.TEST_NOTIFICATION_EMAIL

        # For demo purposes, generate email from employee name
        # In production, this would query the employee database
        if '@' in employee:
            return employee

        # Extract name and generate email
        name = employee.split('(')[0].strip()
        email_name = name.lower().replace(' ', '.')
        return f"{email_name}@gmail.com"
    
    def _extract_phone(self, employee: str) -> Optional[str]:
        """Extract phone number from employee string"""
        # In production, this would query the employee database
        # For demo, return None (SMS won't be sent)
        return None

# Global notification service instance
_notification_service = None

def get_notification_service() -> NotificationService:
    """Get or create notification service instance (singleton pattern)"""
    global _notification_service
    if _notification_service is None:
        _notification_service = NotificationService()
    return _notification_service
