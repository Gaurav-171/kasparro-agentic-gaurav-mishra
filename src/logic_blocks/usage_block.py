"""
Usage block generator - transforms usage instructions into step-by-step guide.

Strategy: Add context about routine timing and application tips.
"""

from typing import Dict, Any, List
from src.models.product import ProductModel


def generate_usage_block(product: ProductModel) -> Dict[str, Any]:
    """
    Generate usage instructions with context.
    
    Args:
        product: ProductModel instance
        
    Returns:
        Dictionary with structured usage content
    """
    
    # Parse the usage instruction
    usage_text = product.usage.lower()
    
    # Determine timing
    if "morning" in usage_text:
        timing = "Morning"
        routine_position = "after cleansing, before sunscreen"
    elif "evening" in usage_text or "night" in usage_text:
        timing = "Evening"
        routine_position = "after cleansing, before moisturizer"
    else:
        timing = "Daily"
        routine_position = "as needed in your skincare routine"
    
    # Extract application amount
    if "2-3 drops" in usage_text or "2–3 drops" in usage_text:
        application_amount = "2-3 drops"
    elif "drop" in usage_text:
        application_amount = "Few drops"
    elif "pea-sized" in usage_text:
        application_amount = "Pea-sized amount"
    else:
        application_amount = "As directed"
    
    # Generate step-by-step instructions
    steps = _generate_application_steps(product, application_amount, timing)
    
    # Generate tips
    tips = _generate_usage_tips(product)
    
    return {
        "title": "How to Use",
        "frequency": _determine_frequency(usage_text),
        "timing": timing,
        "routine_position": routine_position,
        "application_amount": application_amount,
        "steps": steps,
        "tips": tips,
        "instructions": product.usage
    }


def _generate_application_steps(
    product: ProductModel,
    amount: str,
    timing: str
) -> List[Dict[str, str]]:
    """
    Generate step-by-step application instructions.
    """
    steps = [
        {
            "step": 1,
            "action": "Cleanse",
            "description": "Start with a clean face and neck. Pat dry completely."
        },
        {
            "step": 2,
            "action": "Apply Serum",
            "description": f"Dispense {amount} onto fingertips and apply to face and neck."
        },
        {
            "step": 3,
            "action": "Massage",
            "description": "Gently massage in upward, circular motions for 30 seconds."
        },
        {
            "step": 4,
            "action": "Wait",
            "description": "Allow serum to absorb for 1-2 minutes before proceeding."
        }
    ]
    
    # Add timing-specific step
    if "morning" in timing.lower():
        steps.append({
            "step": 5,
            "action": "Apply Sunscreen",
            "description": "Always apply broad-spectrum SPF 30+ sunscreen as the final step."
        })
    else:
        steps.append({
            "step": 5,
            "action": "Moisturize",
            "description": "Follow with your regular moisturizer to lock in benefits."
        })
    
    return steps


def _generate_usage_tips(product: ProductModel) -> List[str]:
    """
    Generate usage tips based on product properties.
    """
    tips = []
    
    # Vitamin C specific tips
    if any("vitamin c" in ing.lower() for ing in product.ingredients):
        tips.append("Vitamin C works best on clean skin - apply to completely dry face")
        tips.append("Store in a cool place to maintain stability and potency")
    
    # Skin type specific tips
    if "Oily" in product.skin_types:
        tips.append("Use lightweight moisturizer after application")
    
    if "Sensitive" in product.skin_types or "sensitive" in product.side_effects.lower():
        tips.append("Start with use 2-3 times per week to allow skin to adapt")
        tips.append("Do patch test on inner arm first if this is your first time")
    
    # General tips
    tips.append("Consistency is key - use daily for best results")
    tips.append("Visible results typically appear within 2-4 weeks of regular use")
    
    return tips


def _determine_frequency(usage_text: str) -> str:
    """
    Determine usage frequency from usage text.
    """
    if "once" in usage_text:
        return "Once daily"
    elif "twice" in usage_text or "morning and evening" in usage_text:
        return "Twice daily"
    elif "morning" in usage_text:
        return "Once daily (morning)"
    elif "evening" in usage_text or "night" in usage_text:
        return "Once daily (evening)"
    else:
        return "Daily"
