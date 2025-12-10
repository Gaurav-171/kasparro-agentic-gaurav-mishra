"""
Template engine - renders pages from templates and data.

This is the core abstraction that separates structure from content.
"""

from typing import Dict, Any, Callable
from src.models.templates import TemplateModel, TemplateSection
from src.models.product import ProductModel


class TemplateEngine:
    """
    Renders pages from template definitions and data.
    """
    
    def __init__(self):
        self.registered_blocks: Dict[str, Callable] = {}
    
    def register_block(self, block_name: str, block_func: Callable) -> None:
        """Register a logic block."""
        self.registered_blocks[block_name] = block_func
    
    def render_section(
        self,
        section: TemplateSection,
        product: ProductModel,
        extra_context: Dict[str, Any] = None
    ) -> Dict[str, Any]:
        """
        Render a single section by combining required and optional blocks.
        """
        result = {
            "section_name": section.section_name,
            "blocks": []
        }
        
        # Execute required blocks
        for block_name in section.required_blocks:
            if block_name in self.registered_blocks:
                block_func = self.registered_blocks[block_name]
                block_result = block_func(product)
                result["blocks"].append({
                    "name": block_name,
                    "content": block_result,
                    "required": True
                })
        
        # Execute optional blocks if available
        for block_name in section.optional_blocks:
            if block_name in self.registered_blocks:
                try:
                    block_func = self.registered_blocks[block_name]
                    block_result = block_func(product)
                    result["blocks"].append({
                        "name": block_name,
                        "content": block_result,
                        "required": False
                    })
                except Exception as e:
                    print(f" Optional block {block_name} failed: {e}")
        
        return result
    
    def render_template(
        self,
        template: TemplateModel,
        product: ProductModel,
        extra_context: Dict[str, Any] = None
    ) -> Dict[str, Any]:
        """
        Render a complete template by rendering all sections.
        """
        result = {
            "template_type": template.template_type,
            "sections": []
        }
        
        for section in template.sections:
            rendered_section = self.render_section(section, product, extra_context)
            result["sections"].append(rendered_section)
        
        return result


def create_default_engine() -> TemplateEngine:
    """Create and configure the default template engine."""
    from src.logic_blocks import (
        generate_benefit_block,
        generate_ingredient_block,
        generate_usage_block,
        generate_safety_block,
        generate_price_block,
        generate_comparison_block
    )
    
    engine = TemplateEngine()
    
    # Register all logic blocks
    engine.register_block("benefit_block", generate_benefit_block)
    engine.register_block("ingredient_block", generate_ingredient_block)
    engine.register_block("usage_block", generate_usage_block)
    engine.register_block("safety_block", generate_safety_block)
    engine.register_block("price_block", generate_price_block)
    engine.register_block("comparison_block", generate_comparison_block)
    
    return engine
