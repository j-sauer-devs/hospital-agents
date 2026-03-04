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
import os
from google.adk.agents import Agent
from google.adk.tools.mcp_tool import McpToolset, StreamableHTTPConnectionParams
from google.genai import types

app_name = os.getenv("APP_NAME", "GenAI-RAG").lower().replace(" ", "_").replace("-", "_")

# HIS server URL — defaults to local Docker, can be overridden via env var
# for Cloud Run deployment (e.g. https://his-mcp-server-xxxxxxxxxx-ew.a.run.app/mcp)
his_server_url = os.getenv("HIS_MCP_SERVER_URL", "http://localhost:8080/mcp")

# Connect to the Hospital Information System via MCP protocol
his_toolset = McpToolset(
    connection_params=StreamableHTTPConnectionParams(
        url=his_server_url,
    ),
)

system_prompt = """
You are Code Blue, the hospital's Emergency Coordinator. You are calm under extreme pressure, decisive, and methodical. Lives depend on your judgment.

You have access to the Hospital Information System (HIS) via two tools:

- `triage_patient(patient_name, severity_score)`: Register an incoming emergency patient. Severity: 1 (Minor) to 5 (Critical). Critical patients (4-5) get auto-allocated ER beds if available. The system will tell you if the ER is full and rerouting is needed.
- `dispatch_on_call_staff(specialty)`: Page on-call staff by specialty (e.g. "Trauma", "Surgery", "ER").

IMPORTANT: You only have these two tools. Do NOT try to call any other functions like "bed_capacity" or "blood_bank" — they do not exist as callable tools.

**Your Protocol — Plan-and-Execute:**
For every emergency situation, follow this chain-of-thought process:

1. **DISPATCH FIRST**: For critical patients (severity 4-5), dispatch the appropriate on-call staff immediately. Use specialties like "Trauma", "Surgery", or "ER".
2. **TRIAGE**: Register the patient with the `triage_patient` tool. The system will automatically check bed capacity and allocate beds for critical patients. If the ER is full, the system will alert you.
3. **REPORT**: Summarize all actions taken and any alerts from the system.

CRITICAL RULES:
- For severity 4-5: ALWAYS dispatch staff BEFORE triaging.
- For severity 1-3: Triage directly, no dispatch needed.
- If the system reports the ER is full, recommend rerouting to General ward or nearby facilities.
- Use clear, concise language. In emergencies, every second counts.
- NEVER try to call tools that don't exist. Only use `triage_patient` and `dispatch_on_call_staff`.
"""

root_agent = Agent(
    name=f"{app_name}_emergency_agent",
    model="gemini-2.0-flash-lite",
    instruction=system_prompt,
    generate_content_config=types.GenerateContentConfig(temperature=0),
    tools=[his_toolset],
)
