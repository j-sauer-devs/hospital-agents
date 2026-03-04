# The Multi-Agent Hospital Challenge

Welcome to the Multi-Agent Hospital Challenge! This guide is designed to take you on a learning journey through the Google Agent Development Kit (ADK). 

You will build a sophisticated, modular hospital system by creating a series of specialized agents. We have structured this challenge to progress from **least complex to most complex**, allowing you to incrementally build your skills in agent design, tool integration, and orchestration.

---


## Level 1: The Doctor Agent (RAG & Grounded Reasoning)
**Complexity: Easy**

Next, you will build an agent capable of reasoning over private, unstructured data. This introduces Retrieval-Augmented Generation (RAG).

*   **Location:** `src/agents/doctor/`
*   **The Mission:** Transform this agent into a medical reasoning expert that answers questions based on the hospital's private records.
*   **Key Skills:**
    *   **RAG Integration:** Connect the `search_knowledge_base` tool to Vertex AI Search.
    *   **Strict Grounding:** Give the agent a "Clinical Resident" persona. The core challenge is instructing the LLM to strictly cite its sources from the RAG tool and to explicitly refuse to answer if the information is not found in the provided context.

---


## Level 2: The Receptionist Agent (Tool Use & Constrained Action)
**Complexity: Medium**

Your next task is to build an agent that interacts with external systems using defined tools. This introduces the basics of tool calling and persona constraints.

*   **Location:** `src/agents/receptionist/`
*   **The Mission:** Enable the system to handle administrative tasks like researching existing schedules and medication collection status.
*   **Key Skills:**
    *   **Tool Integration:** Implement two new tools in `tools.py`: one to check existing appointments and another to check medication collection status for a patient (using an in-memory dictionary for mock data). Then register these tools in `agent.py`.
    *   **Persona Design:** Create a "Hospital Receptionist" persona in `agent.py`. The challenge here is ensuring the agent *must* gather the required parameters (like patient name) from the user *before* executing the specific lookup tools.

---


## Level 3: The Researcher Agent (External Search & Synthesis)
**Complexity: High**

Now, bridge the gap between internal hospital data and global knowledge. This agent must use multiple tools and synthesize complex information.

*   **Location:** `src/agents/researcher/`
*   **The Mission:** Build an academic explorer that can compare local patient trends against global medical research.
*   **Key Skills:**
    *   **External Tooling:** Implement a tool that interfaces with Google Search (via the `google-genai` SDK or a public API) to map contemporary medical literature.
    *   **Multi-Tool Synthesis:** The agent must be able to use *both* the internal RAG tool (to find local trends) and the external search tool (to find global context), synthesizing the results into a cohesive research summary.

---

## Level 4: The Orchestrator Agent ("The Final Boss")
**Complexity: Expert**

With your team of specialists built, you must now build the intelligence that manages them. This introduces the concept of Agent-to-Agent (A2A) orchestration.

*   **Location:** `src/agents/orchestrator/`
*   **The Mission:** Build a primary interface that acts as a Triage Specialist, routing user requests to the correct sub-agent.
*   **Key Skills:**
    *   **Agent-as-a-Tool (A2A):** Use the ADK to register the Doctor, Receptionist, and Researcher agents as `tools` available to the Orchestrator Agent.
    *   **Routing Logic:** Design system instructions that allow the Orchestrator Agent to accurately determine user intent, delegate the task, and seamlessly pass the response back to the user without losing context.

---

## Level 5: The Emergency Agent (Live System Interaction)
**Complexity: Master**

This final challenge moves beyond internal data and simple APIs to interacting with a live, stateful, external system. You will build an agent that can manage a hospital-wide emergency by connecting to a mock Hospital Information System (HIS).

*   **Location:** `src/agents/emergency/`
*   **The Mission:** Build an automated crisis coordinator. This agent must connect to the running HIS server to monitor hospital status, triage incoming patients based on real-time data (like bed capacity), and dispatch the appropriate on-call staff to where they are needed most.
*   **Key Skills:**
    *   **External System Integration:** The first step is to set up and run the external HIS server (via Docker or Cloud Run), and then configure your agent to use it as its primary tool.
    *   **Stateful Reasoning:** The agent's core logic must be able to check the state of the hospital *before* taking an action. For example, it must check `his://live/bed-capacity` before deciding to `triage_patient`.
    *   **Chain-of-Thought Planning:** In a complex emergency, the agent must make a series of decisions in a logical order. For example: check beds, check blood supply, dispatch staff, *then* begin triaging new arrivals.
    *   **Crisis Persona Design:** The agent's instructions are critical. It needs the persona of a calm, decisive, and efficient hospital emergency manager to reason correctly under pressure.
