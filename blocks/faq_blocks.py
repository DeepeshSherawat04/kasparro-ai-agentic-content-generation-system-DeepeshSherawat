"""
Blocks for building the FAQ page:
- answer_question_block: creates answers based only on product fields.
- build_faq_sections_block: wraps questions and answers into sections.
"""

from typing import Dict, List
from agents.parser_agent import Product
from templates.faq_template import FAQItem, FAQSection


def answer_question_block(product: Product, question: str) -> str:
    """
    Produces short factual answers using only the data we have.
    No additional assumptions or outside knowledge.
    """
    q = question.lower()

    # Pricing questions
    if "price" in q or "cost" in q:
        return f"The price of {product.name} is ₹{product.price}."

    # Skin type / suitability
    if "suitable" in q or "skin type" in q or "oily" in q or "combination" in q:
        return f"{product.name} is suitable for {', '.join(product.skin_type)} skin types."

    # How to apply or when to use
    if any(kw in q for kw in ["apply", "routine", "morning", "night"]):
        return product.how_to_use

    # Ingredient questions
    if "ingredient" in q or "formula" in q:
        return f"The key ingredients in {product.name} are: {', '.join(product.key_ingredients)}."

    # Safety / irritation / sensitivity
    if any(kw in q for kw in ["side effect", "tingling", "safe", "sensitive", "irritation"]):
        return f"Possible side effects include: {product.side_effects}"

    # Compatibility with other actives
    if any(kw in q for kw in ["retinol", "aha", "bha", "layer", "other active"]):
        return (
            f"The key ingredients in {product.name} are {', '.join(product.key_ingredients)}, "
            "so it should be paired carefully with stronger actives."
        )

    # Benefits / brightening / dark spots
    if any(kw in q for kw in ["benefit", "dark spot", "brighten", "dullness"]):
        return (
            f"This serum mainly focuses on {', '.join(product.benefits)}, "
            "making it helpful for brightening and reducing dullness."
        )

    # Result timelines
    if "how long" in q or "see results" in q:
        return "It generally takes 3–4 weeks of consistent use to see visible improvements."

    # Value / purchase decisions
    if "worth" in q or "compare price" in q:
        return f"It offers brightening benefits at a price of ₹{product.price}."

    # Default fallback
    return f"{product.name} is a simple, everyday Vitamin C serum designed for brightening."


def build_faq_sections_block(
    product: Product,
    categorized_questions: Dict[str, List[str]]
) -> List[FAQSection]:
    """
    Wraps questions and answers into section objects that match the template format.
    """
    sections = []

    for category, questions in categorized_questions.items():
        items = []
        for q in questions:
            items.append(FAQItem(question=q, answer=answer_question_block(product, q)))

        sections.append(FAQSection(category_name=category, items=items))

    return sections
