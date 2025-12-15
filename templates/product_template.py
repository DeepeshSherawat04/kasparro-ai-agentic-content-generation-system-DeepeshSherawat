"""
Product Page Template Definition
"""

from typing import Dict, List, Any
from dataclasses import dataclass


@dataclass
class ProductPageTemplate:
    """Template structure for product description pages."""
    
    # Required fields
    page_type: str
    product_name: str
    headline: str
    tagline: str
    hero_section: Dict[str, Any]
    key_features: List[str]
    ingredients: Dict[str, Any]
    how_to_use: Dict[str, Any]
    safety_information: Dict[str, Any]
    who_is_it_for: Dict[str, Any]
    
    # Template rules
    MINIMUM_FEATURES = 3
    REQUIRED_SECTIONS = ["hero_section", "key_features", "ingredients", "how_to_use", "safety_information"]
    
    @classmethod
    def validate(cls, data: dict) -> bool:
        """Validate data against template rules."""
        if len(data.get("key_features", [])) < cls.MINIMUM_FEATURES:
            return False
        
        if not all(section in data for section in cls.REQUIRED_SECTIONS):
            return False
        
        return True
    
    @classmethod
    def format(cls, product_data: dict, content_blocks: Dict[str, Any]) -> dict:
        """Format data according to template structure."""
        return {
            "page_type": "product_description",
            "product_name": product_data["name"],
            "headline": content_blocks["headline"],
            "tagline": content_blocks["tagline"],
            "hero_section": content_blocks["hero_section"],
            "key_features": content_blocks["key_features"],
            "ingredients": content_blocks["ingredients"],
            "how_to_use": content_blocks["usage_instructions"],
            "safety_information": content_blocks["safety_info"],
            "who_is_it_for": {
                "skin_types": product_data["skin_type"],
                "concerns": product_data["benefits"]
            }
        }
    
    @classmethod
    def get_required_blocks(cls) -> List[str]:
        """Return list of content blocks needed."""
        return [
            "headline_generator",
            "tagline_generator",
            "features_extractor",
            "ingredients_formatter",
            "usage_formatter",
            "safety_formatter"
        ]