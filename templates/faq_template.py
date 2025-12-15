"""
FAQ Page Template Definition
Structured template with fields, rules, and formatting.
"""

from typing import Dict, List, Any
from dataclasses import dataclass


@dataclass
class FAQTemplate:
    """Template structure for FAQ pages."""
    
    # Required fields
    title: str
    product: str
    total_questions: int
    sections: List[Dict[str, Any]]
    
    # Template rules
    MINIMUM_QUESTIONS = 15
    REQUIRED_CATEGORIES = ["informational", "usage", "safety", "purchase", "comparison"]
    
    @classmethod
    def validate(cls, data: dict) -> bool:
        """Validate data against template rules."""
        if data.get("total_questions", 0) < cls.MINIMUM_QUESTIONS:
            return False
        
        categories = [s["category"] for s in data.get("sections", [])]
        if not all(cat in categories for cat in cls.REQUIRED_CATEGORIES):
            return False
        
        return True
    
    @classmethod
    def format(cls, product_name: str, questions: List[dict]) -> dict:
        """Format data according to template structure."""
        # Group by category
        categories = {}
        for q in questions:
            cat = q["category"]
            if cat not in categories:
                categories[cat] = []
            categories[cat].append(q)
        
        # Build sections
        sections = []
        for category, items in categories.items():
            sections.append({
                "category": category,
                "items": items
            })
        
        return {
            "title": f"Frequently Asked Questions - {product_name}",
            "product": product_name,
            "total_questions": len(questions),
            "sections": sections
        }
    
    @classmethod
    def get_required_blocks(cls) -> List[str]:
        """Return list of content blocks needed for this template."""
        return [
            "question_generator",
            "answer_generator",
            "category_organizer"
        ]