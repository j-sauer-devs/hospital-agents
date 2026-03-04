import random
import os
from datetime import datetime
from fastmcp import FastMCP
from starlette.responses import JSONResponse

# Initialize the MCP Server
mcp = FastMCP("Hospital-Information-System")

# --- Mock Data Store ---
hospital_data = {
    "beds": {
        "ICU": {"total": 20, "occupied": 18},
        "ER": {"total": 50, "occupied": 45},
        "General": {"total": 200, "occupied": 150}
    },
    "staff_on_call": ["Dr. Smith (Trauma)", "Dr. Jones (Surgery)", "Nurse Chen (ER)"],
    "blood_inventory": {"O-": 4, "A+": 12, "B-": 3}
}

@mcp.custom_route("/", methods=["GET"])
async def health_check(request):
    return JSONResponse({"status": "healthy", "service": "his-mcp-server"})

# --- MCP RESOURCES (Read-only Context) ---

@mcp.resource("his://live/bed-capacity")
def get_bed_capacity() -> str:
    """Provides real-time bed occupancy across all departments."""
    summary = ["Current Bed Status:"]
    for dept, counts in hospital_data["beds"].items():
        summary.append(f"- {dept}: {counts['occupied']}/{counts['total']} beds used")
    return "\n".join(summary)

@mcp.resource("his://live/blood-bank")
def get_blood_status() -> str:
    """Returns current critical blood supply levels."""
    levels = [f"{k}: {v} units" for k, v in hospital_data["blood_inventory"].items()]
    return "Blood Bank Inventory:\n" + "\n".join(levels)

# --- MCP TOOLS (Actions the Agent can take) ---

@mcp.tool()
def triage_patient(patient_name: str, severity_score: int) -> str:
    """
    Registers an incoming emergency patient into the HIS.
    severity_score: 1 (Minor) to 5 (Critical)
    """
    timestamp = datetime.now().strftime("%H:%M:%S")
    if severity_score >= 4:
        # Simulate logic: If severity is high, auto-allocate a bed if available
        if hospital_data["beds"]["ER"]["occupied"] < hospital_data["beds"]["ER"]["total"]:
            hospital_data["beds"]["ER"]["occupied"] += 1
            return f"[{timestamp}] ALERT: {patient_name} (Severity {severity_score}) triaged. ER bed allocated."
        else:
            return f"[{timestamp}] CRITICAL: {patient_name} arriving. ER IS FULL. Reroute required."
    
    return f"[{timestamp}] {patient_name} triaged and added to general waiting list."

@mcp.tool()
def dispatch_on_call_staff(specialty: str) -> str:
    """Pings on-call staff via the hospital pager system."""
    for staff in hospital_data["staff_on_call"]:
        if specialty.lower() in staff.lower():
            return f"SUCCESS: {staff} has been notified and is en route to the ER."
    return f"ERROR: No on-call staff found for {specialty}. Check backup schedules."

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8080))
    mcp.run(transport="http", host="0.0.0.0", port=port)