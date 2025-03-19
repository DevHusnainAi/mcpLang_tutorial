# PanaAI Agents

[![CI](https://github.com/langchain-ai/react-agent/actions/workflows/unit-tests.yml/badge.svg)](https://github.com/langchain-ai/react-agent/actions/workflows/unit-tests.yml)
[![Integration Tests](https://github.com/langchain-ai/react-agent/actions/workflows/integration-tests.yml/badge.svg)](https://github.com/langchain-ai/react-agent/actions/workflows/integration-tests.yml)

## Directory Structure

- All prototyping notebooks are in the prototypes directory.
- All final agents will live in in the src directory.


## Quick Setup
1. Add all environment variables in .env file
2. Run this command to start langgraph studio:

```bash
uvx --refresh --from "langgraph-cli[inmem]" --with-editable . --python 3.11 langgraph dev
```

## Getting Started

### Prerequisites

1. **Install `uv` Package Manager:**
   ```bash
   pip install uv
   ```

### Local Setup

To get startedfollow these steps:

1. **Clone the repository:**

   ```sh
   git clone https://github.com/...
   cd ...
   ```

2. **Create a `.env` file:**

Copy the `.env.example` file to `.env` and update the environment variables as needed:

```sh
cp .env.example .env
```

3. **Run LangGraph Server:**

a. Install uv package manager `python pip install uv`

b. Create Virtual Environment and activate it

```python
uv venv
source .venv/bin/activate
```

for Windows to activate venv

```python
.venv\bin\activate
```

c. Install packages in pyproject.toml

```python
uv run
```

d. Run LangGraph Server

- Ensure you have docker engine running (i.e: Open Docker Desktop)

```python
uv pip install langgraph-cli
uv run langgraph up
```

If you get any error in `d` step stop all containers, run `docker system prune` and try again.
