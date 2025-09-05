"""
PDF-Style Intake Form Generator
Creates printable intake forms and handles PDF generation
"""

from datetime import datetime
from typing import Dict, Optional
import json


class PDFIntakeFormGenerator:
    """Generate PDF-style intake forms that can be printed or filled digitally"""
    
    def __init__(self):
        self.form_template = self.load_form_template()
    
    def load_form_template(self) -> Dict:
        """Load the intake form template"""
        # This would normally load from the JSON file
        # For now, we'll use a basic template structure
        return {
            "clinic_name": "Medical Clinic",
            "form_title": "NEW PATIENT INTAKE FORM",
            "instructions": "Please complete this form in its entirety and bring it to your appointment."
        }
    
    def generate_printable_form(self, output_path: str = None) -> str:
        """Generate a printable intake form in text format"""
        if output_path is None:
            output_path = f"forms/printable_intake_form_{datetime.now().strftime('%Y%m%d')}.txt"
        
        form_content = self._create_printable_content()
        
        with open(output_path, 'w') as f:
            f.write(form_content)
        
        return output_path
    
    def _create_printable_content(self) -> str:
        """Create the printable form content"""
        content = f"""
{'='*80}
                            MEDICAL CLINIC
                        NEW PATIENT INTAKE FORM
{'='*80}

Date: ____________    Patient ID: ____________    

INSTRUCTIONS: Please complete this form in its entirety. All fields marked with 
an asterisk (*) are required. Please print clearly.

{'='*80}
                          PERSONAL INFORMATION
{'='*80}

First Name: *_________________________  Middle Name: _____________________

Last Name: *__________________________  

Date of Birth: *_____/_____/_____      Gender: *___________________
               MM   DD   YYYY

Marital Status: ________________       Social Security #: *____-___-_____

{'='*80}
                          CONTACT INFORMATION  
{'='*80}

Address: *____________________________________________________________

City: *_________________________  State: *________  ZIP: *____________

Primary Phone: *(____)____-______    Secondary Phone: (____)____-______

Email Address: *______________________________________________________

Preferred Contact Method: *□ Phone  □ Email  □ Text Message

{'='*80}
                          EMERGENCY CONTACT
{'='*80}

Emergency Contact Name: *__________________________________________

Relationship to Patient: *______________________________________

Emergency Phone Number: *(____)____-______

Emergency Email: ________________________________________________

{'='*80}
                         INSURANCE INFORMATION
{'='*80}

Insurance Carrier: *____________________________________________

Policy Number: *_______________________________________________

Group Number: ________________________________________________

Policy Holder Name: __________________________________________

Relationship to Patient: □ Self  □ Spouse  □ Parent  □ Child  □ Other

{'='*80}
                           MEDICAL HISTORY
{'='*80}

Primary Care Physician: ________________________________________

Reason for Today's Visit: *____________________________________
____________________________________________________________
____________________________________________________________

Current Medications (include dosage): _________________________
____________________________________________________________
____________________________________________________________
____________________________________________________________

Known Allergies: *_____________________________________________
____________________________________________________________

Past Medical History (surgeries, hospitalizations, chronic conditions):
____________________________________________________________
____________________________________________________________
____________________________________________________________

Family Medical History: _______________________________________
____________________________________________________________
____________________________________________________________

{'='*80}
                         LIFESTYLE INFORMATION
{'='*80}

Smoking Status: *□ Never smoked  □ Former smoker  □ Current smoker

Alcohol Use: □ None  □ Occasional  □ Moderate  □ Heavy

Exercise Habits: ______________________________________________
____________________________________________________________

{'='*80}
                        CONSENT AND AUTHORIZATION
{'='*80}

□ *I consent to treatment by the medical staff

□ *I acknowledge receipt of HIPAA privacy practices

□ *I assign insurance benefits to be paid directly to the provider

□  I consent to receive appointment reminders via my preferred contact method

Patient Signature: *____________________________________________

Print Name: *__________________________________________________

Date: *_____/_____/_____
       MM   DD   YYYY

{'='*80}
                            FOR OFFICE USE ONLY
{'='*80}

Form Received: _____/_____/_____    Staff Initials: ___________

Insurance Verified: □ Yes  □ No    Verification Date: ___________

Copay Collected: $ __________      Payment Method: ____________

Notes: ________________________________________________________
____________________________________________________________

{'='*80}

Thank you for choosing our medical practice. We look forward to 
providing you with excellent healthcare services.

For questions about this form, please call: (555) 123-4567
"""
        return content.strip()
    
    def generate_form_checklist(self) -> str:
        """Generate a checklist for intake form completion"""
        checklist = """
INTAKE FORM COMPLETION CHECKLIST

Before your appointment, please ensure you have completed the following:

□ Personal Information Section
  □ Full name (first, middle, last)
  □ Date of birth
  □ Gender
  □ Social Security Number

□ Contact Information Section  
  □ Complete address
  □ Primary phone number
  □ Email address
  □ Preferred contact method

□ Emergency Contact Section
  □ Emergency contact name
  □ Relationship to patient
  □ Emergency contact phone number

□ Insurance Information Section
  □ Insurance carrier name
  □ Policy number
  □ Group number (if applicable)

□ Medical History Section
  □ Reason for visit
  □ Known allergies (or "None")
  □ Current medications (or "None")

□ Lifestyle Information Section
  □ Smoking status

□ Consent and Authorization Section
  □ Treatment consent (required)
  □ HIPAA acknowledgment (required)
  □ Insurance assignment (required)
  □ Patient signature and date

□ Documents to Bring
  □ Photo ID (driver's license or state ID)
  □ Insurance card(s)
  □ List of current medications
  □ Referral letter (if applicable)
  □ Previous medical records (if applicable)

IMPORTANT REMINDERS:
- Arrive 15 minutes early for your appointment
- Bring a form of payment for any copay or deductible
- If you wear glasses or contacts, bring them to your appointment
- Inform us of any changes to your insurance before your visit

Questions? Call us at (555) 123-4567
"""
        return checklist.strip()


# Example usage
if __name__ == "__main__":
    generator = PDFIntakeFormGenerator()
    
    # Generate printable form
    form_path = generator.generate_printable_form()
    print(f"Printable intake form generated: {form_path}")
    
    # Generate checklist
    checklist = generator.generate_form_checklist()
    print("\nIntake Form Checklist:")
    print(checklist)
