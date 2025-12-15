# Kasparro Agentic Content Generation System

**Built with LangGraph · LangChain · Ollama · Modular Logic Blocks**

**Author:** Deepesh Sherawat

---

## Overview

This project implements a production-style **multi-agent AI system** using **LangGraph** and **LangChain**.  
The system reads a single product JSON file and automatically generates:

- `faq.json` – Structured FAQ content with 15+ questions
- `product_page.json` – Detailed product information
- `comparison_page.json` – Comparison with a fictional competitor

The design focuses on **modularity**, **state machine orchestration**, and **clean agent boundaries**.

---

## Features

✅ **True multi-agent workflow** using LangGraph StateGraph  
✅ **5 specialized agents** with single responsibilities  
✅ **Tool-driven data access** to prevent hallucinations  
✅ **Local LLM inference** using Ollama (llama3.1)  
✅ **Deterministic logic blocks** for safety, pricing, usage, benefits  
✅ **Structured JSON outputs** suitable for automation pipelines  
✅ **Guaranteed 15+ FAQ questions** with intelligent fallback  
✅ **Error handling and validation** at all boundaries

---

## Quick Start

### Prerequisites

- Python 3.10+
- Ollama installed and running
- llama3.1 model downloaded

### Installation

```bash
# 1. Clone the repository
git clone <your-repo-url>
cd kasparro-agentic-DeepeshSherawat

# 2. Create virtual environment
python -m venv .venv

# 3. Activate environment
# Windows:
.venv\Scripts\Activate.ps1
# macOS/Linux:
source .venv/bin/activate

# 4. Install dependencies
pip install -r requirements.txt

# 5. Ensure Ollama is running
ollama serve

ollama run llama3.1

# 6. Pull the required model (if not already done)
ollama pull llama3.1
```

### Running the System

```bash
# Run the complete pipeline
python main.py
```

### Expected Output

```
======================================================================
🚀 MULTI-AGENT CONTENT GENERATION SYSTEM
======================================================================
[INFO] ✓ Ollama LLM initialized successfully
[AGENT 1] Product Parser - Running...
[AGENT 1] ✓ Parsed: GlowBoost Vitamin C Serum
[AGENT 2] Question Generator - Running...
[AGENT 2] ✓ Generated 15 questions via LLM
[AGENT 3] FAQ Generator - Running...
[AGENT 3] ✓ Generated FAQ with 15 Q&As
[AGENT 4] Product Page Generator - Running...
[AGENT 4] ✓ Generated product page
[AGENT 5] Comparison Page Generator - Running...
[AGENT 5] ✓ Generated comparison page
[OUTPUT] Writing files...
[OUTPUT] ✓ Successfully wrote:
  → output/faq.json
  → output/product_page.json
  → output/comparison_page.json
======================================================================
✅ PIPELINE COMPLETED SUCCESSFULLY
======================================================================
📊 Total Questions Generated: 15 (Required: ≥15)
```

---

## Output Files

After execution, the following files are generated in the `output/` directory:

```
output/
├── faq.json                 # 15+ categorized Q&A pairs
├── product_page.json        # Complete product description
└── comparison_page.json     # Product comparison table
```

All files follow strict machine-readable JSON schemas.

---

## Project Structure

```
kasparro-agentic-DeepeshSherawat/
├── agents/
│   ├── content_logic.py          # Reusable content generation blocks
│   ├── langchain_tools.py        # LangChain tools (@tool decorator)
│   └── parser_agent.py           # Product data parser with validation
├── orchestrator/
│   └── pipeline.py               # LangGraph StateGraph orchestration
├── data/
│   ├── product_input.json        # Input product data
│   └── product_b.json            # Fictional competitor product
├── output/                       # Generated JSON files (auto-created)
├── tests/
│   └── test_pipeline.py          # Unit and integration tests
├── docs/
│   └── projectdocumentation.md   # Technical documentation
├── main.py                       # Entry point
├── requirements.txt              # Python dependencies
└── README.md                     # This file
```

---

## Architecture

### Multi-Agent State Machine

