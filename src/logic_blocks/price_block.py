"""
Price block generator - transforms price into value proposition.

Strategy: Add context about value, cost per use, and positioning.
"""

from typing import Dict, Any
from src.models.product import ProductModel


def generate_price_block(product: ProductModel, bottle_size_ml: int = 30) -> Dict[str, Any]:
    """
    Generate pricing section with value context.
    
    Args:
        product: ProductModel instance
        bottle_size_ml: Bottle size in milliliters (default: 30ml)
        
    Returns:
        Dictionary with structured pricing content
    """
    
    price = product.price
    
    # Calculate cost per ml
    cost_per_ml = price / bottle_size_ml
    
    # Calculate estimated cost per use (assuming 2-3 drops = ~0.1ml)
    drops_per_use = 2.5  # Average of 2-3 drops
    ml_per_use = drops_per_use * 0.05  # ~0.05ml per drop
    cost_per_use = ml_per_use * cost_per_ml
    
    # Calculate estimated days of use
    uses_per_day = 1  # Default to once daily
    if "twice" in product.usage.lower() or "morning and evening" in product.usage.lower():
        uses_per_day = 2
    
    total_uses = bottle_size_ml / ml_per_use
    days_supply = total_uses / uses_per_day
    
    # Determine price positioning
    if price < 500:
        positioning = "Budget-Friendly"
        positioning_desc = "Affordable luxury for everyday skincare"
    elif price < 1000:
        positioning = "Mid-Range"
        positioning_desc = "Premium quality at accessible pricing"
    elif price < 2000:
        positioning = "Premium"
        positioning_desc = "High-end formulation with proven ingredients"
    else:
        positioning = "Luxury"
        positioning_desc = "Professional-grade investment in skin health"
    
    # Generate value highlights
    value_highlights = _generate_value_highlights(product, cost_per_use, days_supply)
    
    return {
        "title": "Pricing & Value",
        "price": f"₹{price}",
        "price_numeric": price,
        "bottle_size_ml": bottle_size_ml,
        "positioning": positioning,
        "positioning_description": positioning_desc,
        "cost_per_ml": f"₹{cost_per_ml:.2f}",
        "cost_per_use": f"₹{cost_per_use:.2f}",
        "estimated_days_supply": int(days_supply),
        "value_highlights": value_highlights,
        "investment_statement": _generate_investment_statement(product, price, days_supply)
    }


def _generate_value_highlights(
    product: ProductModel,
    cost_per_use: float,
    days_supply: float
) -> list:
    """
    Generate value proposition highlights.
    """
    highlights = []
    
    # Cost per use highlight
    if cost_per_use < 5:
        highlights.append(f"Less than ₹{int(cost_per_use) + 1} per application")
    else:
        highlights.append(f"Approximately ₹{cost_per_use:.0f} per use")
    
    # Supply duration
    if days_supply >= 60:
        highlights.append(f"Over {int(days_supply/30)} months supply with daily use")
    else:
        highlights.append(f"Approximately {int(days_supply)} days of use")
    
    # Concentration value
    if product.concentration:
        highlights.append(f"Effective {product.concentration} formulation")
    
    # Ingredient value
    premium_ingredients = ["Vitamin C", "Hyaluronic Acid", "Retinol", "Niacinamide"]
    if any(ing in product.ingredients for ing in premium_ingredients):
        highlights.append("Contains premium, research-backed ingredients")
    
    # Multi-benefit value
    if len(product.benefits) >= 2:
        highlights.append(f"Delivers {len(product.benefits)} benefits in one product")
    
    return highlights


def _generate_investment_statement(
    product: ProductModel,
    price: float,
    days_supply: float
) -> str:
    """
    Generate an investment/value statement.
    """
    daily_cost = price / days_supply
    
    if daily_cost < 15:
        return f"An investment of just ₹{daily_cost:.0f} per day for healthier, more radiant skin"
    elif daily_cost < 30:
        return f"Premium skincare at ₹{daily_cost:.0f} daily - less than your morning coffee"
    else:
        return f"A professional-grade treatment for ₹{daily_cost:.0f} per day"
