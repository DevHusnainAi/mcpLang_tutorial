FROM langchain/langgraph-api:3.13

# Add the source code to the container
ADD . /deps/lead_flow_agent

# Set the working directory
WORKDIR /deps/lead_flow_agent

# Upgrade pip
RUN pip install --upgrade pip

# Install the necessary Python dependencies
RUN PYTHONDONTWRITEBYTECODE=1 pip install --no-cache-dir -c /api/constraints.txt -e /deps/*

# Set environment variables
ENV LANGSERVE_GRAPHS='{"lead_flow_agent": "./src/lead_flow_agent/entrypoint.py:lead_flow_agent"}'

WORKDIR /deps/lead_flow_agent