"""
Small helper blocks used to build different parts of the product page.
Each block focuses on one area so the overall page stays easy to maintain.
"""

from agents.parser_agent import Product


def build_overview_block(product: Product):
    # Basic summary information about the product
    return {
        "name": product.name,
        "concentration": product.concentration,
        "suitable_for": ", ".join(product.skin_type),
        "short_tagline": (
            f"A straightforward {product.concentration} formula suitable for "
            f"{', '.join(product.skin_type)} skin types."
        )
    }


def build_ingredients_block(product: Product):
    # The product only exposes a small list of key ingredients
    return {
        "key_ingredients": product.key_ingredients
    }


def build_safety_block(product: Product):
    # Keeps safety notes simple and based solely on provided data
    return {
        "side_effects": product.side_effects,
        "sensitive_skin_note": (
            "If your skin is sensitive, be cautious and monitor how your skin responds."
        )
    }


def build_pricing_block(product: Product):
    # Price remains static, but different sellers may vary slightly
    return {
        "price_in_inr": f"₹{product.price}",
        "pricing_note": "Pricing may vary slightly depending on the seller."
    }
