# Medical Appointment Scheduling AI Agent

An intelligent medical appointment scheduling system built with Python, LangChain, and Streamlit. Features smart scheduling, automated reminders, insurance validation, and comprehensive patient management.

![Python](https://img.shields.io/badge/python-v3.9+-blue.svg)
![LangChain](https://img.shields.io/badge/LangChain-🦜🔗-green.svg)
![Streamlit](https://img.shields.io/badge/Streamlit-FF4B4B.svg)
![License](https://img.shields.io/badge/license-MIT-green.svg)

## 🏥 Features

### Core Functionality
- **🧠 Smart Scheduling**: AI-powered duration optimization based on patient type and appointment reason
- **📋 Insurance Validation**: Real-time insurance verification and coverage checking
- **📧 Multi-channel Notifications**: Email and SMS appointment confirmations and reminders
- **📄 Automated Form Distribution**: Digital intake forms sent after appointment confirmation
- **🔔 3-Stage Reminder System**: Automated reminders at 24h, 4h, and 1h before appointments
- **📊 Excel Export**: Professional appointment reports with multiple sheets and formatting
- **💾 Data Backup**: Automated backup system with manifest tracking

### Advanced Features
- **🤖 Conversational AI**: Natural language appointment booking and management
- **📱 SMS Integration**: Support for Twilio and AWS SNS (simulated mode included)
- **💬 Patient Response Processing**: Automated handling of confirmations, cancellations, and requests
- **🔍 Smart Patient Lookup**: Intelligent patient search and deduplication
- **⏰ Flexible Scheduling**: Support for various appointment types and durations
- **🔒 Data Security**: Secure handling of sensitive medical information

## 🚀 Quick Start

### Prerequisites
- Python 3.9 or higher
- OpenAI API key
- Gmail account (for email notifications)

### Installation

1. **Clone the repository**
```bash
git clone https://github.com/Charul00/medical-appointment-scheduling-AI-agent.git
cd medical-appointment-scheduling-AI-agent
```

2. **Install dependencies**
```bash
pip install -r requirements.txt
```

3. **Set up environment variables**
Create a `.env` file in the root directory:
```env
# OpenAI Configuration
OPENAI_API_KEY=your_openai_api_key_here

# Email Configuration (Gmail)
EMAIL_ADDRESS=your_gmail@gmail.com
EMAIL_PASSWORD=your_app_password_here

# SMS Configuration (Optional - for real SMS)
# TWILIO_ACCOUNT_SID=your_twilio_sid
# TWILIO_AUTH_TOKEN=your_twilio_token
# TWILIO_PHONE_NUMBER=+1234567890
```

4. **Run the application**
```bash
streamlit run app.py
```

5. **Access the application**
Open your browser and go to `http://localhost:8501`

## 📱 SMS Integration

### Current Status: Simulated Mode
The system runs in simulated SMS mode by default, which:
- ✅ Shows exactly what SMS messages would be sent
- ✅ Perfect for testing and demonstrations
- ✅ No cost or setup required
- ✅ All SMS content is logged for review

### Real SMS Setup (Optional)

#### Option 1: Twilio (Recommended)
```bash
# Install Twilio
pip install twilio

# Set environment variables
export TWILIO_ACCOUNT_SID="your_account_sid_here"
export TWILIO_AUTH_TOKEN="your_auth_token_here"
export TWILIO_PHONE_NUMBER="+1234567890"
```

#### Option 2: AWS SNS
```bash
# Install boto3
pip install boto3

# Configure AWS credentials
aws configure
```

**Cost**: ~$0.0075 per SMS message

## 🏗️ System Architecture

```
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   Streamlit     │    │   LangChain     │    │   Data Layer    │
│   Frontend      │ ←→ │   AI Agent      │ ←→ │   CSV Files     │
└─────────────────┘    └─────────────────┘    └─────────────────┘
         │                       │                       │
         ▼                       ▼                       ▼
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   Email/SMS     │    │   Reminder      │    │   Backup        │
│   Services      │    │   Engine        │    │   System        │
└─────────────────┘    └─────────────────┘    └─────────────────┘
```

## 📊 Workflow

1. **Patient Interaction**: Natural language booking through Streamlit interface
2. **Smart Scheduling**: AI determines optimal appointment duration and type
3. **Insurance Validation**: Real-time verification of insurance coverage
4. **Confirmation**: Multi-channel notifications (email + SMS)
5. **Form Distribution**: Automated intake form delivery after confirmation
6. **Reminder System**: 3-stage automated reminders with patient response handling
7. **Data Management**: Excel export, backup, and comprehensive logging

## 🔧 Configuration

### Email Setup (Gmail)
1. Enable 2-factor authentication on your Gmail account
2. Generate an App Password for this application
3. Use the App Password (not your regular password) in the configuration

### Clinic Information
Edit `src/utils/smtp_email_service.py` to customize:
- Clinic name and contact information
- Email templates and branding
- Default appointment durations

## 📁 Project Structure

```
medical-appointment-scheduling-AI-agent/
├── app.py                          # Streamlit main application
├── src/
│   ├── agents/
│   │   └── scheduling_agent.py     # Main AI agent with all tools
│   └── utils/
│       ├── email_templates.py      # Email and SMS templates
│       ├── smtp_email_service.py   # Email service integration
│       ├── sms_service.py          # SMS service with multiple providers
│       └── reminder_engine.py      # Automated reminder system
├── data/
│   ├── patients/                   # Patient database
│   ├── doctors/                    # Doctor information
│   ├── appointments/               # Appointment records
│   └── reminders/                  # Reminder tracking
├── exports/                        # Excel exports and backups
├── requirements.txt                # Python dependencies
├── .env.example                    # Environment variables template
└── README.md                       # This file
```

## 🛠️ Tools Available

### Agent Tools
- `lookup_patient` - Find existing patients
- `add_patient` - Register new patients with insurance validation
- `get_doctor_info` - Search available doctors by specialty
- `search_available_slots` - Find open appointment times
- `book_appointment` - Complete appointment booking with smart scheduling
- `reschedule_appointment` - Modify existing appointments
- `cancel_appointment` - Cancel appointments with reason tracking
- `check_insurance_coverage` - Validate insurance information
- `send_appointment_confirmation` - Multi-channel confirmation delivery
- `distribute_intake_forms` - Automated form distribution
- `export_appointments_excel` - Generate professional reports
- `backup_data` - Create system backups
- `schedule_appointment_reminders` - Set up automated reminders
- `send_manual_reminder` - Override automatic reminder timing
- `process_patient_response` - Handle patient replies and actions
- `run_reminder_system` - Process all due reminders
- `configure_sms_service` - SMS setup and configuration

## 🧪 Testing

Run the test suite to verify all functionality:

```bash
# Test core scheduling functionality
python3 -c "
import sys; sys.path.append('src')
from agents.scheduling_agent import MedicalSchedulingAgent
agent = MedicalSchedulingAgent()
print('System initialized successfully!')
"

# Test booking workflow
python3 -c "
import sys; sys.path.append('src')
from agents.scheduling_agent import MedicalSchedulingAgent
agent = MedicalSchedulingAgent()
result = agent._book_appointment('I am John Doe, email john@email.com, need checkup')
print('Booking test completed')
"
```

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🆘 Support

- **Documentation**: Check the code comments and docstrings
- **Issues**: Open a GitHub issue for bugs or feature requests
- **SMS Setup**: Use the built-in `configure_sms_service` tool for setup instructions

## 🎯 Roadmap

- [ ] Integration with EHR systems
- [ ] Advanced analytics and reporting
- [ ] Mobile app development
- [ ] Multi-language support
- [ ] Calendar integration (Google Calendar, Outlook)
- [ ] Video consultation scheduling
- [ ] Prescription reminder system

## 🏆 Features in Detail

### Smart Scheduling
- **New Patients**: Extended time for intake and registration
- **Returning Patients**: Optimized durations based on visit history
- **Specialty Consultations**: Automatic duration adjustment by medical specialty
- **Follow-up Visits**: Shortened time blocks for routine check-ins

### Reminder System
1. **Regular Reminder** (24h before): Appointment details and preparation instructions
2. **Form Completion Check** (4h before): Verify intake forms are completed
3. **Final Confirmation** (1h before): Confirm attendance or collect cancellation reason

### Insurance Validation
- Real-time carrier verification
- Member ID format validation
- Group number verification
- Copay estimation
- Coverage status checking

---

**Built with ❤️ Charul Chim Generative AI Enthusiast **
