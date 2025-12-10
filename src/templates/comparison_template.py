"""
Comparison page template definition.

Structure:
- Overview section (both products)
- Comparison matrix (uses comparison_block)
- Detailed comparison sections
- Recommendation section
"""

from typing import Dict, Any, List
from src.models.templates import TemplateModel, TemplateSection


def get_comparison_template() -> TemplateModel:
    """Get the comparison page template."""
    sections = [
        TemplateSection(
            section_name="overview",
            required_blocks=[],
            optional_blocks=[],
            llm_enhance=False,
            format_rules={
                "include_product_a_summary": True,
                "include_product_b_summary": True
            }
        ),
        TemplateSection(
            section_name="matrix",
            required_blocks=["comparison_block"],
            optional_blocks=[],
            llm_enhance=False,
            format_rules={
                "dimensions": [
                    "Price",
                    "Concentration",
                    "Skin Type Coverage",
                    "Ingredients",
                    "Benefits",
                    "Safety"
                ]
            }
        ),
        TemplateSection(
            section_name="detailed_comparison",
            required_blocks=[],
            optional_blocks=[],
            llm_enhance=True,
            format_rules={
                "sections": [
                    "Price Analysis",
                    "Formula Comparison",
                    "Efficacy Comparison",
                    "Safety Comparison"
                ]
            }
        ),
        TemplateSection(
            section_name="recommendation",
            required_blocks=[],
            optional_blocks=[],
            llm_enhance=True,
            format_rules={
                "length": "3-5 sentences",
                "structure": [
                    "Who should choose Product A",
                    "Who should choose Product B",
                    "Overall recommendation"
                ]
            }
        )
    ]
    
    return TemplateModel(template_type="comparison", sections=sections)


def get_comparison_dimensions() -> List[Dict[str, str]]:
    """Get the comparison dimensions."""
    return [
        {
            "dimension": "Price",
            "description": "Cost and value for money"
        },
        {
            "dimension": "Concentration",
            "description": "Active ingredient concentration"
        },
        {
            "dimension": "Skin Type Coverage",
            "description": "Suitable for different skin types"
        },
        {
            "dimension": "Ingredients",
            "description": "Quality and overlap of ingredients"
        },
        {
            "dimension": "Benefits",
            "description": "Number and type of claimed benefits"
        },
        {
            "dimension": "Safety",
            "description": "Side effects and safety profile"
        }
    ]


def get_comparison_guidelines() -> Dict[str, Any]:
    """Get guidelines for comparison page generation."""
    return {
        "objectivity": "Fair and balanced comparison without bias",
        "structure": "Matrix-based with detailed analysis",
        "tone": "Professional, informative, helpful",
        "recommendation": "Based on comparison data, not marketing",
        "disclosure": "Clear about fictional product"
    }


def get_fictional_product_guidelines() -> Dict[str, Any]:
    """Get guidelines for creating fictional Product B."""
    return {
        "realism": "Should feel like a real market competitor",
        "pricing": "Within ±30% of original product price",
        "ingredients": "50-70% overlap with original product",
        "benefits": "50-80% overlap with original product",
        "side_effects": "Realistic and believable",
        "differentiation": "Clear differences that make comparison meaningful"
    }
