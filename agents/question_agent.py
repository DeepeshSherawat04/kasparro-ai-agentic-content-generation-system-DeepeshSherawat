"""
Generates groups of questions that a user might ask about the product.
Each block returns questions for a specific area, and this agent just
organizes them into categories.
"""

from agents.parser_agent import Product
from blocks.questions_blocks import (
    generate_informational_questions_block,
    generate_safety_questions_block,
    generate_usage_questions_block,
    generate_purchase_questions_block,
    generate_comparison_questions_block,
)


class QuestionGenerationAgent:
    def run(self, product: Product):
        # Collect questions from the individual blocks and arrange them by category
        return {
            "informational": generate_informational_questions_block(product),
            "safety": generate_safety_questions_block(product),
            "usage": generate_usage_questions_block(product),
            "purchase": generate_purchase_questions_block(product),
            "comparison": generate_comparison_questions_block(product),
        }
