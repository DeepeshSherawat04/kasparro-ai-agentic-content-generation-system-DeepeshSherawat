"""
Helper functions that support the comparison page.
These blocks focus on small, clear tasks: creating Product B,
comparing ingredients, and summarizing the differences.
"""

from dataclasses import dataclass
from typing import List, Dict
from agents.parser_agent import Product as ProductA


@dataclass
class ProductB:
    name: str
    key_ingredients: List[str]
    benefits: List[str]
    price: int


def create_product_b_block() -> ProductB:
    """
    Defines the fictional comparison product used throughout the system.
    """
    return ProductB(
        name="RadiancePlus Brightening Serum",
        key_ingredients=["Vitamin C", "Niacinamide"],
        benefits=["Brightening", "Evens skin tone"],
        price=749,
    )


def compare_ingredients_block(product_a: ProductA, product_b: ProductB) -> Dict[str, List[str]]:
    """
    Finds common and unique ingredients between the two products.
    """
    a_set = set(product_a.key_ingredients)
    b_set = set(product_b.key_ingredients)

    return {
        "ingredient_overlap": sorted(list(a_set & b_set)),
        "unique_to_a": sorted(list(a_set - b_set)),
        "unique_to_b": sorted(list(b_set - a_set)),
    }


def build_comparison_summary_block(
    product_a: ProductA,
    product_b: ProductB,
    ingredients_data: Dict[str, List[str]],
) -> Dict[str, str]:
    """
    Creates short, readable summary sentences for the comparison section.
    """
    price_diff = product_b.price - product_a.price
    if price_diff > 0:
        price_sentence = f"{product_b.name} is ₹{price_diff} more expensive than {product_a.name}."
    elif price_diff < 0:
        price_sentence = f"{product_b.name} is ₹{abs(price_diff)} cheaper than {product_a.name}."
    else:
        price_sentence = f"Both products are priced the same at ₹{product_a.price}."

    overlap = ingredients_data.get("ingredient_overlap", [])
    if overlap:
        ingredient_sentence = f"Both contain: {', '.join(overlap)}."
    else:
        ingredient_sentence = "They do not share any listed key ingredients."

    return {
        "price_difference": price_sentence,
        "ingredient_summary": ingredient_sentence,
    }
