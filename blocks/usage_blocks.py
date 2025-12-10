"""
Defines the usage section for the product page.
Kept simple: one line for how to use, one line as a usage hint.
"""

from agents.parser_agent import Product


def build_usage_block(product: Product):
    return {
        "how_to_use": product.how_to_use,
        "frequency_hint": (
            "It is meant to be used in the morning before sunscreen as part of your routine."
        )
    }
