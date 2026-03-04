# Use an official lightweight Python image
FROM python:3.11-slim

# Set the working directory in the container
WORKDIR /app

# Install dependencies
# We install fastmcp and uvicorn (needed for the SSE web server)
RUN pip install --no-cache-dir fastmcp uvicorn starlette

# Copy the server code into the container
COPY main.py .

# Expose the port Cloud Run will use
EXPOSE 8080

# Run the MCP server using the SSE transport
# FastMCP handles the uvicorn execution under the hood when transport="sse"
CMD ["python", "main.py"]