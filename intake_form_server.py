"""
Local Development Server for Intake Forms
Serves intake forms locally instead of requiring external domain
"""

import streamlit as st
import sys
import os
from pathlib import Path

# Add src to path for imports
sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))

def serve_intake_form():
    """Serve the patient intake form locally"""
    
    st.set_page_config(
        page_title="Patient Intake Form - Valley Medical Center",
        page_icon="🏥",
        layout="wide"
    )
    
    # Get form ID from URL params
    form_id = st.query_params.get("form_id", "UNKNOWN")
    
    st.title("🏥 Valley Medical Center")
    st.header("Patient Intake Form")
    st.markdown("---")
    
    if form_id != "UNKNOWN":
        st.success(f"✅ Form ID: {form_id}")
        st.info("📧 This form was sent to you via email confirmation")
    
    # Main intake form
    with st.form("patient_intake_form"):
        st.subheader("📋 Personal Information")
        
        col1, col2 = st.columns(2)
        with col1:
            first_name = st.text_input("First Name *", placeholder="John")
            last_name = st.text_input("Last Name *", placeholder="Doe")
            email = st.text_input("Email Address *", placeholder="john.doe@email.com")
            phone = st.text_input("Phone Number *", placeholder="(555) 123-4567")
        
        with col2:
            date_of_birth = st.date_input("Date of Birth *")
            gender = st.selectbox("Gender", ["Select...", "Male", "Female", "Other", "Prefer not to say"])
            address = st.text_area("Address *", placeholder="123 Main St, City, State 12345")
        
        st.subheader("🏥 Insurance Information")
        
        col3, col4 = st.columns(2)
        with col3:
            insurance_provider = st.selectbox(
                "Insurance Provider *",
                ["Select...", "Blue Cross Blue Shield", "Aetna", "Cigna", "UnitedHealthcare", 
                 "Humana", "Kaiser Permanente", "Medicare", "Medicaid", "Other", "Self-Pay"]
            )
            policy_number = st.text_input("Policy Number", placeholder="ABC123456789")
        
        with col4:
            group_number = st.text_input("Group Number", placeholder="GRP001")
            subscriber_name = st.text_input("Subscriber Name", placeholder="If different from patient")
        
        st.subheader("🩺 Medical History")
        
        allergies = st.text_area("Allergies (medications, foods, environmental)", 
                                placeholder="Please list any known allergies or write 'None'")
        current_medications = st.text_area("Current Medications", 
                                         placeholder="List all medications, vitamins, and supplements")
        medical_conditions = st.text_area("Current Medical Conditions", 
                                        placeholder="List any ongoing medical conditions")
        previous_surgeries = st.text_area("Previous Surgeries", 
                                        placeholder="List any previous surgeries with dates")
        
        st.subheader("👨‍👩‍👧‍👦 Emergency Contact")
        
        col5, col6 = st.columns(2)
        with col5:
            emergency_name = st.text_input("Emergency Contact Name *", placeholder="Jane Doe")
            emergency_phone = st.text_input("Emergency Contact Phone *", placeholder="(555) 987-6543")
        
        with col6:
            emergency_relationship = st.text_input("Relationship *", placeholder="Spouse, Parent, Sibling, etc.")
        
        st.subheader("📝 Additional Information")
        
        reason_for_visit = st.text_area("Reason for Today's Visit", 
                                      placeholder="Briefly describe the reason for your appointment")
        
        # Consent and agreements
        st.subheader("✅ Consent and Agreements")
        
        consent_treatment = st.checkbox("I consent to medical treatment and procedures")
        consent_privacy = st.checkbox("I acknowledge receipt of the Notice of Privacy Practices")
        consent_financial = st.checkbox("I understand my financial responsibility for services")
        
        # Submit button
        submitted = st.form_submit_button("📤 Submit Intake Form", type="primary")
        
        if submitted:
            # Validate required fields
            required_fields = [first_name, last_name, email, phone, address]
            if not all(required_fields) or gender == "Select..." or insurance_provider == "Select...":
                st.error("❌ Please fill in all required fields marked with *")
            elif not all([consent_treatment, consent_privacy, consent_financial]):
                st.error("❌ Please check all consent boxes to proceed")
            else:
                # Simulate form submission
                st.success("✅ Thank you! Your intake form has been submitted successfully.")
                st.balloons()
                
                st.info("""
                📧 **What happens next:**
                1. Your information has been securely saved
                2. Our medical team will review your intake form
                3. You'll receive an appointment confirmation email
                4. Please arrive 10 minutes early for your appointment
                
                📞 **Questions?** Call us at +1-555-MEDICAL
                """)
    
    # Footer
    st.markdown("---")
    st.markdown("""
    <div style='text-align: center; color: gray;'>
    🏥 Valley Medical Center | 123 Health St, Medical City, MC 12345<br>
    📞 +1-555-MEDICAL | 📧 info@valleymedical.local<br>
    <small>This form is served locally for development purposes</small>
    </div>
    """, unsafe_allow_html=True)

if __name__ == "__main__":
    serve_intake_form()
