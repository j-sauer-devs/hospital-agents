# Challenge: The Emergency Agent

Welcome to the next level. In this challenge, you will build an "Emergency" agent that can manage a hospital-wide emergency. This agent will act as an automated emergency coordinator, using the Hospital Information System (HIS) to make critical decisions.

## The Mission

Your goal is to build an agent that can:

1.  **Monitor Hospital Status:** Continuously assess the hospital's critical resources.
2.  **Triage Incoming Patients:** Make decisions about where to send new patients based on their severity and the hospital's capacity.
3.  **Coordinate Staff:** Dispatch the correct on-call staff to where they are needed most.

## Your Interface: The HIS-MCP Server

This challenge uses a mock Hospital Information System (HIS) that runs as a separate server. You can run it locally in a Docker container or deploy it to the cloud.

### Local Server Setup

**Important:** The python script is named `mcp-server.py` but the `Dockerfile` is expecting `main.py`. Before building, please rename the file:

```bash
mv mcp-server.py main.py
```

**1. Build the Docker Image:**
From within the `src/agents/emergency` directory, run:
```bash
docker build -t his-mcp-server .
```

**2. Run the Docker Container:**
```bash
docker run -p 8080:8080 his-mcp-server
```

The server will then be available at `http://localhost:8080`.

### Deploying to Google Cloud Run (Optional)

You can also deploy the server to a public URL using Google Cloud Run. This is a great way to share your server with team members.

**1. Prerequisite: Rename the file**
Just like for the local setup, you must first rename the server file:
```bash
mv mcp-server.py main.py
```

**2. Deploy:**
Run the following `gcloud` command from this directory:
```bash
gcloud run deploy his-mcp-server --source . --region=europe-west4 --allow-unauthenticated
```
This single command will build your container, push it to the Google Container Registry, and deploy it. The `--allow-unauthenticated` flag makes the service public so you can easily test it without needing to configure authentication.

## Key Skills

This challenge will test your ability to:

*   **Design a Persona:** How do you instruct an agent to behave in a crisis?
*   **Utilize MCP Tools:** How do you make an agent "aware" of an external API?
*   **Stateful Reasoning:** Can your agent check the state of the hospital (e.g., bed capacity) and then take an action that changes that state?
*   **Chain of Thought:** Can your agent make a series of decisions in a logical order?

## Getting Started

1.  Create your agent's files (e.g., `agent.py`, `tools.py`) inside this directory.
2.  Your agent will need to be configured to connect to your MCP server's address (either `http://localhost:8080` or your public Cloud Run URL).
3.  Design your agent's instructions to give it the persona of a calm, decisive, and efficient hospital emergency manager.

## Connecting Your Agent to the MCP Server

To interact with the HIS server, your agent will need to use an MCP (Model Context Protocol) client. You will instantiate this client in your code, pointing it at the URL where your server is running.

Here are pseudo-code examples for both local and deployed servers:

### Connecting to a Local Server

```python
# PSEUDO-CODE
from adk.mcp import MCPClient

# The server is running in Docker on your local machine
server_url = "http://localhost:8080/mcp"

# Your agent will use this client to call tools and get resources
his_client = MCPClient(url=server_url)

# Example: Get the bed capacity
bed_status = his_client.get("his://live/bed-capacity")
```

### Connecting to a GCP Cloud Run Server

When you deploy your server to Cloud Run, it will give you a public URL. You simply use that URL instead.

```python
# PSEUDO-CODE
from adk.mcp import MCPClient

# Get the URL from your `gcloud run deploy` command's output
# It will look something like: https://his-mcp-server-xxxxxxxxxx-ew.a.run.app
server_url = "YOUR_CLOUD_RUN_SERVICE_URL/mcp"

# Your agent connects to the public URL
his_client = MCPClient(url=server_url)

# The usage is exactly the same
bed_status = his_client.get("his://live/bed-capacity")
```

Good luck.
