# orchestrator/pipeline.py
"""
Stable LangChain 1.1.3 + LangGraph ReAct agent pipeline.
Uses deterministic tools and an Ollama LLM (llama3.1).
"""

import json
from pathlib import Path
from typing import Optional, Dict, Any
from dotenv import load_dotenv

from langchain_ollama import ChatOllama
from langgraph.prebuilt import create_react_agent

# Deterministic tools
from agents.langchain_tools import (
    read_product,
    build_overview,
    build_ingredients,
    build_usage,
    build_benefits,
    build_safety,
    build_pricing,
    compare_products,
)

# Deterministic blocks (used for fallback only)
from agents.parser_agent import ProductParserAgent
from blocks.product_blocks import (
    build_overview_block,
    build_ingredients_block,
    build_pricing_block,
    build_safety_block,
)
from blocks.usage_blocks import build_usage_block
from blocks.benefits_blocks import build_benefits_block
from blocks.comparison_blocks import (
    create_product_b_block,
    compare_ingredients_block,
    build_comparison_summary_block,
)

load_dotenv()


class PipelineOrchestrator:
    """Main orchestrator for FAQ, product page, comparison page."""

    def __init__(self, output_dir: str = "output"):
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(exist_ok=True)

        # Local LLM (Ollama)
        self.llm = ChatOllama(
            model="llama3.1:latest",
            temperature=0,
        )

        self.tools = [
            read_product,
            build_overview,
            build_ingredients,
            build_usage,
            build_benefits,
            build_safety,
            build_pricing,
            compare_products,
        ]

        # Build ReAct agent
        self.agent = create_react_agent(
            model=self.llm,
            tools=self.tools,
        )

    def _save(self, filename: str, data: dict):
        """Write JSON output."""
        path = self.output_dir / filename
        path.write_text(json.dumps(data, indent=2, ensure_ascii=False), encoding="utf-8")

    def _agent_ask(self, prompt: str) -> Optional[str]:
        """
        Sends ChatML-compliant message to LangGraph agent.

        Returns final message content or None.
        """
        try:
            result = self.agent.invoke(
                {"messages": [{"role": "user", "content": prompt}]}
            )

            # Prefer "messages"
            if isinstance(result, dict):
                msgs = result.get("messages")
                if isinstance(msgs, list) and msgs:
                    last = msgs[-1]
                    if isinstance(last, dict):
                        return last.get("content")
                    if isinstance(last, str):
                        return last

                # Some builds put output into "output"
                if isinstance(result.get("output"), str):
                    return result["output"]

            return None

        except Exception as e:
            print("[Pipeline] Agent failed:", e)
            return None

    # ----------------------------------------------------------------------
    # RUN PIPELINE
    # ----------------------------------------------------------------------
    def run(self):
        print("[Pipeline] Starting pipeline...")

        # Step 1: Parse product (deterministic)
        parser = ProductParserAgent()
        product = parser.run()
        product_json = json.dumps(product.__dict__, ensure_ascii=False)

        # Step 2: Ask agent to generate questions
        q_prompt = (
            "Use tools (read_product, build_overview, etc.) to inspect the product.\n"
            "Return ONLY valid JSON with keys:\n"
            "informational, usage, safety, purchase, comparison.\n"
            "Each key → list of 1–3 short user questions.\n"
            "NO text outside JSON."
        )

        raw_q = self._agent_ask(q_prompt)

        try:
            categorized_questions = json.loads(raw_q)
        except Exception:
            print("[Pipeline] Question agent failed — using static fallback.")
            categorized_questions = {
                "informational": ["What is the product?", "Who should use it?"],
                "usage": ["How do I use it?"],
                "safety": ["Is it safe for all skin types?"],
                "purchase": ["What is the price?"],
                "comparison": ["How does it compare to alternatives?"],
            }

        # Step 3: Ask agent to answer each question
        faq_sections = []

        for category, questions in categorized_questions.items():
            items = []

            for q in questions:
                ans_prompt = (
                    "Answer strictly using tools only.\n"
                    "Return ONLY valid JSON:\n"
                    '{"question": "...", "answer": "..."}\n'
                    f"QUESTION: {q}"
                )

                raw_ans = self._agent_ask(ans_prompt)

                try:
                    ans_obj = json.loads(raw_ans)
                except Exception:
                    print("[Pipeline] Answer agent failed — using fallback.")
                    overview = build_overview_block(product)
                    fallback = overview.get("short_description", "No information available.")
                    ans_obj = {"question": q, "answer": fallback}

                items.append(ans_obj)

            faq_sections.append({"category": category, "items": items})

        faq_json = {
            "title": f"{product.name} – FAQ",
            "sections": faq_sections,
        }
        self._save("faq.json", faq_json)
        print("[Pipeline] FAQ written.")

        # Step 4: Product Page (deterministic only)
        product_page = {
            "title": f"{product.name} – Product Page",
            "overview": build_overview_block(product),
            "ingredients": build_ingredients_block(product),
            "benefits": build_benefits_block(product),
            "usage": build_usage_block(product),
            "safety": build_safety_block(product),
            "pricing": build_pricing_block(product),
        }
        self._save("product_page.json", product_page)
        print("[Pipeline] Product page written.")

        # Step 5: Comparison Page (deterministic)
        product_b = create_product_b_block()
        ing_cmp = compare_ingredients_block(product, product_b)
        summary = build_comparison_summary_block(product, product_b, ing_cmp)

        comparison_page = {
            "title": f"{product.name} vs {product_b.name}",
            "product_a": product.__dict__,
            "product_b": product_b.__dict__,
            "ingredient_comparison": ing_cmp,
            "summary": summary,
        }
        self._save("comparison_page.json", comparison_page)
        print("[Pipeline] Comparison page written.")

        print("[Pipeline] Completed.")
