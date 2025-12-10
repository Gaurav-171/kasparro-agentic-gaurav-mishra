"""
Template system for declarative page generation.

Templates define the structure of pages without hardcoding content.
"""

from src.templates.template_engine import TemplateEngine
from src.templates.faq_template import get_faq_template
from src.templates.product_template import get_product_template
from src.templates.comparison_template import get_comparison_template

__all__ = [
    "TemplateEngine",
    "get_faq_template",
    "get_product_template",
    "get_comparison_template",
]
