"""
Comparison Page Template Definition
"""

from typing import Dict, List, Any
from dataclasses import dataclass


@dataclass
class ComparisonPageTemplate:
    """Template structure for product comparison pages."""
    
    # Required fields
    page_type: str
    title: str
    subtitle: str
    products: Dict[str, Any]
    comparison_table: List[Dict[str, Any]]
    recommendation: Dict[str, Any]
    
    # Template rules
    MINIMUM_COMPARISON_POINTS = 4
    REQUIRED_ASPECTS = ["Price", "Concentration", "Key Ingredients", "Skin Type Compatibility"]
    
    @classmethod
    def validate(cls, data: dict) -> bool:
        """Validate data against template rules."""
        if len(data.get("comparison_table", [])) < cls.MINIMUM_COMPARISON_POINTS:
            return False
        
        aspects = [item["aspect"] for item in data.get("comparison_table", [])]
        if not all(aspect in aspects for aspect in cls.REQUIRED_ASPECTS):
            return False
        
        return True
    
    @classmethod
    def format(cls, product_a: dict, product_b: dict, comparison_points: List[dict]) -> dict:
        """Format data according to template structure."""
        return {
            "page_type": "product_comparison",
            "title": f"{product_a['name']} vs {product_b['name']}",
            "subtitle": "Comprehensive comparison to help you choose",
            "products": {
                "product_a": {
                    "name": product_a["name"],
                    "price": f"₹{product_a['price']}"
                },
                "product_b": {
                    "name": product_b["name"],
                    "price": f"₹{product_b['price']}"
                }
            },
            "comparison_table": comparison_points,
            "recommendation": {
                "best_for_budget": product_a["name"] if product_a["price"] < product_b["price"] else product_b["name"]
            }
        }
    
    @classmethod
    def get_required_blocks(cls) -> List[str]:
        """Return list of content blocks needed."""
        return [
            "comparison_generator",
            "winner_selector",
            "recommendation_generator"
        ]