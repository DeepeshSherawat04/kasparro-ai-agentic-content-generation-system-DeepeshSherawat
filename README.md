Kasparro – Agentic Content Generation System
Author: Deepesh Sherawat

This project is a small demonstration of how an agent-based content pipeline can be organised in a clean, modular way. The idea is straightforward: start with a compact product dataset and generate three separate content pages from it — a FAQ page, a product information page, and a comparison page — all in structured JSON.

The focus is on engineering design rather than writing long pieces of content. Most of the thinking went into how the agents interact, how the logic is broken into reusable blocks, and how templates keep the output predictable.

How the System Works

The pipeline runs in a few clear steps:

-> ParserAgent
Reads the raw JSON file and converts it into a typed Product object.

-> QuestionGenerationAgent
Creates a set of user-oriented questions divided into categories.

-> FAQPageAgent
Answers those questions using a small rule engine built only on the product data.

-> ProductPageAgent
Builds a structured product page by combining several reusable blocks.

-> ComparisonPageAgent
Generates a fictional second product, compares it with the original, and produces a summary.

-> PipelineOrchestrator
Runs all the agents in order and writes out the final files.

All generated pages are saved inside the output/ directory:

-> faq.json

-> product_page.json

->comparison_page.json

Running the Project

From the project root, simply run:

python main.py


Once finished, the output JSON files will appear in the output/ folder.

Project Structure -
agents/          → All agents: parser, FAQ, product page, comparison
blocks/          → Reusable logic blocks
templates/       → Page templates that define output structure
orchestrator/    → The main pipeline workflow
output/          → Generated JSON files
docs/            → Documentation
data/            → Input product data


Each folder has a clear purpose, and no component relies on hidden global state.

Design Approach -

The overall design keeps things simple and reliable:

-> Each agent is responsible for a single step.

-> Logic blocks are used instead of hardcoding logic inside agents.

-> Templates only define structure, not behaviour.

-> The system remains deterministic — every output comes strictly from the input dataset.

-> Adding new content types should not require rewriting the existing flow.

This makes the project easy to understand and easier to extend.

Closing Notes:

The project is intentionally lightweight, but the structure resembles what you would expect from a real-world automated content system. The emphasis was on clarity and modularity rather than over-engineering or creating overly complex abstractions.
With more time, I would consider adding caching, per-block unit tests, and configuration options, but for the scope of this assignment, the system demonstrates the core ideas well.