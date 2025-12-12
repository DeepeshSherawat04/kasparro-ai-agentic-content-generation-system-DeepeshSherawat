# tests/test_pipeline.py
import sys, os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

import json
from pathlib import Path
from unittest.mock import patch, MagicMock

from orchestrator.pipeline import PipelineOrchestrator


def test_pipeline_end_to_end(tmp_path):
    """
    End-to-end test that mocks LangChain agent construction and runtime.
    This prevents any external LLM calls while asserting the output JSON files exist
    and have the expected basic structure.
    """

    output_dir = tmp_path / "output"
    orchestrator = PipelineOrchestrator(output_dir=str(output_dir))

    # Predefined question JSON (agent response for question generation)
    fake_questions = json.dumps({
        "informational": ["What is the product?"],
        "usage": ["How do I use it?"],
        "safety": ["Is it safe?"],
        "purchase": ["What is the price?"],
        "comparison": ["How does it compare?"]
    })

    # Predefined answer JSON used for each question
    fake_answer = json.dumps({"question": "dummy", "answer": "test answer"})

    # Build a fake agent object with a .run method that returns the above strings
    fake_agent = MagicMock()
    # .run will be called: first for questions, then repeatedly for answers.
    fake_agent.run.side_effect = [fake_questions, fake_answer, fake_answer, fake_answer, fake_answer, fake_answer]

    # Patch create_agent to return our fake_agent
    with patch("langchain.agents.create_agent", return_value=fake_agent):
        orchestrator.run()

    # Validate files
    faq_file = output_dir / "faq.json"
    product_file = output_dir / "product_page.json"
    comparison_file = output_dir / "comparison_page.json"

    assert faq_file.exists(), "faq.json was not created"
    assert product_file.exists(), "product_page.json was not created"
    assert comparison_file.exists(), "comparison_page.json was not created"

    # Basic structural checks
    faq_data = json.loads(faq_file.read_text(encoding="utf-8"))
    assert "sections" in faq_data and isinstance(faq_data["sections"], list)

    product_data = json.loads(product_file.read_text(encoding="utf-8"))
    assert "overview" in product_data and "pricing" in product_data

    comparison_data = json.loads(comparison_file.read_text(encoding="utf-8"))
    assert "product_a" in comparison_data and "product_b" in comparison_data
