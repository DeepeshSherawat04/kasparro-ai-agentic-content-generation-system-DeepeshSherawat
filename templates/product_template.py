"""
Defines the shape of the product page. The agent fills each section
using the logic blocks so the data stays predictable and easy to read.
"""

from dataclasses import dataclass
from typing import Dict, List, Any


@dataclass
class ProductPageTemplate:
    title: str
    overview: Dict[str, str]
    ingredients: Dict[str, List[str]]
    benefits: Dict[str, Any]
    usage: Dict[str, str]
    safety: Dict[str, str]
    pricing: Dict[str, str]
