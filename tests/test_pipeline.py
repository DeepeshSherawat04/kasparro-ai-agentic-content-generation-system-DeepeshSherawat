"""
This file contains a basic end-to-end test for the content generation pipeline.

The goal here is simple: make sure the orchestrator runs without errors and
produces the three expected JSON files (FAQ, product page, comparison page).
The test checks only structure and file presence, not wording or text quality,
so it stays stable even as copy changes.
"""

import sys
import os
import json
from pathlib import Path

# Ensure the test environment can import project modules
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from orchestrator.pipeline import PipelineOrchestrator


def test_pipeline_end_to_end(tmp_path):
    """
    Runs the entire pipeline using a temporary output directory.
    After execution, all output files should exist and follow the
    basic expected structure.
    """

    output_dir = tmp_path / "output"
    orchestrator = PipelineOrchestrator(output_dir=str(output_dir))
    orchestrator.run()

    # Verify the three expected files are created
    faq_file = output_dir / "faq.json"
    product_file = output_dir / "product_page.json"
    comparison_file = output_dir / "comparison_page.json"

    assert faq_file.exists(), "faq.json was not created"
    assert product_file.exists(), "product_page.json was not created"
    assert comparison_file.exists(), "comparison_page.json was not created"

    # Basic structure checks for each JSON file
    faq_data = json.loads(faq_file.read_text(encoding="utf-8"))
    assert "sections" in faq_data
    assert isinstance(faq_data["sections"], list)

    product_data = json.loads(product_file.read_text(encoding="utf-8"))
    assert "overview" in product_data
    assert "ingredients" in product_data
    assert "pricing" in product_data

    comparison_data = json.loads(comparison_file.read_text(encoding="utf-8"))
    assert "product_a" in comparison_data
    assert "product_b" in comparison_data
    assert "summary" in comparison_data
