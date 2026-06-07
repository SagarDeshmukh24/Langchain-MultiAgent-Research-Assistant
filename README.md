
# Langchain Multi-Agent Research Assistant

A small research-assistant prototype that coordinates lightweight LangChain-style agents and a processing pipeline to help explore, summarize, and research documents.

## Highlights

- Designed as a modular multi-agent system: agents, pipeline, and tools are separated for clarity and extensibility.
- Lightweight runner scripts: `main.py` and `app.py` provide quick ways to run the assistant.
- Minimal dependencies managed in `requirements.txt` for easy setup.

## Techniques Used

- Agent orchestration (multi-agent coordination) for dividing research tasks.
- Pipeline-based document ingestion and preprocessing for retrieval and RAG workflows.
- Tool interface layer to encapsulate external actions (search, retrieval, web requests, etc.).

## Architecture (brief)

- Entrypoints: `main.py` and `app.py` — start the local assistant or run demo flows.
- Agents: [src/agents/agents.py](src/agents/agents.py) — defines agent roles and coordination logic.
- Pipeline: [src/pipeline/pipeline.py](src/pipeline/pipeline.py) — handles data ingestion, chunking, and preprocessing.
- Tools: [src/tools/tools.py](src/tools/tools.py) — utility/tool wrappers used by agents.
- Package deps: `requirements.txt` — pinned Python packages required to run the project.

## Install (recommended)

Follow these steps to create an isolated environment and install dependencies.

Conda (recommended):

```bash
conda create -n langagent python=3.11 -y
conda activate langagent
pip install -r requirements.txt
```

Virtualenv / venv:

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

## Quick Start

Run the demo runner (choose `main.py` or `app.py` depending on the workflow you prefer):

```bash
python main.py
# or
streamlit run app.py
```

If the project expects additional configuration (API keys, vector DB endpoints), set them as environment variables before running.

## Project Structure

Top-level layout:

```
app.py
main.py
requirements.txt
src/
	agents/
		agents.py
	pipeline/
		pipeline.py
	tools/
		tools.py
```

## Contributing

Contributions are welcome — open an issue or a PR with a short description of your change.


