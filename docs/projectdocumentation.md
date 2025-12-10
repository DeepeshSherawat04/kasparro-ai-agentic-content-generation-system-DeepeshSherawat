Kasparro – Applied AI Agentic Content Generation System
Author: Deepesh Sherawat

1. Problem Statement

The task was to design a modular system that takes a small structured product dataset and generates three different content pages from it:

-> a FAQ page

-> a product information page

-> a comparison page

All outputs must be machine-readable JSON, and the system should rely on small, reusable logic blocks instead of long prompts or manual content.

The goal is to show how an AI-driven content pipeline can be organised in a maintainable and extensible way — similar to how such systems are built in production environments.

The assignment prioritises system design and structure, not marketing copy.

2. Scope & Assumptions

To keep the design focused and deterministic, the work follows a few constraints:

-> Only the provided product data can be used; no external research or hidden rules.

-> Product B (used in the comparison page) must be fictional but follow the same structure as Product A.

-> Each page is generated through a combination of templates and logic blocks.

-> No agent shares global state; data flows sequentially.

-> The system should remain easy to extend for new product types or additional pages.

These boundaries shape a clean, predictable pipeline.

3. Solution Overview

The solution uses a multi-agent workflow where each agent has a single clear responsibility. Data flows from one step to the next in a controlled manner.

Summary of the workflow:

-> ParserAgent
Reads the input JSON and converts it into a Product model.

-> QuestionGenerationAgent
Generates grouped user questions (informational, safety, usage, purchase, and comparison).

-> FAQPageAgent
Creates a complete FAQ page using a deterministic rule engine.

-> ProductPageAgent
Builds the product page using modular logic blocks (overview, benefits, usage, pricing, etc.).

-> ComparisonPageAgent
Creates a fictional Product B, compares both products, and generates a short summary.

-> PipelineOrchestrator
Connects all agents, runs the pipeline, and writes the output files.

This avoids a monolithic design and keeps the project easy to test and maintain.

4. System Design
4.1 High-Level Architecture Diagram
flowchart TD
    A[product_input.json] --> B[ParserAgent]
    B --> C[QuestionGenerationAgent]
    B --> D[ProductPageAgent]
    C --> E[FAQPageAgent]
    B --> F[ComparisonPageAgent]

    D --> O1[product_page.json]
    E --> O2[faq.json]
    F --> O3[comparison_page.json]


This diagram captures how information moves through the system.
Each agent receives the minimum required data and outputs a structured result.

4.2 Agent Responsibilities
Agent	                              Responsibility
ParserAgent	               ->       Convert raw JSON into a Product model
QuestionGenerationAgent	   ->       Produce categorized user questions
FAQPageAgent	             ->       Answer questions using rule-based logic
ProductPageAgent	         ->       Assemble a structured product page
ComparisonPageAgent	       ->       Create Product B and compare both products
PipelineOrchestrator	     ->       Run all agents and write JSON outputs

Keeping these roles strict helps maintain a predictable workflow.

4.3 Logic Blocks

Logic blocks are small functions that each handle one transformation.
Examples include:

-> build_overview_block()

-> build_ingredients_block()

-> build_pricing_block()

-> compare_ingredients_block()

-> answer_question_block()

This approach prevents duplication and supports future extensions.

4.4 Templates

Each output page has its own template class.
Templates define the structure of the output, while logic blocks fill in the contents.

Separating structure from logic improves readability and makes it easier to evolve the system.

5. Data & Output Structure

Each output file follows a clear JSON schema.

-> FAQ Format
{
  "title": "",
  "sections": [
    {
      "category": "",
      "items": [{"question": "", "answer": ""}]
    }
  ]
}

-> Product Page Format
{
  "title": "",
  "overview": {},
  "ingredients": {},
  "benefits": {},
  "usage": {},
  "safety": {},
  "pricing": {}
}

-> Comparison Page Format
{
  "title": "",
  "product_a": {},
  "product_b": {},
  "ingredient_comparison": {},
  "summary": {}
}

6. Conclusion

The system follows a simple but solid architecture.
Every part of the workflow has been separated into clear responsibilities.
Logic blocks keep transformations reusable, and templates ensure that output remains structured.

The result is a small yet realistic agentic content generation system that turns a minimal dataset into clean, well-structured JSON pages.
It is easy to follow, easy to modify, and a practical foundation for more advanced automation pipelines.

***END***