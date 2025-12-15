"""
Template Engine - Orchestrates template usage with content blocks
"""

from typing import Dict, Any, Type
from templates.faq_template import FAQTemplate
from templates.product_template import ProductPageTemplate
from templates.comparison_template import ComparisonPageTemplate


class TemplateEngine:
    """
    Template Engine that manages template selection, validation, and rendering.
    """
    
    TEMPLATES = {
        "faq": FAQTemplate,
        "product": ProductPageTemplate,
        "comparison": ComparisonPageTemplate
    }
    
    @classmethod
    def get_template(cls, template_type: str) -> Type:
        """Get template class by type."""
        if template_type not in cls.TEMPLATES:
            raise ValueError(f"Unknown template type: {template_type}")
        return cls.TEMPLATES[template_type]
    
    @classmethod
    def render(cls, template_type: str, data: dict, content_blocks: Dict[str, Any] = None) -> dict:
        """
        Render data using specified template.
        
        Args:
            template_type: Type of template (faq, product, comparison)
            data: Raw data to render
            content_blocks: Pre-computed content blocks
            
        Returns:
            dict: Formatted output according to template
        """
        template = cls.get_template(template_type)
        
        # Format according to template
        if template_type == "faq":
            output = template.format(data["product_name"], data["questions"])
        elif template_type == "product":
            output = template.format(data["product"], content_blocks)
        elif template_type == "comparison":
            output = template.format(data["product_a"], data["product_b"], data["comparison_points"])
        else:
            raise ValueError(f"Unsupported template type: {template_type}")
        
        # Validate output
        if not template.validate(output):
            raise ValueError(f"Output does not meet template requirements for {template_type}")
        
        return output
    
    @classmethod
    def get_required_blocks(cls, template_type: str) -> list:
        """Get list of content blocks required by template."""
        template = cls.get_template(template_type)
        return template.get_required_blocks()