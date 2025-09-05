"""
Email Templates for Appointment Management System
"""

from datetime import datetime, timedelta
from typing import Dict, Optional


class AppointmentReminderTemplates:
    """Email and SMS templates for appointment reminders"""
    
    def __init__(self, clinic_name: str = "Medical Clinic", clinic_phone: str = "(555) 123-4567"):
        self.clinic_name = clinic_name
        self.clinic_phone = clinic_phone
    
    def regular_appointment_reminder(self, appointment_data: Dict, reminder_timing: str = "24h") -> Dict[str, str]:
        """
        Regular appointment reminder template
        
        Args:
            appointment_data: Dictionary containing appointment information
            reminder_timing: When this reminder is sent (24h, 4h, 1h)
            
        Returns:
            Dictionary with email subject and body
        """
        timing_text = {
            "24h": "tomorrow",
            "4h": "in 4 hours", 
            "1h": "in 1 hour"
        }.get(reminder_timing, "soon")
        
        subject = f"📅 Appointment Reminder - {timing_text.title()} | {self.clinic_name}"
        
        body = f"""
🏥 **APPOINTMENT REMINDER**

Dear {appointment_data.get('patient_name', 'Patient')},

This is a friendly reminder about your upcoming appointment {timing_text}.

**APPOINTMENT DETAILS:**
📅 Date: {appointment_data.get('appointment_date', 'TBD')}
🕐 Time: {appointment_data.get('appointment_time', 'TBD')}
👨‍⚕️ Provider: Dr. {appointment_data.get('doctor_name', 'TBD')}
⏱️ Duration: {appointment_data.get('duration_minutes', 30)} minutes
📍 Location: {self.clinic_name} - Main Office
🆔 Appointment ID: {appointment_data.get('appointment_id', 'N/A')}

**PREPARATION CHECKLIST:**
✅ Bring photo ID and insurance card
✅ List of current medications
✅ Arrive 15 minutes early for check-in
{'✅ Complete intake forms (new patients)' if appointment_data.get('patient_type') == 'New Patient' else '✅ Brief check-in (returning patients)'}

**NEED TO RESCHEDULE?**
📞 Call us: {self.clinic_phone}
⏰ At least 24 hours notice required

**CONTACT INFO:**
📞 Main Office: {self.clinic_phone}
🚨 Emergency: (555) 999-8888

We look forward to seeing you {timing_text}!

Best regards,
{self.clinic_name} Team
"""
        
        return {"subject": subject, "body": body}
    
    def form_completion_reminder(self, appointment_data: Dict) -> Dict[str, str]:
        """
        Reminder asking if intake forms have been completed
        
        Args:
            appointment_data: Dictionary containing appointment information
            
        Returns:
            Dictionary with email subject and body
        """
        subject = f"📋 Have you completed your intake forms? | {self.clinic_name}"
        
        body = f"""
🏥 **INTAKE FORM COMPLETION CHECK**

Dear {appointment_data.get('patient_name', 'Patient')},

Your appointment is coming up soon! We want to make sure everything is ready for your visit.

**YOUR UPCOMING APPOINTMENT:**
📅 Date: {appointment_data.get('appointment_date', 'TBD')}
🕐 Time: {appointment_data.get('appointment_time', 'TBD')}
👨‍⚕️ Provider: Dr. {appointment_data.get('doctor_name', 'TBD')}

**INTAKE FORM STATUS CHECK:**
Have you completed your new patient intake forms yet?

**✅ COMPLETED FORMS?**
Great! You're all set. Just bring your ID and insurance card.

**❌ NOT COMPLETED YET?**
No worries! You can:
• Complete them online (link sent in your confirmation email)
• Print and fill out the attached form
• Arrive 15 minutes early to complete at our office

**QUICK COMPLETION OPTIONS:**
📱 Online Form: Check your confirmation email for the link
📄 Print Form: Download the attached PDF
🏥 At Office: Arrive early and we'll help you complete them

**NEED HELP?**
📞 Call us: {self.clinic_phone}
💬 Text: Reply to this message

**REPLY TO THIS MESSAGE:**
• Type "COMPLETED" if you've finished your forms
• Type "HELP" if you need assistance
• Type "PRINT" if you need the forms resent

We want to ensure your appointment runs smoothly and on time!

Best regards,
{self.clinic_name} Team
"""
        
        return {"subject": subject, "body": body}
    
    def visit_confirmation_reminder(self, appointment_data: Dict) -> Dict[str, str]:
        """
        Final reminder asking for visit confirmation or cancellation reason
        
        Args:
            appointment_data: Dictionary containing appointment information
            
        Returns:
            Dictionary with email subject and body
        """
        subject = f"🔔 Final Reminder - Confirm or Cancel Your Appointment | {self.clinic_name}"
        
        body = f"""
🏥 **FINAL APPOINTMENT CONFIRMATION**

Dear {appointment_data.get('patient_name', 'Patient')},

Your appointment is scheduled for very soon. Please confirm your attendance or let us know if you need to cancel.

**YOUR APPOINTMENT:**
📅 **TODAY** - {appointment_data.get('appointment_date', 'TBD')}
🕐 Time: {appointment_data.get('appointment_time', 'TBD')}
👨‍⚕️ Provider: Dr. {appointment_data.get('doctor_name', 'TBD')}
📍 Location: {self.clinic_name} - Main Office

**⚠️ IMPORTANT - PLEASE RESPOND:**

**✅ COMING TO YOUR APPOINTMENT?**
• Reply "CONFIRM" to confirm your attendance
• Arrive 15 minutes early for check-in
• Bring ID, insurance card, and medications list

**❌ NEED TO CANCEL?**
• Reply "CANCEL" and tell us why:
  - "CANCEL - SICK" 
  - "CANCEL - EMERGENCY"
  - "CANCEL - SCHEDULE CONFLICT"
  - "CANCEL - OTHER: [reason]"

**📅 NEED TO RESCHEDULE?**
• Reply "RESCHEDULE" and we'll help you find a new time
• Call us at {self.clinic_phone}

**⏰ LAST-MINUTE CHANGES:**
If you need to cancel within 2 hours of your appointment, please call us directly:
📞 {self.clinic_phone}

**CONTACT OPTIONS:**
📞 Call: {self.clinic_phone}
💬 Text: Reply to this message
🚨 Emergency: (555) 999-8888

**NO RESPONSE?**
If we don't hear from you, we'll assume you're coming and will hold your appointment slot.

We appreciate your timely response!

Best regards,
{self.clinic_name} Team
"""
        
        return {"subject": subject, "body": body}
    
    def sms_templates(self, appointment_data: Dict, reminder_type: str) -> str:
        """
        SMS templates for different reminder types
        
        Args:
            appointment_data: Dictionary containing appointment information
            reminder_type: Type of reminder (regular, form_check, confirmation)
            
        Returns:
            SMS message text
        """
        if reminder_type == "regular":
            return f"""
🏥 {self.clinic_name}

Appointment Reminder:
📅 {appointment_data.get('appointment_date', 'TBD')}
🕐 {appointment_data.get('appointment_time', 'TBD')}
👨‍⚕️ Dr. {appointment_data.get('doctor_name', 'TBD')}

Arrive 15 min early. Bring ID & insurance.
Call {self.clinic_phone} to reschedule.

ID: {appointment_data.get('appointment_id', 'N/A')[-6:]}
Reply STOP to opt out.
"""
        
        elif reminder_type == "form_check":
            return f"""
🏥 {self.clinic_name}

Have you completed your intake forms?

📅 Appointment: {appointment_data.get('appointment_date', 'TBD')} at {appointment_data.get('appointment_time', 'TBD')}

Reply:
• COMPLETED - if forms are done
• HELP - need assistance
• PRINT - resend forms

Call: {self.clinic_phone}
Reply STOP to opt out.
"""
        
        elif reminder_type == "confirmation":
            return f"""
🏥 {self.clinic_name}

FINAL REMINDER
📅 TODAY: {appointment_data.get('appointment_date', 'TBD')}
🕐 {appointment_data.get('appointment_time', 'TBD')}

Reply:
• CONFIRM - I'm coming
• CANCEL - Can't make it
• RESCHEDULE - Need new time

Call: {self.clinic_phone}
Reply STOP to opt out.
"""
        
        return "Appointment reminder from " + self.clinic_name


