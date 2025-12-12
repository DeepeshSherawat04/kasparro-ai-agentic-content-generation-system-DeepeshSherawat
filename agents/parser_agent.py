# agents/parser_agent.py
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
    Kept intentionally simple and deterministic.
    """
    def __init__(self, file_path: str = "data/product_input.json"):
        self.file_path = Path(file_path)

    def run(self) -> Product:
        raw = json.loads(self.file_path.read_text(encoding="utf-8"))
        return Product(
            name=raw["name"],
            concentration=raw["concentration"],
            skin_type=raw["skin_type"],
            key_ingredients=raw["key_ingredients"],
            benefits=raw["benefits"],
            how_to_use=raw["how_to_use"],
            side_effects=raw["side_effects"],
            price=raw["price"],
        )
