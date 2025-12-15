# tests/test_pipeline.py
"""
Fixed end-to-end test for the pipeline.
"""
import sys
import os
import json
import pytest
from pathlib import Path
from unittest.mock import patch, MagicMock

# Add parent directory to path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from orchestrator.pipeline import PipelineOrchestrator


def test_pipeline_runs_without_errors():
    """Test that pipeline runs end-to-end using fallback (no LLM needed)."""
    
    # Ensure data files exist
    assert Path("data/product_input.json").exists(), "product_input.json missing"
    assert Path("data/product_b.json").exists(), "product_b.json missing"
    
    # Run the pipeline (will use fallback if LLM unavailable)
    orchestrator = PipelineOrchestrator()
    result = orchestrator.run()
    
    # Validate state has required keys
    assert "product_json" in result
    assert "questions" in result
    assert "faq_json" in result
    assert "product_page_json" in result
    assert "comparison_page_json" in result
    
    # Validate question count
    assert len(result["questions"]) >= 15, f"Expected ≥15 questions, got {len(result['questions'])}"
    
    # Validate FAQ structure
    faq = result["faq_json"]
    assert "title" in faq
    assert "sections" in faq
    assert isinstance(faq["sections"], list)
    assert faq["total_questions"] >= 15
    
    # Validate product page structure
    product_page = result["product_page_json"]
    assert "page_type" in product_page
    assert product_page["page_type"] == "product_description"
    assert "product_name" in product_page
    assert "key_features" in product_page
    
    # Validate comparison page structure
    comparison = result["comparison_page_json"]
    assert "page_type" in comparison
    assert comparison["page_type"] == "product_comparison"
    assert "products" in comparison
    assert "product_a" in comparison["products"]
    assert "product_b" in comparison["products"]


def test_output_files_created():
    """Test that all output JSON files are created."""
    
    # Run pipeline
    orchestrator = PipelineOrchestrator()
    orchestrator.run()
    
    # Check output files exist
    output_dir = Path("output")
    assert output_dir.exists(), "output directory not created"
    
    faq_file = output_dir / "faq.json"
    product_file = output_dir / "product_page.json"
    comparison_file = output_dir / "comparison_page.json"
    
    assert faq_file.exists(), "faq.json not created"
    assert product_file.exists(), "product_page.json not created"
    assert comparison_file.exists(), "comparison_page.json not created"
    
    # Validate JSON is valid
    faq_data = json.loads(faq_file.read_text(encoding="utf-8"))
    assert "sections" in faq_data
    
    product_data = json.loads(product_file.read_text(encoding="utf-8"))
    assert "product_name" in product_data
    
    comparison_data = json.loads(comparison_file.read_text(encoding="utf-8"))
    assert "products" in comparison_data


def test_parser_agent():
    """Test that parser agent correctly loads product data."""
    from agents.parser_agent import ProductParserAgent
    
    parser = ProductParserAgent()
    product = parser.run()
    
    assert product.name == "GlowBoost Vitamin C Serum"
    assert product.price == 699
    assert "Vitamin C" in product.key_ingredients
    assert "Oily" in product.skin_type or "Combination" in product.skin_type


def test_content_logic_blocks():
    """Test that content logic blocks work correctly."""
    from agents.content_logic import ContentLogicBlocks
    
    logic = ContentLogicBlocks()
    
    test_product = {
        "name": "Test Serum",
        "concentration": "10% Vitamin C",
        "benefits": ["Brightening", "Anti-aging"],
        "key_ingredients": ["Vitamin C", "Hyaluronic Acid"],
        "skin_type": ["Oily", "Combination"],
        "price": 699,
        "how_to_use": "Apply in the morning",
        "side_effects": "Mild tingling"
    }
    
    # Test headline generation
    headline = logic.generate_product_headline(test_product)
    assert "Test Serum" in headline
    
    # Test tagline generation
    tagline = logic.generate_product_tagline(test_product)
    assert len(tagline) > 0
    
    # Test features generation
    features = logic.generate_key_features(test_product)
    assert isinstance(features, list)
    assert len(features) > 0
    
    # Test price section
    price_section = logic.generate_price_section(test_product)
    assert "price" in price_section
    assert "₹699" in price_section["price"]


if __name__ == "__main__":
    # Run tests
    pytest.main([__file__, "-v"])