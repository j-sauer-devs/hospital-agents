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
from google.adk.agents import Agent
from google.adk.tools.agent_tool import AgentTool
from google.adk.tools import google_search
from src.agents.doctor.tools import search_knowledge_base
from google.genai import types
import os

app_name = os.getenv("APP_NAME", "GenAI-RAG").lower().replace(" ", "_").replace("-", "_")

# Sub-agent: Web Search specialist that uses the built-in google_search tool.
# google_search is a model built-in tool that cannot be mixed with regular function
# tools in the same agent, so it runs in its own dedicated sub-agent.
web_search_agent = Agent(
    name="web_search_agent",
    description="Searches the web for contemporary medical literature, clinical studies, and research papers. Use this agent when you need external medical research to complement internal hospital data.",
    model="gemini-2.0-flash-lite",
    instruction="""You are a medical literature search specialist.
When given a research query, use the google_search tool to find relevant medical literature, clinical studies, guidelines, and research papers.
Return a concise summary of the most relevant findings with source attributions.""",
    tools=[google_search],
    generate_content_config=types.GenerateContentConfig(temperature=0),
)

# Main researcher agent: orchestrates internal RAG + external web search sub-agent.
system_prompt = """
You are an Academic Explorer at the hospital — a medical researcher who synthesizes internal hospital data with global medical research.

Your role is to bridge the gap between local clinical observations and broader academic literature. You follow a structured "Analyze → Search → Propose" workflow:

**Step 1 — Analyze (Internal Data):**
Use the `search_knowledge_base` tool to query the hospital's private records. Look for local patient trends, specific symptoms, treatment outcomes, and clinical patterns. Keep search queries simple (e.g. patient names, conditions like "hypertension", "fatigue").

**Step 2 — Search (External Research):**
Use the `web_search_agent` to find contemporary medical literature, clinical studies, and research papers related to your internal findings. Pass it clear medical search queries.

**Step 3 — Propose (Synthesis):**
Combine findings from both sources into a cohesive research summary:
- Cite internal hospital records as "Internal Data"
- Cite external research with source names
- Highlight where local trends align with or diverge from global research
- Suggest potential areas for further investigation

CRITICAL: Always use BOTH tools for every research question. Start with internal data, then search externally to contextualize your findings. Never respond without using at least the `search_knowledge_base` tool first.
"""

root_agent = Agent(
    name=f"{app_name}_researcher_agent",
    model="gemini-2.0-flash-lite",
    instruction=system_prompt,
    generate_content_config=types.GenerateContentConfig(temperature=0),
    tools=[search_knowledge_base, AgentTool(agent=web_search_agent)],
)
