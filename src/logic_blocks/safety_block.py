"""
Safety block generator - transforms side effects into balanced safety information.

Strategy: Be honest about side effects while providing reassurance and context.
"""

from typing import Dict, Any, List
from src.models.product import ProductModel


def generate_safety_block(product: ProductModel) -> Dict[str, Any]:
    """
    Generate safety and side effects section.
    
    Args:
        product: ProductModel instance
        
    Returns:
        Dictionary with structured safety content
    """
    
    side_effects_text = product.side_effects.lower()
    
    # Parse severity
    if "mild" in side_effects_text:
        severity = "Mild"
        severity_description = "Generally well-tolerated with minimal side effects"
    elif "moderate" in side_effects_text:
        severity = "Moderate"
        severity_description = "Some users may experience temporary discomfort"
    elif "severe" in side_effects_text:
        severity = "Requires Caution"
        severity_description = "Please consult a dermatologist before use"
    else:
        severity = "Minimal"
        severity_description = f"{product.name} is formulated for optimal safety"
    
    # Identify specific side effects
    known_effects = _identify_side_effects(side_effects_text)
    
    # Generate precautions
    precautions = _generate_precautions(product, side_effects_text)
    
    # Generate what to do if side effects occur
    action_steps = _generate_action_steps(severity, known_effects)
    
    # Suitable for
    suitable_for = _determine_suitable_for(product)
    not_suitable_for = _determine_not_suitable_for(product, side_effects_text)
    
    return {
        "title": "Safety & Side Effects",
        "severity": severity,
        "description": severity_description,
        "side_effects": known_effects,
        "precautions": precautions,
        "if_side_effects_occur": action_steps,
        "suitable_for": suitable_for,
        "not_suitable_for": not_suitable_for,
        "disclaimer": "This information is for educational purposes. Always patch test and consult a dermatologist if you have concerns."
    }


def _identify_side_effects(side_effects_text: str) -> List[Dict[str, str]]:
    """
    Identify and contextualize side effects.
    """
    effects = []
    
    if "tingling" in side_effects_text:
        effects.append({
            "effect": "Tingling sensation",
            "context": "Common with actives like Vitamin C, usually subsides after a few minutes"
        })
    
    if "redness" in side_effects_text:
        effects.append({
            "effect": "Mild redness",
            "context": "May occur during initial use as skin adjusts - reduce frequency if severe"
        })
    
    if "dryness" in side_effects_text:
        effects.append({
            "effect": "Temporary dryness",
            "context": "Use a good moisturizer after application to maintain skin barrier"
        })
    
    if "irritation" in side_effects_text:
        effects.append({
            "effect": "Skin irritation",
            "context": "Discontinue use and allow skin to calm before resuming"
        })
    
    if not effects:
        effects.append({
            "effect": "No known severe side effects",
            "context": "Well-tolerated by most users when used as directed"
        })
    
    return effects


def _generate_precautions(product: ProductModel, side_effects_text: str) -> List[str]:
    """
    Generate precautionary measures.
    """
    precautions = [
        "Always patch test on inner arm 24 hours before full application",
        "Avoid contact with eyes - if contact occurs, rinse immediately with water"
    ]
    
    if "sensitive" in side_effects_text:
        precautions.append("Start with 2-3 times per week if you have sensitive skin")
    
    if any("vitamin c" in ing.lower() for ing in product.ingredients):
        precautions.append("Do not mix with vitamin B3 or niacinamide in the same routine")
    
    if any("acid" in ing.lower() for ing in product.ingredients):
        precautions.append("Avoid using with other exfoliating acids on the same day")
    
    precautions.extend([
        "Keep away from heat sources - store in cool place",
        "Consult a dermatologist if you have specific skin conditions or concerns"
    ])
    
    return precautions


def _generate_action_steps(severity: str, effects: List[Dict[str, str]]) -> List[str]:
    """
    Generate steps to take if side effects occur.
    """
    steps = [
        "Stop using the product immediately",
        "Rinse face thoroughly with cool water"
    ]
    
    if severity in ["Moderate", "Requires Caution"]:
        steps.extend([
            "Apply a gentle, fragrance-free moisturizer",
            "Do not use other active ingredients until irritation clears"
        ])
    else:
        steps.append("Apply a calming moisturizer to soothe skin")
    
    steps.append("Consider reintroducing at lower frequency once skin has calmed")
    
    return steps


def _determine_suitable_for(product: ProductModel) -> List[str]:
    """
    Determine who the product is suitable for.
    """
    suitable = []
    
    for skin_type in product.skin_types:
        suitable.append(f"{skin_type} skin")
    
    suitable.append("Adults 18+ years")
    
    if "mild" in product.side_effects.lower():
        suitable.append("Sensitive skin types (with patch test)")
    
    return suitable


def _determine_not_suitable_for(product: ProductModel, side_effects_text: str) -> List[str]:
    """
    Determine who should avoid the product.
    """
    not_suitable = [
        "Pregnant or nursing women (consult doctor)",
        "Children under 18 years"
    ]
    
    if "sensitive" in side_effects_text:
        not_suitable.append("Those with severe skin sensitivity without prior testing")
    
    not_suitable.extend([
        "Those allergic to any ingredient (review full ingredient list)",
        "Active skin infections or severe acne (consult dermatologist first)"
    ])
    
    return not_suitable
