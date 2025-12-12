# Kasparro – Agentic Content Generation System  
### Technical Documentation  
**Author:** Deepesh Sherawat  

This document explains the architecture, design decisions, and workflow behind the agentic content generation system built using **LangChain** and **Ollama**.

---

## 1. Objective

The goal is to convert a single structured product dataset into:

1. A FAQ page  
2. A detailed product information page  
3. A product comparison page  

All outputs must be:

- JSON formatted  
- Built using **multiple agents**, not a linear script  
- Created using **LangChain tools + model reasoning**  
- Supported by deterministic logic blocks  

The emphasis is on **engineering clarity and real-world agentic design**, not marketing copy.

---

## 2. System Constraints & Assumptions

To keep the workflow controlled and deterministic:

- Only data from `product_input.json` can be used  
- Product B must be fictional but follow the same schema  
- Agents must remain modular and independent  
- Tools expose factual blocks (overview, usage, pricing, benefits, etc.)  
- LLMs must only orchestrate reasoning, not fabricate facts  

These constraints match real-world expectations for safe and reliable product-content generation systems.

---

## 3. System Overview

The complete system consists of **five agents**, **logic blocks**, and **tools**, coordinated via a LangChain-driven pipeline.

### Workflow Summary

- **ParserAgent**  
  Converts JSON → Product model

- **QuestionGenerationAgent**  
  Uses the LLM to create grouped user questions

- **FAQPageAgent**  
  Answers questions using tools, producing structured Q/A pairs

- **ProductPageAgent**  
  Builds the product page using deterministic logic blocks

- **ComparisonPageAgent**  
  Generates a fictional Product B, compares ingredients, and writes a structured summary

- **PipelineOrchestrator**  
  Connects all agents and writes JSON outputs

This modularity ensures maintainability, testability, and clarity.

---

## 4. Architecture Diagram

```mermaid
flowchart TD
    A[product_input.json] --> B[ParserAgent]
    B --> C[QuestionGenerationAgent]
    C --> E[FAQPageAgent]

    B --> D[ProductPageAgent]
    B --> F[ComparisonPageAgent]

    D --> O1[product_page.json]
    E --> O2[faq.json]
    F --> O3[comparison_page.json]
The design enforces strict, one-directional data flow.

5. Agent  Responsibilities
Agent	                          Purpose
ParserAgent	             ->     Reads and validates product JSON, outputs Product model
QuestionGenerationAgent	 ->     Produces categorized questions (informational, usage, safety, purchase, comparison)
FAQPageAgent	           ->     Answers questions using deterministic blocks through tools
ProductPageAgent	       ->     Builds a structured product page
ComparisonPageAgent	     ->     Creates Product B; performs ingredient-level comparison
PipelineOrchestrator	   ->     Runs the multi-agent pipeline end-to-end

Each agent follows the Single Responsibility Principle.

6. Logic Blocks
Logic blocks are deterministic functions such as:

-> build_overview_block()

-> build_ingredients_block()

-> build_benefits_block()

-> build_safety_block()

-> build_pricing_block()

-> compare_ingredients_block()

They help ensure:

-> No hallucinations

-> Predictable output

-> Reusability across agents

-> Clear separation of computation vs. structure

7. Templates
Each output JSON page has a predefined structure.
Agents fill these templates using logic blocks + tool calls.

-> FAQ Template
json
{
  "title": "",
  "sections": [
    {
      "category": "",
      "items": [
        {"question": "", "answer": ""}
      ]
    }
  ]
}
-> Product Page Template
json
{
  "title": "",
  "overview": {},
  "ingredients": {},
  "benefits": {},
  "usage": {},
  "safety": {},
  "pricing": {}
}
-> Comparison Page Template
json
{
  "title": "",
  "product_a": {},
  "product_b": {},
  "ingredient_comparison": {},
  "summary": {}
}
8. Key Engineering Principles Demonstrated
Use of frameworks over custom orchestration
(LangChain agents instead of hand-written workflows)

Tool-driven factuality
Ensures product details never deviate from allowed data

Strict JSON-structured outputs
Ideal for downstream automation

Clear modularization
Parses → Generates Questions → Answers → Builds Pages → Compares Products

Extensibility
New tools, agents, and page types can be added easily

Testability
Deterministic logic blocks allow unit testing without relying on LLM outputs

9. Conclusion
This project demonstrates an engineered, modular, and agentic approach to product content generation.
By combining:

LangChain agents

Deterministic logic blocks

Structured templates

Local LLM execution (Ollama)

the system achieves a clean, scalable architecture suitable for production-like environments.

It is simple to follow, easy to extend, and meets the expectations of the Kasparro team regarding agent frameworks, tool use, and clean architecture.

END

