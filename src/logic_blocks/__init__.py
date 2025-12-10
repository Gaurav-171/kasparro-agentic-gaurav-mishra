"""
Reusable content logic blocks.

These are pure functions that transform product data into content blocks.
They can be used by multiple agents and are easily testable.
"""

from src.logic_blocks.benefit_block import generate_benefit_block
from src.logic_blocks.ingredient_block import generate_ingredient_block
from src.logic_blocks.usage_block import generate_usage_block
from src.logic_blocks.safety_block import generate_safety_block
from src.logic_blocks.price_block import generate_price_block
from src.logic_blocks.comparison_block import generate_comparison_block

__all__ = [
    "generate_benefit_block",
    "generate_ingredient_block",
    "generate_usage_block",
    "generate_safety_block",
    "generate_price_block",
    "generate_comparison_block",
]
