"""
SMS Service Integration for Medical Appointment Reminders
"""

import logging
from typing import Dict, Optional
import os

logger = logging.getLogger(__name__)


class SMSService:
    """
    SMS service for sending appointment reminders
    Currently simulated - can be extended with real SMS providers
    """
    
    def __init__(self, provider: str = "simulated"):
        self.provider = provider
        self.is_real_service = False
        
        # Initialize based on provider
        if provider == "twilio":
            self._init_twilio()
        elif provider == "aws_sns":
            self._init_aws_sns()
        elif provider == "simulated":
            self._init_simulated()
        else:
            logger.warning(f"Unknown SMS provider: {provider}, using simulated")
            self._init_simulated()
    
    def _init_simulated(self):
        """Initialize simulated SMS service"""
        self.is_real_service = False
        logger.info("SMS Service initialized in SIMULATION mode")
        logger.info("To enable real SMS:")
        logger.info("1. Install provider: pip install twilio")
        logger.info("2. Set environment variables: TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN, TWILIO_PHONE_NUMBER")
        logger.info("3. Change provider to 'twilio' in configuration")
    
    def _init_twilio(self):
        """Initialize Twilio SMS service"""
        try:
            from twilio.rest import Client
            
            account_sid = os.getenv('TWILIO_ACCOUNT_SID')
            auth_token = os.getenv('TWILIO_AUTH_TOKEN')
            self.from_phone = os.getenv('TWILIO_PHONE_NUMBER')
            
            if not all([account_sid, auth_token, self.from_phone]):
                logger.error("Twilio credentials not found in environment variables")
                logger.error("Required: TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN, TWILIO_PHONE_NUMBER")
                self._init_simulated()
                return
            
            self.client = Client(account_sid, auth_token)
            self.is_real_service = True
            logger.info("Twilio SMS Service initialized successfully")
            
        except ImportError:
            logger.error("Twilio not installed. Install with: pip install twilio")
            self._init_simulated()
        except Exception as e:
            logger.error(f"Failed to initialize Twilio: {e}")
            self._init_simulated()
    
    def _init_aws_sns(self):
        """Initialize AWS SNS SMS service"""
        try:
            import boto3
            
            self.sns_client = boto3.client('sns')
            self.is_real_service = True
            logger.info("AWS SNS SMS Service initialized successfully")
            
        except ImportError:
            logger.error("boto3 not installed. Install with: pip install boto3")
            self._init_simulated()
        except Exception as e:
            logger.error(f"Failed to initialize AWS SNS: {e}")
            self._init_simulated()
    
    def send_sms(self, to_phone: str, message: str, appointment_id: str = None) -> Dict:
        """
        Send SMS message
        
        Args:
            to_phone: Recipient phone number
            message: SMS message content
            appointment_id: Optional appointment ID for tracking
            
        Returns:
            Dictionary with send result
        """
        if not to_phone:
            return {
                "success": False,
                "error": "No phone number provided",
                "provider": self.provider
            }
        
        # Clean phone number
        clean_phone = self._clean_phone_number(to_phone)
        
        if self.provider == "twilio" and self.is_real_service:
            return self._send_twilio_sms(clean_phone, message, appointment_id)
        elif self.provider == "aws_sns" and self.is_real_service:
            return self._send_aws_sns_sms(clean_phone, message, appointment_id)
        else:
            return self._send_simulated_sms(clean_phone, message, appointment_id)
    
    def _send_twilio_sms(self, to_phone: str, message: str, appointment_id: str = None) -> Dict:
        """Send SMS via Twilio"""
        try:
            message_obj = self.client.messages.create(
                body=message,
                from_=self.from_phone,
                to=to_phone
            )
            
            logger.info(f"Twilio SMS sent successfully. SID: {message_obj.sid}")
            return {
                "success": True,
                "provider": "twilio",
                "message_sid": message_obj.sid,
                "to": to_phone,
                "appointment_id": appointment_id
            }
            
        except Exception as e:
            logger.error(f"Failed to send Twilio SMS: {e}")
            return {
                "success": False,
                "error": str(e),
                "provider": "twilio",
                "to": to_phone,
                "appointment_id": appointment_id
            }
    
    def _send_aws_sns_sms(self, to_phone: str, message: str, appointment_id: str = None) -> Dict:
        """Send SMS via AWS SNS"""
        try:
            response = self.sns_client.publish(
                PhoneNumber=to_phone,
                Message=message
            )
            
            logger.info(f"AWS SNS SMS sent successfully. MessageId: {response.get('MessageId')}")
            return {
                "success": True,
                "provider": "aws_sns",
                "message_id": response.get('MessageId'),
                "to": to_phone,
                "appointment_id": appointment_id
            }
            
        except Exception as e:
            logger.error(f"Failed to send AWS SNS SMS: {e}")
            return {
                "success": False,
                "error": str(e),
                "provider": "aws_sns",
                "to": to_phone,
                "appointment_id": appointment_id
            }
    
    def _send_simulated_sms(self, to_phone: str, message: str, appointment_id: str = None) -> Dict:
        """Simulate SMS sending"""
        logger.info(f"📱 SIMULATED SMS to {to_phone}")
        logger.info(f"📄 Message content:")
        logger.info(f"{message}")
        logger.info(f"📋 Appointment ID: {appointment_id}")
        logger.info("=" * 50)
        
        return {
            "success": True,
            "provider": "simulated",
            "to": to_phone,
            "appointment_id": appointment_id,
            "message": "SMS simulated successfully"
        }
    
    def _clean_phone_number(self, phone: str) -> str:
        """Clean and format phone number"""
        if not phone:
            return ""
        
        # Remove all non-digit characters
        digits_only = ''.join(filter(str.isdigit, phone))
        
        # Add country code if missing (assume US)
        if len(digits_only) == 10:
            digits_only = "1" + digits_only
        
        # Format as +1xxxxxxxxxx
        if len(digits_only) == 11 and digits_only.startswith('1'):
            return f"+{digits_only}"
        
        return phone  # Return original if can't format
    
    def get_delivery_status(self, message_id: str) -> Dict:
        """Get delivery status of sent message"""
        if self.provider == "twilio" and self.is_real_service:
            try:
                message = self.client.messages(message_id).fetch()
                return {
                    "status": message.status,
                    "error_code": message.error_code,
                    "error_message": message.error_message
                }
            except Exception as e:
                return {"status": "unknown", "error": str(e)}
        
        elif self.provider == "simulated":
            return {
                "status": "delivered",
                "message": "Simulated delivery successful"
            }
        
        return {"status": "unknown", "message": "Status check not supported for this provider"}