The system uses **LangGraph** to create a true state machine with 5 specialized agents:

```
START → Parser → Question Gen → FAQ Gen → Product Page → Comparison → Write → END
```

Each agent has:
- **Single responsibility**
- **Defined input/output** via shared state
- **No side effects** (pure functions)

### Agent Responsibilities

| Agent | Purpose |
|------------------|---------------|
| **Parser Agent** | Validates and parses `product_input.json` |
| **Question Generation Agent** | Creates 15+ categorized questions using LLM |
| **FAQ Page Agent** | Answers questions using only product data |
| **Product Page Agent** | Generates structured product description |
| **Comparison Page Agent** | Compares with fictional Product B |

### State Flow

```python
class AgentState(TypedDict, total=False):
    product_json: str           # Parsed product data
    questions: list             # Generated questions
    faq_json: dict             # FAQ page structure
    product_page_json: dict    # Product page structure
    comparison_page_json: dict # Comparison page structure
```

---

## Running Tests

```bash
# Run all tests
pytest tests/test_pipeline.py -v

# Run specific test
pytest tests/test_pipeline.py::test_parser_agent -v
```

### Test Coverage

- ✅ Product parsing and validation
- ✅ Content logic blocks
- ✅ End-to-end pipeline execution
- ✅ Output file generation

---

## Key Design Decisions

### 1. LangGraph State Machine (Not Manual Loops)
Uses proper state machine orchestration instead of sequential Python loops.

### 2. Deterministic Fallbacks
If LLM fails, the system uses guaranteed fallback logic (e.g., 15 hardcoded questions).

### 3. Tool-Based Architecture
LangChain `@tool` decorator ensures type safety and documentation.

### 4. Data Isolation
Answers are generated **only** from `product_input.json` - no external knowledge.

### 5. Error Handling
- File validation at parser
- JSON parsing with clear errors
- LLM timeout handling (120s)
- Graceful fallback mechanisms

---

## Dependencies

Core dependencies (see `requirements.txt`):

```txt
langchain==1.1.3                   # LangChain core
langchain-community>=0.4.0         
langchain-core>=1.2.0              # langchain primitives
langgraph>=0.0.50                  # state machine orchestration
langchain-ollama>=0.3.4             # Ollama integration
ollama>=0.6.0                       # Ollama Client
python-dotenv>=0.21.1               # Environment variables
pytest>=9.0.2                       # Testing framework
pytest-mock==3.15.1
```

---

## Configuration

The system uses sensible defaults but can be configured:

### LLM Settings (in `orchestrator/pipeline.py`)

```python
llm = ChatOllama(
    model="llama3.1",      # Change model here
    temperature=0.7,       # Creativity level
    timeout=120,           # Request timeout
    num_ctx=4096,         # Context window
)
```

### Input Data Format

`data/product_input.json` must contain:

```json
{
  "name": "string",
  "concentration": "string",
  "skin_type": ["string"],
  "key_ingredients": ["string"],
  "benefits": ["string"],
  "how_to_use": "string",
  "side_effects": "string",
  "price": number
}
```

---

## What This Project Demonstrates

✅ **Production-grade multi-agent architecture**  
✅ **Proper use of LangGraph for orchestration**  
✅ **Modular and testable design**  
✅ **Type safety and validation**  
✅ **Error handling and resilience**  
✅ **Clean separation of concerns**  
✅ **Deterministic content generation**  
✅ **No hallucinations** (data-driven answers)

---

## Troubleshooting

### "Ollama server not running"
```bash
# Start Ollama
ollama serve
```

### "Model not found"
```bash
# Pull the model
ollama pull llama3.1
```

### "LLM generation failed"
The system automatically falls back to deterministic question generation. This is by design and ensures 15+ questions are always generated.

### "Import errors"
```bash
# Reinstall dependencies
pip install -r requirements.txt --force-reinstall
```

---

## License

This project is part of the Kasparro AI Engineer assessment.

---

## Contact

**Deepesh Sherawat**  
For questions or issues, please refer to the technical documentation in `docs/projectdocumentation.md`.