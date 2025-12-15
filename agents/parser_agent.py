# agents/parser_agent.py
"""
Product Parser Agent with validation.
Converts raw JSON into structured Product model.
"""
from dataclasses import dataclass
from typing import List
import json
from pathlib import Path


@dataclass
class Product:
    name: str
    concentration: str
    skin_type: List[str]
    key_ingredients: List[str]
    benefits: List[str]
    how_to_use: str
    side_effects: str
    price: int


class ProductParserAgent:
    """
    Loads the product_input.json and returns a Product dataclass.
    Includes validation and error handling.
    """
    def __init__(self, file_path: str = "data/product_input.json"):
        self.file_path = Path(file_path)

    def run(self) -> Product:
        """Parse and validate product data.
        
        Returns:
            Product: Validated product data model
            
        Raises:
            FileNotFoundError: If product input file doesn't exist
            ValueError: If JSON is invalid or missing required fields
        """
        # Validate file exists
        if not self.file_path.exists():
            raise FileNotFoundError(
                f"Product input file not found: {self.file_path}\n"
                f"Please ensure data/product_input.json exists."
            )
        
        # Parse JSON with error handling
        try:
            raw = json.loads(self.file_path.read_text(encoding="utf-8"))
        except json.JSONDecodeError as e:
            raise ValueError(f"Invalid JSON in product input file: {e}")
        
        # Validate required fields
        required_fields = [
            "name", "concentration", "skin_type", "key_ingredients",
            "benefits", "how_to_use", "side_effects", "price"
        ]
        
        missing_fields = [field for field in required_fields if field not in raw]
        if missing_fields:
            raise ValueError(
                f"Missing required fields in product_input.json: {', '.join(missing_fields)}"
            )
        
        # Create Product with validation
        return Product(
            name=raw["name"],
            concentration=raw["concentration"],
            skin_type=raw["skin_type"],
            key_ingredients=raw["key_ingredients"],
            benefits=raw["benefits"],
            how_to_use=raw["how_to_use"],
            side_effects=raw["side_effects"],
            price=int(raw["price"])
        )