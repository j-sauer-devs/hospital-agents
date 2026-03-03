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
