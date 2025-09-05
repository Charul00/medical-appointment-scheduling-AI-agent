"""
SMTP Email Service for Personal Email Integration
Replaces SendGrid with standard SMTP (Gmail, Outlook, etc.)
"""

import smtplib
import ssl
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email import encoders
import os
from pathlib import Path
from typing import Dict, Optional, List
import logging
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class SMTPEmailService:
    """SMTP Email service for sending emails via personal email accounts"""
    
    def __init__(self):
        """Initialize SMTP service with environment variables"""
        self.from_email = os.getenv('FROM_EMAIL', 'charulchim06@gmail.com')
        self.email_password = os.getenv('EMAIL_PASSWORD', '')
        self.smtp_server = os.getenv('SMTP_SERVER', 'smtp.gmail.com')
        self.smtp_port = int(os.getenv('SMTP_PORT', '587'))
        
        # Clinic information
        self.clinic_name = os.getenv('CLINIC_NAME', 'Valley Medical Center')
        self.clinic_phone = os.getenv('CLINIC_PHONE', '+1-555-MEDICAL')
        
        logger.info(f"SMTP Email Service initialized for {self.from_email}")
    
    def send_email(self, to_email: str, subject: str, body: str, 
                   html_body: Optional[str] = None, attachments: Optional[List[str]] = None) -> bool:
        """
        Send email via SMTP
        
        Args:
            to_email: Recipient email address
            subject: Email subject
            body: Plain text email body
            html_body: HTML email body (optional)
            attachments: List of file paths to attach (optional)
            
        Returns:
            bool: True if email sent successfully, False otherwise
        """
        try:
            # Create message
            msg = MIMEMultipart('alternative')
            msg['From'] = self.from_email
            msg['To'] = to_email
            msg['Subject'] = subject
            
            # Add plain text part
            text_part = MIMEText(body, 'plain')
            msg.attach(text_part)
            
            # Add HTML part if provided
            if html_body:
                html_part = MIMEText(html_body, 'html')
                msg.attach(html_part)
            
            # Add attachments if provided
            if attachments:
                for file_path in attachments:
                    if os.path.exists(file_path):
                        self._add_attachment(msg, file_path)
                    else:
                        logger.warning(f"Attachment not found: {file_path}")
            
            # Create SMTP session
            server = smtplib.SMTP(self.smtp_server, self.smtp_port)
            server.starttls()  # Enable security
            
            # Login and send email
            server.login(self.from_email, self.email_password)
            text = msg.as_string()
            server.sendmail(self.from_email, to_email, text)
            server.quit()
            
            logger.info(f"Email sent successfully to {to_email}")
            return True
            
        except Exception as e:
            logger.error(f"Failed to send email to {to_email}: {str(e)}")
            return False
    
    def _add_attachment(self, msg: MIMEMultipart, file_path: str):
        """Add file attachment to email message"""
        try:
            with open(file_path, "rb") as attachment:
                part = MIMEBase('application', 'octet-stream')
                part.set_payload(attachment.read())
            
            encoders.encode_base64(part)
            part.add_header(
                'Content-Disposition',
                f'attachment; filename= {os.path.basename(file_path)}'
            )
            msg.attach(part)
            
        except Exception as e:
            logger.error(f"Failed to add attachment {file_path}: {str(e)}")
    
    def send_appointment_confirmation(self, patient_data: Dict) -> bool:
        """
        Send appointment confirmation email with intake form
        
        Args:
            patient_data: Dictionary containing patient and appointment information
            
        Returns:
            bool: True if email sent successfully
        """
        try:
            from .email_templates import IntakeFormEmailTemplates
            
            templates = IntakeFormEmailTemplates(self.clinic_name, self.clinic_phone)
            email_content = templates.appointment_confirmation_with_intake_form(patient_data)
            
            # Create HTML version
            html_body = self._create_html_email(email_content['body'])
            
            # Add intake form attachment if available
            attachments = []
            intake_form_path = patient_data.get('intake_form_pdf_path')
            if intake_form_path and os.path.exists(intake_form_path):
                attachments.append(intake_form_path)
            
            return self.send_email(
                to_email=patient_data.get('email', ''),
                subject=email_content['subject'],
                body=email_content['body'],
                html_body=html_body,
                attachments=attachments
            )
            
        except Exception as e:
            logger.error(f"Failed to send appointment confirmation: {str(e)}")
            return False
    
    def send_intake_form_reminder(self, patient_data: Dict) -> bool:
        """Send intake form completion reminder"""
        try:
            from .email_templates import IntakeFormEmailTemplates
            
            templates = IntakeFormEmailTemplates(self.clinic_name, self.clinic_phone)
            email_content = templates.intake_form_reminder(patient_data)
            
            html_body = self._create_html_email(email_content['body'])
            
            return self.send_email(
                to_email=patient_data.get('email', ''),
                subject=email_content['subject'],
                body=email_content['body'],
                html_body=html_body
            )
            
        except Exception as e:
            logger.error(f"Failed to send intake form reminder: {str(e)}")
            return False
    
    def send_intake_form_email(self, patient_data: Dict, appointment_data: Dict, 
                              form_file_path: str = None) -> bool:
        """Send intake form to patient with optional form attachment"""
        try:
            from .email_templates import IntakeFormEmailTemplates
            
            templates = IntakeFormEmailTemplates(self.clinic_name, self.clinic_phone)
            
            # Prepare combined data for email template
            combined_data = {**patient_data, **appointment_data}
            email_content = templates.intake_form_email(combined_data)
            
            html_body = self._create_html_email(email_content['body'])
            
            # Send email with optional attachment
            success = self.send_email(
                to_email=patient_data.get('email', ''),
                subject=email_content['subject'],
                body=email_content['body'],
                html_body=html_body,
                attachment_path=form_file_path
            )
            
            if success:
                logger.info(f"Intake form email sent successfully to {patient_data.get('name', 'patient')}")
            else:
                logger.warning(f"Failed to send intake form email to {patient_data.get('name', 'patient')}")
                
            return success
            
        except Exception as e:
            logger.error(f"Failed to send intake form email: {str(e)}")
            return False
    
    def send_intake_form_confirmation(self, patient_data: Dict) -> bool:
        """Send intake form received confirmation"""
        try:
            from .email_templates import IntakeFormEmailTemplates
            
            templates = IntakeFormEmailTemplates(self.clinic_name, self.clinic_phone)
            email_content = templates.intake_form_received_confirmation(patient_data)
            
            html_body = self._create_html_email(email_content['body'])
            
            return self.send_email(
                to_email=patient_data.get('email', ''),
                subject=email_content['subject'],
                body=email_content['body'],
                html_body=html_body
            )
            
        except Exception as e:
            logger.error(f"Failed to send intake form confirmation: {str(e)}")
            return False
    
    def _create_html_email(self, text_body: str) -> str:
        """Convert plain text email to HTML format"""
        # Simple HTML conversion - replace newlines with <br> and add basic styling
        html_body = text_body.replace('\n', '<br>')
        
        html_template = f"""
        <!DOCTYPE html>
        <html>
        <head>
            <meta charset="UTF-8">
            <style>
                body {{ font-family: Arial, sans-serif; line-height: 1.6; color: #333; }}
                .header {{ background-color: #f8f9fa; padding: 20px; border-radius: 5px; margin-bottom: 20px; }}
                .content {{ padding: 20px; }}
                .footer {{ background-color: #f8f9fa; padding: 15px; margin-top: 20px; font-size: 12px; color: #666; }}
                .important {{ background-color: #fff3cd; padding: 15px; border-left: 4px solid #ffc107; margin: 15px 0; }}
                .appointment-details {{ background-color: #e7f3ff; padding: 15px; border-radius: 5px; margin: 15px 0; }}
            </style>
        </head>
        <body>
            <div class="header">
                <h2 style="color: #0056b3; margin: 0;">{self.clinic_name}</h2>
            </div>
            <div class="content">
                {html_body}
            </div>
            <div class="footer">
                <p><strong>{self.clinic_name}</strong><br>
                Phone: {self.clinic_phone}<br>
                This is an automated message. Please do not reply to this email.</p>
            </div>
        </body>
        </html>
        """
        
        return html_template
    
    def send_appointment_reminder(self, appointment_data: Dict, reminder_type: str = "regular", 
                                reminder_timing: str = "24h") -> bool:
        """Send appointment reminder email"""
        try:
            from .email_templates import AppointmentReminderTemplates
            
            templates = AppointmentReminderTemplates(self.clinic_name, self.clinic_phone)
            
            if reminder_type == "regular":
                email_content = templates.regular_appointment_reminder(appointment_data, reminder_timing)
            elif reminder_type == "form_check":
                email_content = templates.form_completion_reminder(appointment_data)
            elif reminder_type == "confirmation":
                email_content = templates.visit_confirmation_reminder(appointment_data)
            else:
                logger.error(f"Unknown reminder type: {reminder_type}")
                return False
            
            html_body = self._create_html_email(email_content['body'])
            
            success = self.send_email(
                to_email=appointment_data.get('patient_email', ''),
                subject=email_content['subject'],
                body=email_content['body'],
                html_body=html_body
            )
            
            if success:
                logger.info(f"Appointment reminder ({reminder_type}) sent successfully to {appointment_data.get('patient_name', 'patient')}")
            else:
                logger.warning(f"Failed to send appointment reminder ({reminder_type}) to {appointment_data.get('patient_name', 'patient')}")
                
            return success
            
        except Exception as e:
            logger.error(f"Failed to send appointment reminder: {str(e)}")
            return False
    
    def send_sms_reminder(self, appointment_data: Dict, reminder_type: str = "regular") -> bool:
        """Send SMS reminder using enhanced SMS service"""
        try:
            from .email_templates import AppointmentReminderTemplates
            from .sms_service import SMSService
            
            templates = AppointmentReminderTemplates(self.clinic_name, self.clinic_phone)
            sms_message = templates.sms_templates(appointment_data, reminder_type)
            
            # Initialize SMS service
            sms_service = SMSService()  # Uses simulated by default
            
            # Send SMS
            result = sms_service.send_sms(
                to_phone=appointment_data.get('patient_phone', ''),
                message=sms_message,
                appointment_id=appointment_data.get('appointment_id', '')
            )
            
            if result['success']:
                logger.info(f"SMS reminder ({reminder_type}) sent successfully to {appointment_data.get('patient_name', 'patient')}")
                if result['provider'] == 'simulated':
                    logger.info(f"SMS Content Preview: {sms_message[:100]}...")
                return True
            else:
                logger.warning(f"Failed to send SMS reminder: {result.get('error', 'Unknown error')}")
                return False
            
        except Exception as e:
            logger.error(f"Failed to send SMS reminder: {str(e)}")
            return False
    
    def test_connection(self) -> bool:
        """Test SMTP connection and authentication"""
        try:
            server = smtplib.SMTP(self.smtp_server, self.smtp_port)
            server.starttls()
            server.login(self.from_email, self.email_password)
            server.quit()
            
            logger.info("SMTP connection test successful")
            return True
            
        except Exception as e:
            logger.error(f"SMTP connection test failed: {str(e)}")
            logger.info("Make sure you have:")
            logger.info("1. Set up 2-factor authentication on your Gmail account")
            logger.info("2. Generated an App Password for this application")
            logger.info("3. Set EMAIL_PASSWORD environment variable to your App Password")
            return False