class IntakeFormEmailTemplates:
    """Email templates for sending intake forms to patients"""
    
    def __init__(self, clinic_name: str = "Medical Clinic", clinic_phone: str = "(555) 123-4567"):
        self.clinic_name = clinic_name
        self.clinic_phone = clinic_phone
    
    def appointment_confirmation_with_intake_form(self, patient_data: Dict) -> Dict[str, str]:
        """
        Email template for appointment confirmation with intake form
        
        Args:
            patient_data: Dictionary containing patient and appointment information
            
        Returns:
            Dictionary with email subject and body
        """
        subject = f"Appointment Confirmed - Please Complete Intake Form | {self.clinic_name}"
        
        body = f"""
Dear {patient_data.get('first_name', 'Patient')},

Thank you for scheduling your appointment with {self.clinic_name}. We are pleased to confirm your upcoming visit.

APPOINTMENT DETAILS:
📅 Date: {patient_data.get('appointment_date', 'TBD')}
🕐 Time: {patient_data.get('appointment_time', 'TBD')}
👨‍⚕️ Provider: {patient_data.get('doctor_name', 'TBD')}
📍 Location: {patient_data.get('clinic_address', 'Main Office')}

IMPORTANT: COMPLETE YOUR INTAKE FORM
To ensure your appointment runs smoothly and on time, please complete your new patient intake form before your visit.

🔗 COMPLETE ONLINE INTAKE FORM: 
{patient_data.get('intake_form_link', 'Link will be provided separately')}

📋 ALTERNATIVE - DOWNLOAD PRINTABLE FORM:
If the online form link doesn't work, you can download and print the intake form from our local system.

ALTERNATIVE OPTIONS:
• Print and complete the attached form, bring it to your appointment
• Arrive 15 minutes early to complete the form at our office
• Call us at {self.clinic_phone} if you need assistance accessing the form

WHAT TO BRING:
✅ Photo ID (driver's license or state ID)
✅ Insurance card(s) 
✅ List of current medications
✅ Referral letter (if applicable)
✅ Previous medical records (if transferring care)
✅ Form of payment for copay/deductible

APPOINTMENT REMINDERS:
We will send you reminder notifications via your preferred contact method:
• 24 hours before your appointment
• 2 hours before your appointment

NEED TO RESCHEDULE?
If you need to reschedule or cancel your appointment, please contact us at least 24 hours in advance:
📞 Phone: {self.clinic_phone}
💻 Online: {patient_data.get('patient_portal_link', 'Available through patient portal')}

QUESTIONS?
If you have any questions about your appointment or the intake form, please don't hesitate to contact us at {self.clinic_phone}.

We look forward to providing you with excellent healthcare services!

Best regards,
{self.clinic_name} Team

---
This is an automated message. Please do not reply to this email.
For urgent medical matters, please call {self.clinic_phone} or visit the nearest emergency room.
"""
        
        return {
            "subject": subject,
            "body": body.strip()
        }
    
    def intake_form_reminder(self, patient_data: Dict) -> Dict[str, str]:
        """
        Email template for intake form completion reminder
        
        Args:
            patient_data: Dictionary containing patient information
            
        Returns:
            Dictionary with email subject and body
        """
        subject = f"Reminder: Complete Your Intake Form Before Your Appointment"
        
        body = f"""
Dear {patient_data.get('first_name', 'Patient')},

This is a friendly reminder that your appointment with {self.clinic_name} is approaching, and we have not yet received your completed intake form.

UPCOMING APPOINTMENT:
📅 Date: {patient_data.get('appointment_date', 'TBD')}
🕐 Time: {patient_data.get('appointment_time', 'TBD')}
👨‍⚕️ Provider: {patient_data.get('doctor_name', 'TBD')}

COMPLETE YOUR INTAKE FORM:
To ensure your appointment starts on time and we can provide you with the best possible care, please complete your intake form as soon as possible.

🔗 COMPLETE ONLINE: {patient_data.get('intake_form_link', 'Link provided in previous email')}

ALTERNATIVE OPTIONS:
• Download and print the form from our website
• Complete the form when you arrive (please arrive 15 minutes early)

WHY IT'S IMPORTANT:
✅ Saves time during your appointment
✅ Helps your provider prepare for your visit
✅ Ensures we have your complete medical history
✅ Facilitates insurance processing

NEED HELP?
If you're having trouble accessing or completing the form, please call us at {self.clinic_phone}. Our staff is happy to assist you.

Thank you for your cooperation!

Best regards,
{self.clinic_name} Team

---
This is an automated reminder. Please do not reply to this email.
"""
        
        return {
            "subject": subject,
            "body": body.strip()
        }
    
    def intake_form_received_confirmation(self, patient_data: Dict) -> Dict[str, str]:
        """
        Email template confirming intake form has been received
        
        Args:
            patient_data: Dictionary containing patient information
            
        Returns:
            Dictionary with email subject and body
        """
        subject = f"Intake Form Received - You're All Set!"
        
        body = f"""
Dear {patient_data.get('first_name', 'Patient')},

Thank you! We have successfully received your completed intake form.

APPOINTMENT DETAILS:
📅 Date: {patient_data.get('appointment_date', 'TBD')}
🕐 Time: {patient_data.get('appointment_time', 'TBD')}
👨‍⚕️ Provider: {patient_data.get('doctor_name', 'TBD')}

YOU'RE ALL SET!
✅ Intake form completed and received
✅ Insurance information reviewed
✅ Appointment confirmed

NEXT STEPS:
1. You will receive appointment reminders via your preferred contact method
2. Please arrive 10-15 minutes before your scheduled time
3. Remember to bring your ID and insurance card

WHAT TO EXPECT:
Your provider has reviewed your intake information and is prepared for your visit. If we have any questions about your form, we will contact you before your appointment.

STILL NEED TO BRING:
📋 Photo ID
🏥 Insurance card(s)
💊 List of current medications (or bring the bottles)
💳 Payment method for copay/deductible

QUESTIONS?
If you have any questions before your appointment, please contact us at {self.clinic_phone}.

We look forward to seeing you soon!

Best regards,
{self.clinic_name} Team

---
This is an automated confirmation. Please do not reply to this email.
"""
        
        return {
            "subject": subject,
            "body": body.strip()
        }
    
    def intake_form_incomplete_notification(self, patient_data: Dict, missing_fields: list) -> Dict[str, str]:
        """
        Email template for incomplete intake form notification
        
        Args:
            patient_data: Dictionary containing patient information
            missing_fields: List of missing required fields
            
        Returns:
            Dictionary with email subject and body
        """
        subject = f"Action Required: Complete Your Intake Form"
        
        missing_items = "\n".join([f"• {field}" for field in missing_fields])
        
        body = f"""
Dear {patient_data.get('first_name', 'Patient')},

We received your intake form submission, but it appears some required information is missing. To ensure we can provide you with the best care during your appointment, please complete the following:

MISSING INFORMATION:
{missing_items}

UPCOMING APPOINTMENT:
📅 Date: {patient_data.get('appointment_date', 'TBD')}
🕐 Time: {patient_data.get('appointment_time', 'TBD')}
👨‍⚕️ Provider: {patient_data.get('doctor_name', 'TBD')}

COMPLETE YOUR FORM:
🔗 Access your form: {patient_data.get('intake_form_link', 'Link provided in previous email')}

Your partially completed information has been saved. Simply click the link above to finish where you left off.

NEED ASSISTANCE?
If you're having trouble completing the form or have questions about any of the required fields, please call us at {self.clinic_phone}. Our staff is ready to help!

IMPORTANT:
Please complete the missing information at least 24 hours before your appointment to ensure we have adequate time to review your information.

Thank you for your prompt attention to this matter.

Best regards,
{self.clinic_name} Team

---
This is an automated notification. Please do not reply to this email.
"""
        
        return {
            "subject": subject,
            "body": body.strip()
        }
    
    def intake_form_followup_questions(self, patient_data: Dict, questions: list) -> Dict[str, str]:
        """
        Email template for follow-up questions about intake form
        
        Args:
            patient_data: Dictionary containing patient information
            questions: List of follow-up questions from medical staff
            
        Returns:
            Dictionary with email subject and body
        """
        subject = f"Follow-up Questions About Your Intake Form"
        
        question_list = "\n".join([f"{i+1}. {q}" for i, q in enumerate(questions)])
        
        body = f"""
Dear {patient_data.get('first_name', 'Patient')},

Thank you for submitting your intake form. Our medical team has reviewed your information and has a few follow-up questions to ensure we provide you with the best possible care.

FOLLOW-UP QUESTIONS:
{question_list}

UPCOMING APPOINTMENT:
📅 Date: {patient_data.get('appointment_date', 'TBD')}
🕐 Time: {patient_data.get('appointment_time', 'TBD')}
👨‍⚕️ Provider: {patient_data.get('doctor_name', 'TBD')}

HOW TO RESPOND:
Please reply to this email with your answers, or call us at {self.clinic_phone} to discuss these questions with our medical staff.

TIMING:
We would appreciate receiving your responses at least 24 hours before your appointment so our provider can adequately prepare for your visit.

Thank you for your cooperation in helping us provide you with excellent care!

Best regards,
{self.clinic_name} Medical Team

---
You may reply to this email or call {self.clinic_phone} for any questions.
"""
        
        return {
            "subject": subject,
            "body": body.strip()
        }


# Example usage
if __name__ == "__main__":
    templates = IntakeFormEmailTemplates("Springfield Medical Center", "(555) 123-4567")
    
    # Example patient data
    patient_data = {
        "first_name": "John",
        "last_name": "Doe",
        "appointment_date": "January 15, 2024",
        "appointment_time": "10:00 AM",
        "doctor_name": "Dr. Sarah Johnson",
        "clinic_address": "123 Medical Drive, Springfield, IL",
        "intake_form_link": "https://clinic.com/intake/form/abc123",
        "patient_portal_link": "https://clinic.com/portal"
    }
    
    # Generate confirmation email
    confirmation = templates.appointment_confirmation_with_intake_form(patient_data)
    print("APPOINTMENT CONFIRMATION EMAIL:")
    print(f"Subject: {confirmation['subject']}")
    print(f"Body:\n{confirmation['body']}")
    print("\n" + "="*80 + "\n")
    
    # Generate reminder email
    reminder = templates.intake_form_reminder(patient_data)
    print("INTAKE FORM REMINDER EMAIL:")
    print(f"Subject: {reminder['subject']}")
    print(f"Body:\n{reminder['body']}")