# Configuration class for easy SMS setup
class SMSConfig:
    """Configuration helper for SMS service"""
    
    @staticmethod
    def get_recommended_provider() -> str:
        """Get recommended SMS provider based on available credentials"""
        # Check for Twilio credentials
        if all([
            os.getenv('TWILIO_ACCOUNT_SID'),
            os.getenv('TWILIO_AUTH_TOKEN'),
            os.getenv('TWILIO_PHONE_NUMBER')
        ]):
            return "twilio"
        
        # Check for AWS credentials
        try:
            import boto3
            # Try to create SNS client to test credentials
            boto3.client('sns')
            return "aws_sns"
        except:
            pass
        
        return "simulated"
    
    @staticmethod
    def setup_instructions(provider: str = None) -> str:
        """Get setup instructions for SMS provider"""
        if not provider:
            provider = SMSConfig.get_recommended_provider()
        
        if provider == "twilio":
            return """
🔧 TWILIO SMS SETUP INSTRUCTIONS:

1. Sign up at https://www.twilio.com/
2. Get your Account SID, Auth Token, and Phone Number
3. Set environment variables:
   export TWILIO_ACCOUNT_SID="your_account_sid"
   export TWILIO_AUTH_TOKEN="your_auth_token"
   export TWILIO_PHONE_NUMBER="+1234567890"
4. Install Twilio: pip install twilio
5. Restart the application

💰 Pricing: ~$0.0075 per SMS in the US
"""
        
        elif provider == "aws_sns":
            return """
🔧 AWS SNS SMS SETUP INSTRUCTIONS:

1. Set up AWS account and configure AWS CLI
2. Create IAM user with SNS permissions
3. Configure AWS credentials:
   aws configure
   (or set AWS_ACCESS_KEY_ID and AWS_SECRET_ACCESS_KEY)
4. Install boto3: pip install boto3
5. Restart the application

💰 Pricing: ~$0.00645 per SMS in the US
"""
        
        else:
            return """
🔧 CURRENT: SIMULATED SMS MODE

✅ Advantages:
- No cost, no setup required
- Perfect for testing and demos
- All SMS content is logged

⚠️ Limitations:
- No actual SMS messages sent
- Patients won't receive real notifications

🚀 To enable real SMS, choose a provider:
- Twilio (recommended for small-medium practices)
- AWS SNS (good for larger enterprises)
"""
