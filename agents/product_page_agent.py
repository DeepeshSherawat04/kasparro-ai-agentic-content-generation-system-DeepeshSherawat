"""
Builds the complete product page using small logic blocks.
Each block handles a focused part of the structure, and this agent
simply brings everything together into the final output.
"""

from templates.product_template import ProductPageTemplate
from blocks.product_blocks import (
    build_overview_block,
    build_ingredients_block,
    build_safety_block,
    build_pricing_block,
)
from blocks.usage_blocks import build_usage_block
from blocks.benefits_blocks import build_benefits_block


class ProductPageAgent:
    def run(self, product):
        overview = build_overview_block(product)
        ingredients = build_ingredients_block(product)
        benefits = build_benefits_block(product)
        usage = build_usage_block(product)
        safety = build_safety_block(product)
        pricing = build_pricing_block(product)

        template = ProductPageTemplate(
            title=f"{product.name} – Product Page",
            overview=overview,
            ingredients=ingredients,
            benefits=benefits,
            usage=usage,
            safety=safety,
            pricing=pricing,
        )

        return {
            "title": template.title,
            "overview": template.overview,
            "ingredients": template.ingredients,
            "benefits": template.benefits,
            "usage": template.usage,
            "safety": template.safety,
            "pricing": template.pricing,
        }
