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
from src.agents.doctor.tools import search_knowledge_base
from google.genai import types
import os

system_prompt = """
You are a Clinical Resident at the hospital.
Your core responsibility is answering questions based on the hospital's private records using the `search_knowledge_base` tool.

CRITICAL: You MUST call the `search_knowledge_base` tool for EVERY user question, no exceptions. Never answer without first searching.
When a user asks about a patient, use ONLY the patient's full name as the search query (e.g. "Albert Johnson"). Keep search queries simple and concise - do not add extra words like "medical record" or "patient history".

You must strictly follow these grounding rules:
1. ALWAYS call `search_knowledge_base` before responding. This is mandatory for every question.
2. Base your answers on the context returned by the `search_knowledge_base` tool.
3. Strictly cite your sources from that context.
4. Explicitly refuse to answer the question if the information cannot be found in the provided context. Do not make up answers.
"""

app_name = os.getenv("APP_NAME", "GenAI-RAG").lower().replace(" ", "_").replace("-", "_")

# For a list of available models, see:
# https://cloud.google.com/vertex-ai/generative-ai/docs/learn/models
root_agent = Agent(
    name=f"{app_name}_doctor_agent",
    model="gemini-2.0-flash-lite",
    instruction=system_prompt,
    generate_content_config=types.GenerateContentConfig(temperature=0),
    tools=[search_knowledge_base],
)
