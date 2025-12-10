"""
Creates the benefits section for the product page. Kept simple because
we only depend on the product's own field values.
"""

from agents.parser_agent import Product


def build_benefits_block(product: Product):
    return {
        "benefits_list": product.benefits,
        "summary": f"This serum focuses on {', '.join(product.benefits)}."
    }
