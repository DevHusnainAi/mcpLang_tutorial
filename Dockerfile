FROM langchain/langgraph-api:3.13

# Add the source code to the container
ADD . /deps/lang_mcp_tutorial

# Set the working directory
WORKDIR /deps/lang_mcp_tutorial

# Upgrade pip
RUN pip install --upgrade pip

# Install the necessary Python dependencies
RUN PYTHONDONTWRITEBYTECODE=1 pip install --no-cache-dir -c /api/constraints.txt -e /deps/*

# Set environment variables
ENV LANGSERVE_GRAPHS='{"lang_mcp_tutorial": "./src/lang_mcp_tutorial/entrypoint.py:lang_mcp_tutorial"}'

WORKDIR /deps/lang_mcp_tutorial