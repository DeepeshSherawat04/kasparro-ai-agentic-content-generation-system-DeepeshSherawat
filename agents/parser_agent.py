"""
Reads product_input.json and turns it into a Product instance.
The goal is simply to load the data cleanly and keep the model predictable.
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
    def __init__(self, file_path="data/product_input.json"):
        self.file_path = Path(file_path)

    def run(self) -> Product:
        # Load the raw JSON and map it to the Product dataclass
        data = json.loads(self.file_path.read_text(encoding="utf-8"))
        return Product(
            name=data["name"],
            concentration=data["concentration"],
            skin_type=data["skin_type"],
            key_ingredients=data["key_ingredients"],
            benefits=data["benefits"],
            how_to_use=data["how_to_use"],
            side_effects=data["side_effects"],
            price=data["price"],
        )
