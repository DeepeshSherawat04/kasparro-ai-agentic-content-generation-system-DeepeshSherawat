"""
Builds the comparison page by assembling information about the main product
and a second fictional product. The agent keeps the flow straightforward:
prepare Product B, compare both products, and format the final JSON output.
"""

from templates.comparison_template import ComparisonPageTemplate
from blocks.comparison_blocks import (
    create_product_b_block,
    compare_ingredients_block,
    build_comparison_summary_block,
)


class ComparisonPageAgent:
    def run(self, product_a):
        # Create the secondary product used for comparison
        product_b = create_product_b_block()

        # Compare ingredients and prepare a short summary
        ingredients_data = compare_ingredients_block(product_a, product_b)
        summary = build_comparison_summary_block(product_a, product_b, ingredients_data)

        # Build a template object to keep the structure consistent
        template = ComparisonPageTemplate(
            title=f"{product_a.name} vs {product_b.name} – Comparison",
            product_a=product_a,
            product_b=product_b,
            ingredients_data=ingredients_data,
            summary=summary,
        )

        # Convert the structure into a plain JSON-friendly dict
        return {
            "title": template.title,
            "product_a": {
                "name": product_a.name,
                "price": product_a.price,
                "key_ingredients": product_a.key_ingredients,
                "benefits": product_a.benefits,
            },
            "product_b": {
                "name": product_b.name,
                "price": product_b.price,
                "key_ingredients": product_b.key_ingredients,
                "benefits": product_b.benefits,
            },
            "ingredient_comparison": template.ingredients_data,
            "summary": template.summary,
        }
