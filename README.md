# Kasparro Agentic Content Generation System  
### Built with LangChain · Ollama · Modular Logic Blocks

**Author:** Deepesh Sherawat

This project implements a small yet production-style **agentic AI system** using **LangChain**.  
The system reads a single product JSON file and automatically generates:

- `faq.json` – Structured FAQ content  
- `product_page.json` – Detailed product information  
- `comparison_page.json` – Comparison with a fictional competitor  

The design focuses on **modularity**, **tool-assisted reasoning**, and **clean agent boundaries**.  
All content is generated using **LangChain agents**, not custom scripting, to meet real agentic-framework design expectations.

---

## Features

- **True multi-agent workflow** (LangChain agents, not manual orchestration)  
- **Tool-driven data access** to prevent hallucinations  
- **Local LLM inference** using *Ollama*  
- **Deterministic logic blocks** for safety, pricing, usage, benefits, etc.  
- **Structured JSON outputs** suitable for automation pipelines  
- **Clear separation of templates, tools, agents, and processing logic**

---

## Quick Start

1. Create a virtual environment
```bash
python -m venv .venv

2. Activate the environment
# Windows
.venv\Scripts\activate

# macOS/Linux
source .venv/bin/activate

3. Install dependencies
pip install -r requirements.txt

4. Make sure Ollama is running
ollama serve

5. Run the pipeline
python main.py

Output Files

After execution, the following files are generated:

output/
│── faq.json
│── product_page.json
└── comparison_page.json


All follow strict machine-readable schemas.

Project Structure
.
├── agents/
│   ├── langchain_tools.py      # Tools used by agents
│   └── parser_agent.py         # Converts input JSON into model
├── blocks/
│   ├── product_blocks.py
│   ├── usage_blocks.py
│   ├── benefits_blocks.py
│   └── comparison_blocks.py
├── orchestrator/
│   └── pipeline.py             # LangChain-driven agent workflow
├── data/
│   └── product_input.json
├── output/                     # Generated files
├── tests/
│   └── test_pipeline.py
└── requirements.txt

 Running Tests
pytest -q

 What This Project Demonstrates

Clean engineering principles for agent systems

Proper usage of LangChain as an orchestration framework

Modular & deterministic content generation

Realistic architecture similar to production-ready AI pipelines