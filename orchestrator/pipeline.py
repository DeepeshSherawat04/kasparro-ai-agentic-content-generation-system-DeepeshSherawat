"""
This runs the entire flow of the system. The pipeline acts as a coordinator:
it loads the product, generates questions, builds each content page,
and writes everything out as JSON.
"""

import json
from pathlib import Path
from typing import Dict, Any

from agents.parser_agent import ProductParserAgent
from agents.question_agent import QuestionGenerationAgent
from agents.faq_page_agent import FAQPageAgent
from agents.product_page_agent import ProductPageAgent
from agents.comparison_page_agent import ComparisonPageAgent


class PipelineOrchestrator:
    def __init__(self, output_dir: str = "output"):
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(exist_ok=True)

        # Initialize agents used in the pipeline
        self.parser_agent = ProductParserAgent()
        self.question_agent = QuestionGenerationAgent()
        self.faq_agent = FAQPageAgent()
        self.product_agent = ProductPageAgent()
        self.comparison_agent = ComparisonPageAgent()

    def _write_json(self, filename: str, data: Dict[str, Any]):
        """Save a JSON file to the output folder."""
        path = self.output_dir / filename
        path.write_text(json.dumps(data, indent=2, ensure_ascii=False), encoding="utf-8")

    def _log(self, message: str):
        """Lightweight logger to show progress in the console."""
        print(f"[Pipeline] {message}")

    def run(self):
        self._log("Starting pipeline...")

        # Load product data
        self._log("Parsing product_input.json...")
        product = self.parser_agent.run()
        self._log(f"Loaded product: {product.name}")

        # Create categorized questions
        self._log("Generating categorized questions...")
        categorized_questions = self.question_agent.run(product)
        self._log(f"Generated {sum(len(v) for v in categorized_questions.values())} questions")

        # Build FAQ page
        self._log("Building FAQ page JSON...")
        faq_json = self.faq_agent.run(product, categorized_questions)
        self._log("FAQ page generated")

        # Build product page
        self._log("Building Product page JSON...")
        product_json = self.product_agent.run(product)
        self._log("Product page generated")

        # Build comparison page
        self._log("Building Comparison page JSON...")
        comparison_json = self.comparison_agent.run(product)
        self._log("Comparison page generated")

        # Save files
        self._log("Writing output JSON files...")
        self._write_json("faq.json", faq_json)
        self._write_json("product_page.json", product_json)
        self._write_json("comparison_page.json", comparison_json)

        self._log("Pipeline completed successfully.")
