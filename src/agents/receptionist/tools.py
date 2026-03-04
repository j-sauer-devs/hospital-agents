# Copyright 2025 Google LLC
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
import asyncio
import logging
import os
from datetime import date

from fastmcp import FastMCP

# Set up logging
logger = logging.getLogger(__name__)
logging.basicConfig(format="[%(levelname)s]: %(message)s", level=logging.INFO)

mcp = FastMCP("Appointment MCP Server 🗓️")

# In-memory "database" for appointments.
# In a real-world application, this would be a database.
SCHEDULE = {
    "2026-03-04": ["10:00", "14:30"],
    "2026-03-05": ["09:00", "11:00", "15:00"],
}
ALL_SLOTS = ["09:00", "10:00", "11:00", "13:00", "14:00", "15:00", "16:00"]

# In-memory "database" for existing patient appointments.
PATIENT_APPOINTMENTS = {
    "Albert Johnson": [{"date": "2026-03-04", "time": "10:00", "reason": "Follow-up for hypertension"}],
    "Maria Garcia": [{"date": "2026-03-05", "time": "09:00", "reason": "Annual physical exam"}],
    "James Wilson": [{"date": "2026-03-05", "time": "11:00", "reason": "Lab results review"}],
}

# In-memory "database" for medication collection status.
MEDICATION_STATUS = {
    "Albert Johnson": {"medication": "Sumatriptan 50mg", "status": "pending"},
    "Maria Garcia": {"medication": "Metformin 500mg", "status": "collected"},
    "James Wilson": {"medication": "Lisinopril 10mg", "status": "not collected"},
}


@mcp.tool()
def view_available_slots(booking_date: date):
    """Checks the schedule for a given date and returns available appointment slots.

    Args:
        booking_date: The date to check for available slots, in YYYY-MM-DD format.

    Returns:
        A dictionary containing a list of available time slots for the given date.
    """
    logger.info(f"--- 🛠️ Tool: view_available_slots called for date: {booking_date} ---")
    booked_slots = SCHEDULE.get(str(booking_date), [])
    available_slots = [slot for slot in ALL_SLOTS if slot not in booked_slots]
    logger.info(f"✅ Available slots for {booking_date}: {available_slots}")
    return {"date": str(booking_date), "available_slots": available_slots}


@mcp.tool()
def book_appointment(booking_date: date, time: str, patient_name: str, reason: str):
    """Books a new appointment on a specific date and time for a patient.

    Args:
        booking_date: The date for the appointment in YYYY-MM-DD format.
        time: The time for the appointment in HH:MM format.
        patient_name: The full name of the patient.
        reason: A brief reason for the appointment.

    Returns:
        A dictionary with a confirmation message or an error message.
    """
    logger.info(
        f"--- 🛠️ Tool: book_appointment called for {patient_name} on {booking_date} at {time} ---"
    )
    booking_date_str = str(booking_date)

    # Check if the date exists, if not, create it
    if booking_date_str not in SCHEDULE:
        SCHEDULE[booking_date_str] = []

    # Check if the slot is valid and available
    if time not in ALL_SLOTS:
        error_msg = f"Error: The time slot {time} is not a valid appointment time."
        logger.error(error_msg)
        return {"error": error_msg}

    if time in SCHEDULE[booking_date_str]:
        error_msg = f"Error: The time slot {time} on {booking_date_str} is already booked."
        logger.error(error_msg)
        return {"error": error_msg}

    # Book the appointment
    SCHEDULE[booking_date_str].append(time)
    confirmation_msg = f"Success: Appointment confirmed for {patient_name} on {booking_date_str} at {time} for: {reason}."
    logger.info(f"✅ {confirmation_msg}")
    # In a real system, we would also save the patient_name and reason.
    return {"status": "confirmed", "message": confirmation_msg}

@mcp.tool()
def check_existing_appointments(patient_name: str):
    """Checks existing appointments for a given patient.

    Args:
        patient_name: The full name of the patient to look up.

    Returns:
        A dictionary containing the patient's upcoming appointments or a message if none are found.
    """
    logger.info(f"--- 🛠️ Tool: check_existing_appointments called for patient: {patient_name} ---")
    appointments = PATIENT_APPOINTMENTS.get(patient_name)
    if appointments:
        logger.info(f"✅ Found {len(appointments)} appointment(s) for {patient_name}")
        return {"patient": patient_name, "appointments": appointments}
    else:
        logger.info(f"ℹ️ No appointments found for {patient_name}")
        return {"patient": patient_name, "message": f"No existing appointments found for {patient_name}."}


@mcp.tool()
def medication_collection_status(patient_name: str):
    """Checks the medication collection status for a given patient.

    Args:
        patient_name: The full name of the patient to look up.

    Returns:
        A dictionary containing the patient's medication name and collection status, or a message if no records are found.
    """
    logger.info(f"--- 🛠️ Tool: medication_collection_status called for patient: {patient_name} ---")
    status = MEDICATION_STATUS.get(patient_name)
    if status:
        logger.info(f"✅ Medication status for {patient_name}: {status['medication']} - {status['status']}")
        return {"patient": patient_name, "medication": status["medication"], "status": status["status"]}
    else:
        logger.info(f"ℹ️ No medication records found for {patient_name}")
        return {"patient": patient_name, "message": f"No medication records found for {patient_name}."}

if __name__ == "__main__":
    port = int(os.getenv("RECEPTIONIST_PORT", 8081))
    logger.info(f"🚀 MCP server started on port {port}")
    asyncio.run(
        mcp.run_async(
            transport="http",
            host="0.0.0.0",
            port=port,
        )
    )
