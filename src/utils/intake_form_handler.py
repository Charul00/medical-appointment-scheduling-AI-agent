"""
Patient Intake Form Handler
Manages intake form data collection, validation, and integration with the scheduling system.
"""

import json
import pandas as pd
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional, Tuple
from dataclasses import dataclass, asdict
import re


@dataclass
class PersonalInfo:
    """Personal information section of intake form"""
    first_name: str
    middle_name: Optional[str]
    last_name: str
    date_of_birth: str
    gender: str
    marital_status: Optional[str]
    social_security: str


@dataclass
class ContactInfo:
    """Contact information section of intake form"""
    address: str
    city: str
    state: str
    zip_code: str
    primary_phone: str
    secondary_phone: Optional[str]
    email: str
    preferred_contact: str


@dataclass
class EmergencyContact:
    """Emergency contact information"""
    name: str
    relationship: str
    phone: str
    email: Optional[str]


@dataclass
class InsuranceInfo:
    """Insurance information section"""
    carrier: str
    policy_number: str
    group_number: Optional[str]
    policy_holder: Optional[str]
    relationship_to_patient: Optional[str]


@dataclass
class MedicalHistory:
    """Medical history information"""
    primary_care_physician: Optional[str]
    reason_for_visit: str
    current_medications: Optional[str]
    allergies: str
    medical_history: Optional[str]
    family_history: Optional[str]


@dataclass
class LifestyleInfo:
    """Lifestyle and habits information"""
    smoking_status: str
    alcohol_use: Optional[str]
    exercise_habits: Optional[str]


@dataclass
class ConsentInfo:
    """Consent and authorization information"""
    treatment_consent: bool
    hipaa_consent: bool
    insurance_assignment: bool
    appointment_reminders: bool
    patient_signature: str
    signature_date: str


@dataclass
class PatientIntakeForm:
    """Complete patient intake form data structure"""
    personal_info: PersonalInfo
    contact_info: ContactInfo
    emergency_contact: EmergencyContact
    insurance_info: InsuranceInfo
    medical_history: MedicalHistory
    lifestyle_info: LifestyleInfo
    consent_info: ConsentInfo
    form_id: str
    submission_date: str
    appointment_id: Optional[str] = None


