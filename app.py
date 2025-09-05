"""
Streamlit Web Interface for Medical Appointment Scheduling AI Agent
"""

import streamlit as st
import sys
import os
import pandas as pd
from datetime import datetime, timedelta

# Add src to path for imports
sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))

from agents.scheduling_agent import MedicalSchedulingAgent

def main():
    st.set_page_config(
        page_title="Medical Appointment Scheduling AI",
        page_icon="🏥",
        layout="wide"
    )
    
    st.title("🏥 Medical Appointment Scheduling AI Agent")
    st.markdown("---")
    
    # Initialize the agent
    if 'agent' not in st.session_state:
        st.session_state.agent = MedicalSchedulingAgent()
        st.session_state.chat_history = []
    
    # Sidebar with system info
    with st.sidebar:
        st.header("📊 System Status")
        st.success("✅ AI Agent: Online")
        st.success("✅ Database: Connected")
        st.success("✅ Schedule Data: Loaded")
        
        st.header("� Database Info")
        try:
            # Load patient data
            patients_df = pd.read_csv('data/patients/patient_database.csv')
            doctors_df = pd.read_csv('data/doctors/doctor_profiles.csv')
            
            st.metric("Total Patients", len(patients_df))
            st.metric("Total Doctors", len(doctors_df))
            
            # Show sample patients
            if st.checkbox("Show Patient Database"):
                st.subheader("👥 Existing Patients")
                st.write("**Use these exact names to test existing patient lookup:**")
                for i, patient in patients_df.head(10).iterrows():
                    st.write(f"• **{patient['first_name']} {patient['last_name']}**")
                    st.write(f"  📞 {patient['phone']}")
                    st.write(f"  📧 {patient['email']}")
                    st.write("---")
            
            # Show sample doctors
            if st.checkbox("Show Doctor Database"):
                st.subheader("👨‍⚕️ Available Doctors")
                for i, doctor in doctors_df.iterrows():
                    st.write(f"• **Dr. {doctor['first_name']} {doctor['last_name']}**")
                    st.write(f"  🩺 {doctor['specialty']}")
                    st.write(f"  📞 {doctor['phone']}")
                    st.write("---")
                    
        except Exception as e:
            st.error(f"Error loading database: {e}")
        
        st.header("�🔧 Quick Actions")
        if st.button("Show Available Doctors"):
            response = st.session_state.agent._get_doctor_info("all")
            st.text_area("Doctors:", response, height=200)
        
        if st.button("Show Next Week Availability"):
            response = st.session_state.agent._search_available_slots("next week")
            st.text_area("Available Slots:", response, height=300)
    
    # Main chat interface
    st.header("💬 Chat with AI Scheduling Assistant")
    
    # Display chat history
    chat_container = st.container()
    with chat_container:
        for i, (user_msg, agent_response) in enumerate(st.session_state.chat_history):
            with st.chat_message("user"):
                st.write(user_msg)
            with st.chat_message("assistant"):
                st.write(agent_response)
    
    # Chat input
    if prompt := st.chat_input("Type your message here..."):
        # Add user message to history
        st.session_state.chat_history.append((prompt, ""))
        
        # Get agent response
        with st.spinner("AI is thinking..."):
            try:
                response = st.session_state.agent.chat(prompt)
                # Update the last entry with the response
                st.session_state.chat_history[-1] = (prompt, response)
            except Exception as e:
                error_msg = f"Sorry, I encountered an error: {str(e)}"
                st.session_state.chat_history[-1] = (prompt, error_msg)
        
        # Rerun to update the display
        st.rerun()
    
    # Sample queries section
    st.header("💡 Try These Sample Queries")
    col1, col2, col3 = st.columns(3)
    
    with col1:
        if st.button("Find Available Appointments"):
            sample_query = "What appointments are available next week?"
            if sample_query not in [msg[0] for msg in st.session_state.chat_history]:
                response = st.session_state.agent.chat(sample_query)
                st.session_state.chat_history.append((sample_query, response))
                st.rerun()
    
    with col2:
        if st.button("Get Doctor Information"):
            sample_query = "What doctors do you have available?"
            if sample_query not in [msg[0] for msg in st.session_state.chat_history]:
                response = st.session_state.agent.chat(sample_query)
                st.session_state.chat_history.append((sample_query, response))
                st.rerun()
    
    with col3:
        if st.button("Check Insurance"):
            sample_query = "Do you accept Blue Cross Blue Shield insurance?"
            if sample_query not in [msg[0] for msg in st.session_state.chat_history]:
                response = st.session_state.agent.chat(sample_query)
                st.session_state.chat_history.append((sample_query, response))
                st.rerun()
    
    # Footer
    st.markdown("---")
    st.markdown(
        """
        <div style='text-align: center; color: gray;'>
        🤖 Powered by LangChain & LangGraph | Built with Streamlit
        </div>
        """, 
        unsafe_allow_html=True
    )

if __name__ == "__main__":
    main()
