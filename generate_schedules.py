import pandas as pd
from datetime import datetime, timedelta
import os

# Create doctor schedule data
doctors = [
    {"doctor_id": "DOC001", "name": "Dr. Emily Smith", "specialty": "Family Medicine"},
    {"doctor_id": "DOC002", "name": "Dr. Michael Williams", "specialty": "Internal Medicine"},
    {"doctor_id": "DOC003", "name": "Dr. Sarah Brown", "specialty": "Pediatrics"},
    {"doctor_id": "DOC004", "name": "Dr. Robert Johnson", "specialty": "Cardiology"},
    {"doctor_id": "DOC005", "name": "Dr. Jennifer Davis", "specialty": "Geriatrics"},
    {"doctor_id": "DOC006", "name": "Dr. David Lee", "specialty": "Psychiatry"}
]

# Generate schedule for next 4 weeks
start_date = datetime(2025, 9, 8)  # Starting Monday
schedule_data = []

for week in range(4):
    for day in range(5):  # Monday to Friday
        current_date = start_date + timedelta(weeks=week, days=day)
        day_name = current_date.strftime("%A")
        
        for doctor in doctors:
            # Different schedules for different doctors
            if doctor["doctor_id"] == "DOC001":  # Dr. Smith - Full time
                slots = ["08:00", "08:30", "09:00", "09:30", "10:00", "10:30", "11:00", "11:30", 
                        "13:00", "13:30", "14:00", "14:30", "15:00", "15:30", "16:00", "16:30"]
            elif doctor["doctor_id"] == "DOC002":  # Dr. Williams - Full time
                slots = ["09:00", "09:30", "10:00", "10:30", "11:00", "11:30", 
                        "14:00", "14:30", "15:00", "15:30", "16:00", "16:30"]
            elif doctor["doctor_id"] == "DOC003":  # Dr. Brown - Pediatrics (shorter days)
                slots = ["08:00", "08:30", "09:00", "09:30", "10:00", "10:30", "11:00", "11:30"]
            elif doctor["doctor_id"] == "DOC004":  # Dr. Johnson - Cardiology (part-time)
                if day in [0, 2, 4]:  # Mon, Wed, Fri
                    slots = ["09:00", "10:00", "11:00", "14:00", "15:00", "16:00"]
                else:
                    slots = []
            elif doctor["doctor_id"] == "DOC005":  # Dr. Davis - Geriatrics
                slots = ["08:30", "09:30", "10:30", "11:30", "13:30", "14:30", "15:30"]
            elif doctor["doctor_id"] == "DOC006":  # Dr. Lee - Psychiatry
                slots = ["10:00", "11:00", "14:00", "15:00", "16:00"]
            
            for slot in slots:
                schedule_data.append({
                    "date": current_date.strftime("%Y-%m-%d"),
                    "day_of_week": day_name,
                    "doctor_id": doctor["doctor_id"],
                    "doctor_name": doctor["name"],
                    "specialty": doctor["specialty"],
                    "time_slot": slot,
                    "duration_minutes": 30,
                    "status": "available",
                    "appointment_type": "any",
                    "location": "Main Clinic" if doctor["doctor_id"] in ["DOC001", "DOC002"] else 
                              "Pediatric Center" if doctor["doctor_id"] == "DOC003" else
                              "Specialty Clinic" if doctor["doctor_id"] == "DOC004" else
                              "Senior Care Center" if doctor["doctor_id"] == "DOC005" else
                              "Mental Health Center"
                })

# Create DataFrame and save to Excel
df = pd.DataFrame(schedule_data)

# Create output directory if it doesn't exist
output_dir = "/Users/charulchim/Documents/medical appointment scheduling AI agent/data/doctors"
os.makedirs(output_dir, exist_ok=True)

# Save to Excel with multiple sheets
with pd.ExcelWriter(f"{output_dir}/doctor_schedules.xlsx", engine='openpyxl') as writer:
    # Main schedule sheet
    df.to_excel(writer, sheet_name='All_Schedules', index=False)
    
    # Individual doctor sheets
    for doctor in doctors:
        doctor_schedule = df[df['doctor_id'] == doctor['doctor_id']]
        sheet_name = doctor['name'].replace('Dr. ', '').replace(' ', '_')
        doctor_schedule.to_excel(writer, sheet_name=sheet_name, index=False)

print(f"Generated {len(df)} appointment slots for {len(doctors)} doctors over 4 weeks")
print("Saved to: doctor_schedules.xlsx")
