# Copyright 2025 Google LLC
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may
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
from google.adk.agents import Agent
from src.agents.receptionist.tools import (
    view_available_slots,
    book_appointment,
    check_existing_appointments,
    medication_collection_status,
)
from google.genai import types
import os


system_prompt = """
You are a helpful and friendly hospital receptionist.
Your primary role is to assist patients with scheduling, managing their appointments, and checking medication collection status.

You have the following tools available:
- `view_available_slots`: Check available appointment slots for a given date.
- `book_appointment`: Book a new appointment for a patient.
- `check_existing_appointments`: Look up a patient's existing upcoming appointments.
- `medication_collection_status`: Check whether a patient's medication has been collected, is pending, or has not been collected.

Always use the appropriate tool to answer patient questions. When booking an appointment, make sure to collect the patient's full name and the reason for their visit.
Be polite and professional in all your interactions.
"""

app_name = os.getenv("APP_NAME", "GenAI-RAG").lower().replace(" ", "_").replace("-", "_")

# For a list of available models, see:
# https://cloud.google.com/vertex-ai/generative-ai/docs/learn/models
root_agent = Agent(
    name=f"{app_name}_receptionist_agent",
    description="Handles scheduling and logistics. Can check existing appointments, book new ones, view available slots, and check medication collection status. Returns specific dates, times, and status details.",
    model="gemini-2.0-flash-lite",
    instruction=system_prompt,
    tools=[view_available_slots, book_appointment, check_existing_appointments, medication_collection_status],
    generate_content_config=types.GenerateContentConfig(temperature=0),
)
