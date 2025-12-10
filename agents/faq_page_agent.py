"""
Builds the FAQ page by pairing generated questions with deterministic answers.
All the heavy lifting is handled by the FAQ blocks; this agent simply shapes
everything into the final page structure.
"""

from templates.faq_template import FAQPageTemplate
from blocks.faq_blocks import build_faq_sections_block


class FAQPageAgent:
    def run(self, product, categorized_questions):
        sections = build_faq_sections_block(product, categorized_questions)

        template = FAQPageTemplate(
            title=f"{product.name} – Frequently Asked Questions",
            sections=sections,
        )

        return {
            "title": template.title,
            "sections": [
                {
                    "category": section.category_name,
                    "items": [
                        {"question": item.question, "answer": item.answer}
                        for item in section.items
                    ],
                }
                for section in template.sections
            ],
        }