class IntakeFormHandler:
    """Handles patient intake form processing and validation"""
    
    def __init__(self, data_dir: str = "data/intake_forms"):
        self.data_dir = Path(data_dir)
        self.data_dir.mkdir(parents=True, exist_ok=True)
        self.forms_file = self.data_dir / "submitted_forms.json"
        self.validation_errors = []
    
    def validate_form_data(self, form_data: Dict) -> Tuple[bool, List[str]]:
        """
        Validate intake form data
        
        Args:
            form_data: Dictionary containing form field data
            
        Returns:
            Tuple of (is_valid, list_of_errors)
        """
        errors = []
        
        # Required field validation
        required_fields = [
            'firstName', 'lastName', 'dateOfBirth', 'gender', 'socialSecurity',
            'address', 'city', 'state', 'zipCode', 'primaryPhone', 'email',
            'preferredContact', 'emergencyName', 'emergencyRelationship',
            'emergencyPhone', 'insuranceCarrier', 'policyNumber', 
            'reasonForVisit', 'allergies', 'smokingStatus', 'patientSignature',
            'signatureDate'
        ]
        
        for field in required_fields:
            if not form_data.get(field) or str(form_data.get(field)).strip() == '':
                errors.append(f"Required field '{field}' is missing or empty")
        
        # Email validation
        email = form_data.get('email', '')
        if email and not re.match(r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$', email):
            errors.append("Invalid email format")
        
        # Phone number validation (basic)
        phone_fields = ['primaryPhone', 'emergencyPhone']
        for field in phone_fields:
            phone = form_data.get(field, '')
            if phone:
                # Remove formatting and check if it's 10 digits
                clean_phone = re.sub(r'[\s\-\(\)\.]+', '', phone)
                if not re.match(r'^\d{10}$', clean_phone):
                    errors.append(f"Invalid phone number format for {field}")
        
        # Date validation
        try:
            dob = form_data.get('dateOfBirth')
            if dob:
                datetime.strptime(dob, '%Y-%m-%d')
        except ValueError:
            errors.append("Invalid date of birth format")
        
        # SSN validation (basic format check)
        ssn = form_data.get('socialSecurity', '')
        if ssn and not re.match(r'^\d{3}-\d{2}-\d{4}$', ssn):
            errors.append("Invalid Social Security Number format (should be XXX-XX-XXXX)")
        
        # Consent validation
        required_consents = ['treatmentConsent', 'hipaaConsent', 'insuranceAssignment']
        for consent in required_consents:
            if not form_data.get(consent):
                errors.append(f"Required consent '{consent}' not provided")
        
        return len(errors) == 0, errors
    
    def process_form_submission(self, form_data: Dict, appointment_id: Optional[str] = None) -> Tuple[bool, str, Optional[PatientIntakeForm]]:
        """
        Process a submitted intake form
        
        Args:
            form_data: Dictionary containing form field data
            appointment_id: Optional appointment ID to link the form
            
        Returns:
            Tuple of (success, message, intake_form_object)
        """
        try:
            # Validate the form data
            is_valid, errors = self.validate_form_data(form_data)
            if not is_valid:
                return False, f"Validation errors: {'; '.join(errors)}", None
            
            # Generate form ID
            form_id = f"INTAKE_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
            submission_date = datetime.now().isoformat()
            
            # Create structured intake form object
            intake_form = PatientIntakeForm(
                personal_info=PersonalInfo(
                    first_name=form_data['firstName'],
                    middle_name=form_data.get('middleName'),
                    last_name=form_data['lastName'],
                    date_of_birth=form_data['dateOfBirth'],
                    gender=form_data['gender'],
                    marital_status=form_data.get('maritalStatus'),
                    social_security=form_data['socialSecurity']
                ),
                contact_info=ContactInfo(
                    address=form_data['address'],
                    city=form_data['city'],
                    state=form_data['state'],
                    zip_code=form_data['zipCode'],
                    primary_phone=form_data['primaryPhone'],
                    secondary_phone=form_data.get('secondaryPhone'),
                    email=form_data['email'],
                    preferred_contact=form_data['preferredContact']
                ),
                emergency_contact=EmergencyContact(
                    name=form_data['emergencyName'],
                    relationship=form_data['emergencyRelationship'],
                    phone=form_data['emergencyPhone'],
                    email=form_data.get('emergencyEmail')
                ),
                insurance_info=InsuranceInfo(
                    carrier=form_data['insuranceCarrier'],
                    policy_number=form_data['policyNumber'],
                    group_number=form_data.get('groupNumber'),
                    policy_holder=form_data.get('policyHolder'),
                    relationship_to_patient=form_data.get('relationshipToPatient')
                ),
                medical_history=MedicalHistory(
                    primary_care_physician=form_data.get('primaryCarePhysician'),
                    reason_for_visit=form_data['reasonForVisit'],
                    current_medications=form_data.get('currentMedications'),
                    allergies=form_data['allergies'],
                    medical_history=form_data.get('medicalHistory'),
                    family_history=form_data.get('familyHistory')
                ),
                lifestyle_info=LifestyleInfo(
                    smoking_status=form_data['smokingStatus'],
                    alcohol_use=form_data.get('alcoholUse'),
                    exercise_habits=form_data.get('exerciseHabits')
                ),
                consent_info=ConsentInfo(
                    treatment_consent=bool(form_data.get('treatmentConsent')),
                    hipaa_consent=bool(form_data.get('hipaaConsent')),
                    insurance_assignment=bool(form_data.get('insuranceAssignment')),
                    appointment_reminders=bool(form_data.get('appointmentReminders', False)),
                    patient_signature=form_data['patientSignature'],
                    signature_date=form_data['signatureDate']
                ),
                form_id=form_id,
                submission_date=submission_date,
                appointment_id=appointment_id
            )
            
            # Save the form
            self.save_intake_form(intake_form)
            
            return True, f"Intake form processed successfully. Form ID: {form_id}", intake_form
            
        except Exception as e:
            return False, f"Error processing intake form: {str(e)}", None
    
    def save_intake_form(self, intake_form: PatientIntakeForm) -> None:
        """Save intake form to storage"""
        # Load existing forms
        forms = self.load_all_forms()
        
        # Add new form
        forms[intake_form.form_id] = asdict(intake_form)
        
        # Save back to file
        with open(self.forms_file, 'w') as f:
            json.dump(forms, f, indent=2, default=str)
    
    def load_all_forms(self) -> Dict:
        """Load all submitted forms"""
        if self.forms_file.exists():
            with open(self.forms_file, 'r') as f:
                return json.load(f)
        return {}
    
    def get_form_by_id(self, form_id: str) -> Optional[Dict]:
        """Retrieve a specific form by ID"""
        forms = self.load_all_forms()
        return forms.get(form_id)
    
    def get_forms_by_appointment(self, appointment_id: str) -> List[Dict]:
        """Get all forms associated with an appointment"""
        forms = self.load_all_forms()
        return [form for form in forms.values() if form.get('appointment_id') == appointment_id]
    
    def export_forms_to_excel(self, output_file: str = None) -> str:
        """Export all forms to Excel file"""
        if output_file is None:
            output_file = self.data_dir / f"intake_forms_export_{datetime.now().strftime('%Y%m%d_%H%M%S')}.xlsx"
        
        forms = self.load_all_forms()
        if not forms:
            raise ValueError("No forms to export")
        
        # Flatten the data for Excel export
        flattened_data = []
        for form_id, form_data in forms.items():
            flat_record = {
                'form_id': form_id,
                'submission_date': form_data.get('submission_date'),
                'appointment_id': form_data.get('appointment_id'),
                
                # Personal Info
                'first_name': form_data['personal_info']['first_name'],
                'middle_name': form_data['personal_info'].get('middle_name'),
                'last_name': form_data['personal_info']['last_name'],
                'date_of_birth': form_data['personal_info']['date_of_birth'],
                'gender': form_data['personal_info']['gender'],
                'marital_status': form_data['personal_info'].get('marital_status'),
                'social_security': form_data['personal_info']['social_security'],
                
                # Contact Info
                'address': form_data['contact_info']['address'],
                'city': form_data['contact_info']['city'],
                'state': form_data['contact_info']['state'],
                'zip_code': form_data['contact_info']['zip_code'],
                'primary_phone': form_data['contact_info']['primary_phone'],
                'secondary_phone': form_data['contact_info'].get('secondary_phone'),
                'email': form_data['contact_info']['email'],
                'preferred_contact': form_data['contact_info']['preferred_contact'],
                
                # Emergency Contact
                'emergency_name': form_data['emergency_contact']['name'],
                'emergency_relationship': form_data['emergency_contact']['relationship'],
                'emergency_phone': form_data['emergency_contact']['phone'],
                'emergency_email': form_data['emergency_contact'].get('email'),
                
                # Insurance
                'insurance_carrier': form_data['insurance_info']['carrier'],
                'policy_number': form_data['insurance_info']['policy_number'],
                'group_number': form_data['insurance_info'].get('group_number'),
                'policy_holder': form_data['insurance_info'].get('policy_holder'),
                'relationship_to_patient': form_data['insurance_info'].get('relationship_to_patient'),
                
                # Medical History
                'primary_care_physician': form_data['medical_history'].get('primary_care_physician'),
                'reason_for_visit': form_data['medical_history']['reason_for_visit'],
                'current_medications': form_data['medical_history'].get('current_medications'),
                'allergies': form_data['medical_history']['allergies'],
                'medical_history': form_data['medical_history'].get('medical_history'),
                'family_history': form_data['medical_history'].get('family_history'),
                
                # Lifestyle
                'smoking_status': form_data['lifestyle_info']['smoking_status'],
                'alcohol_use': form_data['lifestyle_info'].get('alcohol_use'),
                'exercise_habits': form_data['lifestyle_info'].get('exercise_habits'),
                
                # Consent
                'treatment_consent': form_data['consent_info']['treatment_consent'],
                'hipaa_consent': form_data['consent_info']['hipaa_consent'],
                'insurance_assignment': form_data['consent_info']['insurance_assignment'],
                'appointment_reminders': form_data['consent_info']['appointment_reminders'],
                'patient_signature': form_data['consent_info']['patient_signature'],
                'signature_date': form_data['consent_info']['signature_date']
            }
            flattened_data.append(flat_record)
        
        # Create DataFrame and export
        df = pd.DataFrame(flattened_data)
        df.to_excel(output_file, index=False)
        
        return str(output_file)
    
    def generate_form_summary(self, form_id: str) -> Optional[str]:
        """Generate a summary of the intake form for review"""
        form_data = self.get_form_by_id(form_id)
        if not form_data:
            return None
        
        personal = form_data['personal_info']
        contact = form_data['contact_info']
        medical = form_data['medical_history']
        
        summary = f"""
PATIENT INTAKE FORM SUMMARY
Form ID: {form_id}
Submission Date: {form_data['submission_date']}

PATIENT INFORMATION:
Name: {personal['first_name']} {personal.get('middle_name', '')} {personal['last_name']}
DOB: {personal['date_of_birth']}
Gender: {personal['gender']}
Phone: {contact['primary_phone']}
Email: {contact['email']}

REASON FOR VISIT:
{medical['reason_for_visit']}

ALLERGIES:
{medical['allergies']}

INSURANCE:
Carrier: {form_data['insurance_info']['carrier']}
Policy: {form_data['insurance_info']['policy_number']}

EMERGENCY CONTACT:
{form_data['emergency_contact']['name']} ({form_data['emergency_contact']['relationship']})
Phone: {form_data['emergency_contact']['phone']}
"""
        return summary.strip()


# Example usage and testing
if __name__ == "__main__":
    # Create handler instance
    handler = IntakeFormHandler()
    
    # Example form data
    sample_form_data = {
        'firstName': 'John',
        'lastName': 'Doe',
        'dateOfBirth': '1990-01-15',
        'gender': 'male',
        'socialSecurity': '123-45-6789',
        'address': '123 Main St',
        'city': 'Anytown',
        'state': 'CA',
        'zipCode': '12345',
        'primaryPhone': '(555) 123-4567',
        'email': 'john.doe@email.com',
        'preferredContact': 'email',
        'emergencyName': 'Jane Doe',
        'emergencyRelationship': 'Spouse',
        'emergencyPhone': '(555) 987-6543',
        'insuranceCarrier': 'Blue Cross Blue Shield',
        'policyNumber': 'BCBS123456',
        'reasonForVisit': 'Annual checkup',
        'allergies': 'None',
        'smokingStatus': 'never',
        'treatmentConsent': True,
        'hipaaConsent': True,
        'insuranceAssignment': True,
        'patientSignature': 'John Doe',
        'signatureDate': '2024-01-15'
    }
    
    # Process the form
    success, message, intake_form = handler.process_form_submission(sample_form_data)
    print(f"Success: {success}")
    print(f"Message: {message}")
    
    if success and intake_form:
        print(f"\nGenerated Form Summary:")
        print(handler.generate_form_summary(intake_form.form_id))
