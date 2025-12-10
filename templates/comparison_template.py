"""
Structure for the comparison page. This keeps the layout consistent,
regardless of how many fields we eventually decide to compare.
"""

from dataclasses import dataclass
from typing import Dict, Any


@dataclass
class ComparisonPageTemplate:
    title: str
    product_a: Any
    product_b: Any
    ingredients_data: Dict
    summary: Dict
