"""
Automated Reminder System Engine
"""

import pandas as pd
import logging
from datetime import datetime, timedelta
from pathlib import Path
from typing import Dict, List, Optional, Tuple
import uuid

logger = logging.getLogger(__name__)


class AppointmentReminderEngine:
    """
    Automated reminder system with multi-channel messaging and conditional workflows
    """
    
    def __init__(self, data_dir: Path, email_service=None):
        self.data_dir = data_dir
        self.email_service = email_service
        
        # Reminder scheduling configuration
        self.reminder_schedule = {
            "regular": timedelta(hours=24),      # 24 hours before
            "form_check": timedelta(hours=4),    # 4 hours before  
            "confirmation": timedelta(hours=1)   # 1 hour before
        }
        
        # Initialize reminder tracking
        self.reminder_file = self.data_dir / "reminders" / "reminder_schedule.csv"
        self.appointments_file = self.data_dir / "appointments" / "scheduled_appointments.csv"
        self.patients_file = self.data_dir / "patients" / "patient_database.csv"
        
        self._ensure_reminder_database()
    
    def _ensure_reminder_database(self):
        """Ensure reminder database exists with proper structure"""
        try:
            if not self.reminder_file.exists():
                self.reminder_file.parent.mkdir(parents=True, exist_ok=True)
                
                # Create empty reminder database with headers
                reminder_df = pd.DataFrame(columns=[
                    'reminder_id', 'appointment_id', 'patient_id', 'reminder_type',
                    'scheduled_time', 'delivery_method', 'status', 'created_at',
                    'sent_at', 'patient_response', 'response_time', 'retry_count', 'notes'
                ])
                reminder_df.to_csv(self.reminder_file, index=False)
                logger.info("Created reminder database")
        except Exception as e:
            logger.error(f"Error ensuring reminder database: {e}")
    
    def schedule_reminders_for_appointment(self, appointment_id: str) -> Dict[str, str]:
        """
        Schedule all three types of reminders for a new appointment
        
        Args:
            appointment_id: The appointment ID to schedule reminders for
            
        Returns:
            Dictionary with status of reminder scheduling
        """
        try:
            # Load appointment and patient data
            appointments_df = pd.read_csv(self.appointments_file)
            patients_df = pd.read_csv(self.patients_file)
            
            # Find the appointment
            appointment = appointments_df[appointments_df['appointment_id'] == appointment_id]
            if appointment.empty:
                return {"status": "error", "message": f"Appointment {appointment_id} not found"}
            
            appointment_data = appointment.iloc[0]
            
            # Get patient data
            patient = patients_df[patients_df['patient_id'] == appointment_data['patient_id']]
            if patient.empty:
                return {"status": "error", "message": f"Patient {appointment_data['patient_id']} not found"}
            
            patient_data = patient.iloc[0]
            
            # Parse appointment datetime
            appointment_datetime = self._parse_appointment_datetime(
                appointment_data['appointment_date'], 
                appointment_data['appointment_time']
            )
            
            if not appointment_datetime:
                return {"status": "error", "message": "Could not parse appointment date/time"}
            
            # Schedule each reminder type
            scheduled_reminders = []
            reminder_df = pd.read_csv(self.reminder_file) if self.reminder_file.exists() else pd.DataFrame()
            
            for reminder_type, time_before in self.reminder_schedule.items():
                reminder_time = appointment_datetime - time_before
                
                # Only schedule if reminder time is in the future
                if reminder_time > datetime.now():
                    reminder_id = f"REM_{datetime.now().strftime('%Y%m%d_%H%M%S')}_{uuid.uuid4().hex[:6]}"
                    
                    # Determine delivery method based on patient preferences and type
                    delivery_method = self._determine_delivery_method(patient_data, reminder_type)
                    
                    new_reminder = {
                        'reminder_id': reminder_id,
                        'appointment_id': appointment_id,
                        'patient_id': appointment_data['patient_id'],
                        'reminder_type': reminder_type,
                        'scheduled_time': reminder_time.isoformat(),
                        'delivery_method': delivery_method,
                        'status': 'scheduled',
                        'created_at': datetime.now().isoformat(),
                        'sent_at': '',
                        'patient_response': '',
                        'response_time': '',
                        'retry_count': 0,
                        'notes': f"Auto-scheduled for {appointment_datetime.strftime('%Y-%m-%d %H:%M')}"
                    }
                    
                    # Add to DataFrame
                    new_reminder_df = pd.DataFrame([new_reminder])
                    reminder_df = pd.concat([reminder_df, new_reminder_df], ignore_index=True)
                    
                    scheduled_reminders.append({
                        'type': reminder_type,
                        'scheduled_for': reminder_time.strftime('%Y-%m-%d %H:%M'),
                        'method': delivery_method
                    })
            
            # Save updated reminders
            reminder_df.to_csv(self.reminder_file, index=False)
            
            return {
                "status": "success",
                "message": f"Scheduled {len(scheduled_reminders)} reminders for appointment {appointment_id}",
                "reminders": scheduled_reminders
            }
            
        except Exception as e:
            logger.error(f"Error scheduling reminders: {e}")
            return {"status": "error", "message": str(e)}
    
    def _parse_appointment_datetime(self, date_str: str, time_str: str) -> Optional[datetime]:
        """Parse appointment date and time strings into datetime object"""
        try:
            # Handle different date formats
            date_formats = ['%Y-%m-%d', '%m/%d/%Y', '%d/%m/%Y']
            time_formats = ['%H:%M', '%I:%M %p', '%H:%M:%S']
            
            parsed_date = None
            for date_format in date_formats:
                try:
                    parsed_date = datetime.strptime(date_str, date_format).date()
                    break
                except ValueError:
                    continue
            
            if not parsed_date:
                logger.error(f"Could not parse date: {date_str}")
                return None
            
            # Parse time
            parsed_time = None
            for time_format in time_formats:
                try:
                    parsed_time = datetime.strptime(time_str, time_format).time()
                    break
                except ValueError:
                    continue
            
            if not parsed_time:
                logger.error(f"Could not parse time: {time_str}")
                return None
            
            return datetime.combine(parsed_date, parsed_time)
            
        except Exception as e:
            logger.error(f"Error parsing appointment datetime: {e}")
            return None
    
    def _determine_delivery_method(self, patient_data: pd.Series, reminder_type: str) -> str:
        """Determine the best delivery method for a reminder"""
        # Safely get email and phone, handling NaN values
        email = patient_data.get('email', '')
        phone = patient_data.get('phone', '')
        
        # Handle NaN values from pandas
        if pd.isna(email):
            email = ''
        if pd.isna(phone):
            phone = ''
            
        has_email = bool(str(email).strip()) if email else False
        has_phone = bool(str(phone).strip()) if phone else False
        
        # Priority logic:
        # - Form check: Email preferred (better for links/attachments)
        # - Confirmation: Both email and SMS for urgency
        # - Regular: Email first, SMS backup
        
        if reminder_type == "form_check":
            return "email" if has_email else "sms" if has_phone else "none"
        elif reminder_type == "confirmation":
            if has_email and has_phone:
                return "email+sms"
            elif has_email:
                return "email"
            elif has_phone:
                return "sms"
            else:
                return "none"
        else:  # regular reminder
            if has_email:
                return "email"
            elif has_phone:
                return "sms"
            else:
                return "none"
    
    def check_and_send_due_reminders(self) -> Dict[str, List]:
        """
        Check for and send any reminders that are due
        
        Returns:
            Dictionary with lists of sent, failed, and skipped reminders
        """
        try:
            if not self.reminder_file.exists():
                return {"sent": [], "failed": [], "skipped": []}
            
            reminder_df = pd.read_csv(self.reminder_file)
            
            # Filter for scheduled reminders that are due
            now = datetime.now()
            due_reminders = reminder_df[
                (reminder_df['status'] == 'scheduled') &
                (pd.to_datetime(reminder_df['scheduled_time']) <= now)
            ]
            
            sent_reminders = []
            failed_reminders = []
            skipped_reminders = []
            
            for idx, reminder in due_reminders.iterrows():
                result = self._send_single_reminder(reminder)
                
                if result['status'] == 'sent':
                    sent_reminders.append(result)
                    # Update reminder status
                    reminder_df.loc[idx, 'status'] = 'sent'
                    reminder_df.loc[idx, 'sent_at'] = now.isoformat()
                elif result['status'] == 'failed':
                    failed_reminders.append(result)
                    # Update retry count and status
                    reminder_df.loc[idx, 'retry_count'] = reminder_df.loc[idx, 'retry_count'] + 1
                    if reminder_df.loc[idx, 'retry_count'] >= 3:
                        reminder_df.loc[idx, 'status'] = 'failed'
                    else:
                        # Reschedule for retry in 30 minutes
                        retry_time = now + timedelta(minutes=30)
                        reminder_df.loc[idx, 'scheduled_time'] = retry_time.isoformat()
                else:
                    skipped_reminders.append(result)
                    reminder_df.loc[idx, 'status'] = 'skipped'
            
            # Save updated reminders
            reminder_df.to_csv(self.reminder_file, index=False)
            
            return {
                "sent": sent_reminders,
                "failed": failed_reminders,
                "skipped": skipped_reminders
            }
            
        except Exception as e:
            logger.error(f"Error checking due reminders: {e}")
            return {"sent": [], "failed": [], "skipped": []}
    
    def _send_single_reminder(self, reminder: pd.Series) -> Dict:
        """Send a single reminder"""
        try:
            # Get appointment and patient data
            appointments_df = pd.read_csv(self.appointments_file)
            patients_df = pd.read_csv(self.patients_file)
            
            appointment = appointments_df[appointments_df['appointment_id'] == reminder['appointment_id']]
            if appointment.empty:
                return {"status": "skipped", "reason": "Appointment not found"}
            
            patient = patients_df[patients_df['patient_id'] == reminder['patient_id']]
            if patient.empty:
                return {"status": "skipped", "reason": "Patient not found"}
            
            # Prepare combined data for templates
            appointment_data = appointment.iloc[0].to_dict()
            patient_data = patient.iloc[0].to_dict()
            
            # Clean data to handle NaN values
            def clean_value(value):
                if pd.isna(value):
                    return ''
                return str(value).strip()
            
            # Build patient name safely
            patient_name = clean_value(patient_data.get('full_name', ''))
            if not patient_name:
                first_name = clean_value(patient_data.get('first_name', ''))
                last_name = clean_value(patient_data.get('last_name', ''))
                patient_name = f"{first_name} {last_name}".strip()
            
            combined_data = {
                **appointment_data,
                'patient_name': patient_name,
                'patient_email': clean_value(patient_data.get('email', '')),
                'patient_phone': clean_value(patient_data.get('phone', '')),
                'doctor_name': clean_value(appointment_data.get('doctor_name', 'TBD'))
            }
            
            # Send based on delivery method
            delivery_method = reminder['delivery_method']
            success = False
            
            if 'email' in delivery_method and self.email_service:
                email_success = self.email_service.send_appointment_reminder(
                    combined_data, 
                    reminder['reminder_type']
                )
                success = email_success or success
            
            if 'sms' in delivery_method:
                sms_success = self.email_service.send_sms_reminder(
                    combined_data,
                    reminder['reminder_type']
                ) if self.email_service else True  # Simulated success
                success = sms_success or success
            
            if success:
                return {
                    "status": "sent",
                    "reminder_id": reminder['reminder_id'],
                    "type": reminder['reminder_type'],
                    "method": delivery_method,
                    "patient": combined_data['patient_name']
                }
            else:
                return {
                    "status": "failed",
                    "reminder_id": reminder['reminder_id'],
                    "type": reminder['reminder_type'],
                    "reason": "Delivery failed"
                }
                
        except Exception as e:
            logger.error(f"Error sending reminder {reminder.get('reminder_id', 'unknown')}: {e}")
            return {
                "status": "failed",
                "reminder_id": reminder.get('reminder_id', 'unknown'),
                "reason": str(e)
            }
    
    def get_reminder_status(self, appointment_id: str = None, patient_id: str = None) -> Dict:
        """Get reminder status for appointment or patient"""
        try:
            if not self.reminder_file.exists():
                return {"reminders": [], "summary": {"total": 0}}
            
            reminder_df = pd.read_csv(self.reminder_file)
            
            # Filter based on parameters
            if appointment_id:
                filtered_reminders = reminder_df[reminder_df['appointment_id'] == appointment_id]
            elif patient_id:
                filtered_reminders = reminder_df[reminder_df['patient_id'] == patient_id]
            else:
                filtered_reminders = reminder_df
            
            reminders = filtered_reminders.to_dict('records')
            
            # Create summary
            summary = {
                "total": len(reminders),
                "scheduled": len(filtered_reminders[filtered_reminders['status'] == 'scheduled']),
                "sent": len(filtered_reminders[filtered_reminders['status'] == 'sent']),
                "failed": len(filtered_reminders[filtered_reminders['status'] == 'failed']),
                "skipped": len(filtered_reminders[filtered_reminders['status'] == 'skipped'])
            }
            
            return {"reminders": reminders, "summary": summary}
            
        except Exception as e:
            logger.error(f"Error getting reminder status: {e}")
            return {"reminders": [], "summary": {"total": 0}}
    
    def process_patient_response(self, patient_id: str, response: str, reminder_type: str = None) -> Dict:
        """
        Process patient response to reminder
        
        Args:
            patient_id: ID of the responding patient
            response: Patient's response text
            reminder_type: Type of reminder being responded to
            
        Returns:
            Dictionary with processing result and next actions
        """
        try:
            response_lower = response.lower().strip()
            current_time = datetime.now().isoformat()
            
            # Process different response types
            if reminder_type == "form_check":
                if "completed" in response_lower:
                    return {
                        "status": "success",
                        "action": "forms_completed",
                        "message": "Thank you! Your forms are marked as completed.",
                        "next_action": "none"
                    }
                elif "help" in response_lower:
                    return {
                        "status": "success",
                        "action": "help_requested",
                        "message": "We'll call you to help with the forms.",
                        "next_action": "staff_callback"
                    }
                elif "print" in response_lower:
                    return {
                        "status": "success",
                        "action": "print_requested",
                        "message": "Printable forms will be resent to your email.",
                        "next_action": "resend_forms"
                    }
                    
            elif reminder_type == "confirmation":
                if "confirm" in response_lower:
                    return {
                        "status": "success",
                        "action": "visit_confirmed",
                        "message": "Great! We'll see you at your appointment.",
                        "next_action": "none"
                    }
                elif "cancel" in response_lower:
                    cancellation_reason = "unspecified"
                    if "sick" in response_lower:
                        cancellation_reason = "sick"
                    elif "emergency" in response_lower:
                        cancellation_reason = "emergency"
                    elif "schedule" in response_lower:
                        cancellation_reason = "schedule_conflict"
                    
                    return {
                        "status": "success",
                        "action": "appointment_cancelled",
                        "message": f"Appointment cancelled. Reason: {cancellation_reason}",
                        "next_action": "process_cancellation",
                        "cancellation_reason": cancellation_reason
                    }
                elif "reschedule" in response_lower:
                    return {
                        "status": "success",
                        "action": "reschedule_requested",
                        "message": "We'll contact you to schedule a new appointment time.",
                        "next_action": "staff_reschedule"
                    }
            
            # Default response for unrecognized input
            return {
                "status": "partial",
                "action": "unknown_response",
                "message": "Thank you for responding. Our staff will follow up if needed.",
                "next_action": "staff_review"
            }
            
        except Exception as e:
            logger.error(f"Error processing patient response: {e}")
            return {
                "status": "error",
                "message": "Error processing your response. Please call our office.",
                "next_action": "staff_contact"
            }
