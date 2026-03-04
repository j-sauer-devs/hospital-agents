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
from google.adk.tools.agent_tool import AgentTool
from google.genai import types

# Import the root_agent from the other agent files
from src.agents.doctor.agent import root_agent as doctor_agent
from src.agents.receptionist.agent import root_agent as receptionist_agent
from src.agents.researcher.agent import root_agent as researcher_agent

# TODO: Refine this placeholder persona into a "Triage Specialist". 
# It should be instructed to accurately determine user intent (e.g., medical query, appointment, research)
# and delegate to the appropriate sub-agent while maintaining context.
system_prompt = "You are an orchestrator agent. Talk to doctor or receptionist if needed."

app_name = os.getenv("APP_NAME", "hospital").lower().replace("-", "_")

# This agent connects the others as tools (Agent-as-a-Tool)
root_agent = Agent(
    name=f"{app_name}_orchestrator_agent",
    model="gemini-2.0-flash-lite",
    instruction=system_prompt,
    tools=[
        AgentTool(agent=doctor_agent),
        AgentTool(agent=receptionist_agent),
        AgentTool(agent=researcher_agent),
    ],
    generate_content_config=types.GenerateContentConfig(temperature=0), 
)