# Example usage and testing
if __name__ == "__main__":
    # Load environment variables
    from dotenv import load_dotenv
    load_dotenv('.env.example')
    
    # Initialize email service
    email_service = SMTPEmailService()
    
    # Test connection
    print("Testing SMTP connection...")
    if email_service.test_connection():
        print("✅ SMTP connection successful!")
        
        # Test sending appointment confirmation
        patient_data = {
            "first_name": "John",
            "last_name": "Doe",
            "email": "charulchim06@gmail.com",  # Your email for testing
            "appointment_date": "September 10, 2025",
            "appointment_time": "10:00 AM",
            "doctor_name": "Dr. Emily Smith",
            "clinic_address": "123 Health St, Medical City, MC 12345",
            "intake_form_link": "https://clinic.example.com/intake/12345"
        }
        
        print("Sending test appointment confirmation...")
        if email_service.send_appointment_confirmation(patient_data):
            print("✅ Test email sent successfully!")
        else:
            print("❌ Failed to send test email")
    else:
        print("❌ SMTP connection failed")
        print("\nTo use Gmail with your personal email:")
        print("1. Enable 2-factor authentication on your Gmail account")
        print("2. Generate an App Password: https://myaccount.google.com/apppasswords")
        print("3. Set EMAIL_PASSWORD in your .env file to the App Password")
