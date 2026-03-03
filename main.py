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
# main.py (Migrated)
import argparse
import asyncio
from google.adk.runners import InMemoryRunner
from src.agents.doctor.agent import root_agent as doctor_agent
from src.agents.receptionist.agent import root_agent as receptionist_agent
from src.agents.master.agent import root_agent as master_agent
from src.ingestion.pipeline import run_ingestion
from src.shared.logger import setup_logger
from src.shared.validator import validate_datastore
import os

logger = setup_logger(__name__)
app_name = os.getenv("APP_NAME", "GenAI-RAG")

AGENTS = {
    "doctor": doctor_agent,
    "receptionist": receptionist_agent,
    "master": master_agent,
}


def run_chat_mode(agent_name: str):
    logger.info(f"Initializing ADK Chat with agent: {agent_name}...")

    print(f"--- {app_name} ADK Chatbot ({agent_name}) ---")
    print("Type 'exit' to quit.")
    
    agent = AGENTS.get(agent_name)
    if not agent:
        logger.critical(f"Agent '{agent_name}' not found.")
        return

    runner = InMemoryRunner(agent=agent)
    
    # Use the ADK's built-in debug runner for interactive chat
    # This handles the user input loop.
    async def chat():
        while True:
            user_input = input("\nYou: ")
            if user_input.lower() in ["exit", "quit"]:
                break
            await runner.run_debug(user_input)

    asyncio.run(chat())


def main():
    parser = argparse.ArgumentParser(description=f"{app_name} RAG Agent CLI")
    parser.add_argument(
        "--mode",
        choices=["chat", "ingest"],
        required=True,
        help="The mode to run the application in.",
    )
    parser.add_argument(
        "--agent",
        choices=list(AGENTS.keys()),
        default="doctor",
        help="The agent to chat with (default: doctor).",
    )
    args = parser.parse_args()

    # Validate common environment variables
    project_id = os.getenv("PROJECT_ID")
    location = os.getenv("LOCATION")
    data_store_id = os.getenv("DATA_STORE_ID")
    # The ADK runner will automatically pick up the VERTEX_AI_REGION
    if not all([project_id, location, data_store_id, os.getenv("VERTEX_AI_REGION")]):
        logger.critical("Error: PROJECT_ID, LOCATION, VERTEX_AI_REGION and DATA_STORE_ID must be set in your .env file.")
        return

    try:
        validate_datastore(project_id, location, data_store_id)
    except ValueError as e:
        logger.critical(f"Datastore validation failed: {e}")
        return
    except Exception as e:
        logger.critical(f"An unhandled error occurred: {e}")
        return

    if args.mode == "chat":
        logger.info(f"Starting chat mode with agent: {args.agent}...")
        run_chat_mode(args.agent)
    elif args.mode == "ingest":
        logger.info("Starting ingestion mode...")
        run_ingestion(input_dir="data/raw", output_dir="data/processed")
        logger.info("Ingestion mode finished.")

if __name__ == "__main__":
    main()
