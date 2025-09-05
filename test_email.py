#!/usr/bin/env python3
"""
Test the SMTP Email Service with Personal Email
"""

import sys
import os
from pathlib import Path

# Add src to path for imports
current_dir = Path(__file__).parent
sys.path.append(str(current_dir / 'src'))

def test_email_service():
    """Test the SMTP email service"""
    
    print("🧪 Testing Personal Email Integration")
    print("="*50)
    
    try:
        from utils.smtp_email_service import SMTPEmailService
        print("✅ Successfully imported SMTPEmailService")
    except ImportError as e:
        print(f"❌ Failed to import email service: {e}")
        return
    
    # Initialize email service
    email_service = SMTPEmailService()
    
    print(f"📧 Email Service Configuration:")
    print(f"   From Email: {email_service.from_email}")
    print(f"   SMTP Server: {email_service.smtp_server}")
    print(f"   SMTP Port: {email_service.smtp_port}")
    print(f"   Clinic Name: {email_service.clinic_name}")
    
    # Test connection (only if password is set)
    if email_service.email_password:
        print("\n🔗 Testing SMTP Connection...")
        if email_service.test_connection():
            print("✅ SMTP connection successful!")
            
            # Test sending email
            print("\n📬 Testing email sending...")
            
            patient_data = {
                "first_name": "Test",
                "last_name": "Patient",
                "email": "charulchim06@gmail.com",  # Your email
                "appointment_date": "September 10, 2025",
                "appointment_time": "2:00 PM",
                "doctor_name": "Dr. Emily Smith",
                "clinic_address": "123 Health St, Medical City, MC 12345",
                "intake_form_link": "https://clinic.example.com/intake/test123"
            }
            
            if email_service.send_appointment_confirmation(patient_data):
                print("✅ Test appointment confirmation email sent!")
                print(f"📨 Check your inbox at {patient_data['email']}")
            else:
                print("❌ Failed to send test email")
                
        else:
            print("❌ SMTP connection failed")
    else:
        print("\n⚠️  EMAIL_PASSWORD not configured")
        print("To enable email functionality:")
        print("1. Set up 2-factor authentication on Gmail")
        print("2. Generate App Password: https://myaccount.google.com/apppasswords")
        print("3. Add EMAIL_PASSWORD=your_app_password to .env file")
    
    print("\n📝 Current .env configuration:")
    env_file = Path(".env.example")
    if env_file.exists():
        print("✅ .env.example file found")
        with open(env_file) as f:
            for line in f:
                if "EMAIL" in line or "SMTP" in line:
                    print(f"   {line.strip()}")
    else:
        print("❌ .env.example file not found")

def test_agent_with_email():
    """Test the scheduling agent with email integration"""
    
    print("\n🤖 Testing Scheduling Agent with Email")
    print("="*50)
    
    try:
        from agents.scheduling_agent import MedicalSchedulingAgent
        agent = MedicalSchedulingAgent()
        
        print("✅ Scheduling agent initialized")
        
        if agent.email_service:
            print("✅ Email service loaded successfully")
            print("📧 Email integration: ENABLED")
        else:
            print("⚠️  Email service not available")
            print("📧 Email integration: DISABLED")
        
        # Test intake form sending
        print("\n📋 Testing intake form sending...")
        response = agent._send_intake_form("patient_email=charulchim06@gmail.com")
        print(f"Response: {response}")
        
    except ImportError as e:
        print(f"❌ Failed to import scheduling agent: {e}")
    except Exception as e:
        print(f"❌ Error testing agent: {e}")

if __name__ == "__main__":
    print("🏥 Medical Scheduling System - Email Integration Test")
    print("Using Personal Email: charulchim06@gmail.com")
    print("No SendGrid Required!")
    print("\n")
    
    test_email_service()
    test_agent_with_email()
    
    print("\n✨ Email Integration Summary:")
    print("• ✅ Personal Gmail integration configured")
    print("• ✅ SMTP service replaces SendGrid")
    print("• ✅ No external API keys needed (except Gmail App Password)")
    print("• ✅ HTML email templates with clinic branding")
    print("• ✅ Appointment confirmations and intake forms")
    print("\nTo complete setup:")
    print("1. Enable 2FA on your Gmail account")
    print("2. Generate App Password for this application")
    print("3. Set EMAIL_PASSWORD in your .env file")
    print("4. Test by running this script again")
