"""
It generates lists of questions that users commonly ask.
Grouped into different themes to make the FAQ more organized.
"""

from typing import List
from agents.parser_agent import Product


def generate_informational_questions_block(product: Product) -> List[str]:
    return [
        f"What is {product.name} and what does it do?",
        f"Who can use {product.name}?",
        "What skin concerns does this serum target?",
        "Does this serum help with dullness?",
        "How long does it take to see results from using this serum?",
    ]


def generate_safety_questions_block(product: Product) -> List[str]:
    return [
        "Is this serum safe for sensitive skin?",
        "Are there any side effects I should know about?",
        "Can I use this serum every day?",
        "What should I do if I experience irritation?",
        "Can I use this serum with other active ingredients?",
    ]


def generate_usage_questions_block(product: Product) -> List[str]:
    return [
        "How should I apply this serum in my daily routine?",
        "Should I use this serum in the morning or at night?",
        "Can I layer this with other active ingredients like retinol or AHA/BHA?",
        "How much of the serum should I use per application?",
        "Do I need to use sunscreen when using this serum?",
    ]


def generate_purchase_questions_block(product: Product) -> List[str]:
    return [
        f"What is the price of {product.name}?",
        "How long will one bottle last with regular use?",
        "Is this serum worth buying compared to other Vitamin C serums?",
        "Where can I purchase this serum?",
        "Are there any discounts or offers available for this serum?",
    ]


def generate_comparison_questions_block(product: Product) -> List[str]:
    return [
        f"How does {product.name} compare to other Vitamin C serums?",
        "Is this better for oily skin than other serums?",
        "Should I choose this serum or a niacinamide serum for dark spots?",
        "How does the price of this serum compare to similar products?",
        "What are the unique benefits of this serum compared to others?",
    ]
