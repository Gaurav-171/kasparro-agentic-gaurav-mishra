"""
Product page template definition.

Structure:
- Hero section (headline, tagline)
- Benefits section (uses benefit_block)
- Ingredients section (uses ingredient_block)
- Usage section (uses usage_block)
- Safety section (uses safety_block)
- Pricing section (uses price_block)
"""

from typing import Dict, Any
from src.models.templates import TemplateModel, TemplateSection


def get_product_template() -> TemplateModel:
    """Get the product page template."""
    sections = [
        TemplateSection(
            section_name="hero",
            required_blocks=[],
            optional_blocks=[],
            llm_enhance=True,
            format_rules={
                "headline_length": "5-8 words",
                "tagline_length": "10-15 words",
                "style": "Aspirational but honest"
            }
        ),
        TemplateSection(
            section_name="benefits",
            required_blocks=["benefit_block"],
            optional_blocks=[],
            llm_enhance=False,
            format_rules={
                "max_benefits": 6,
                "description_length": "15-25 words per benefit"
            }
        ),
        TemplateSection(
            section_name="ingredients",
            required_blocks=["ingredient_block"],
            optional_blocks=[],
            llm_enhance=False,
            format_rules={
                "include_functions": True,
                "include_benefits": True
            }
        ),
        TemplateSection(
            section_name="usage",
            required_blocks=["usage_block"],
            optional_blocks=[],
            llm_enhance=False,
            format_rules={
                "include_steps": True,
                "include_tips": True,
                "include_frequency": True
            }
        ),
        TemplateSection(
            section_name="safety",
            required_blocks=["safety_block"],
            optional_blocks=[],
            llm_enhance=False,
            format_rules={
                "include_side_effects": True,
                "include_precautions": True,
                "include_who_should_avoid": True
            }
        ),
        TemplateSection(
            section_name="pricing",
            required_blocks=["price_block"],
            optional_blocks=[],
            llm_enhance=False,
            format_rules={
                "include_cost_per_use": True,
                "include_value_proposition": True
            }
        )
    ]
    
    return TemplateModel(template_type="product", sections=sections)


def get_product_page_guidelines() -> Dict[str, Any]:
    """Get guidelines for product page generation."""
    return {
        "page_structure": [
            "Hero section with compelling headline",
            "Benefits section with detailed explanations",
            "Ingredients section with functions and benefits",
            "Usage section with step-by-step instructions",
            "Safety section with transparent information",
            "Pricing section with value proposition"
        ],
        "tone": "Informative, trustworthy, professional",
        "accuracy": "100% based on provided product data",
        "content_flow": "Build trust → Educate → Enable purchase decision"
    }
