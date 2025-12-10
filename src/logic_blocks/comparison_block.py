"""
Comparison block generator - compares two products across dimensions.

Strategy: Objective comparison with structured data for easy visualization.
"""

from typing import Dict, Any, List
from src.models.product import ProductModel


def generate_comparison_block(
    product_a: ProductModel,
    product_b: ProductModel
) -> Dict[str, Any]:
    """
    Generate comparison matrix between two products.
    
    Args:
        product_a: First product
        product_b: Second product
        
    Returns:
        Dictionary with structured comparison data
    """
    
    comparison_matrix = []
    
    # Price comparison
    comparison_matrix.append(_compare_price(product_a, product_b))
    
    # Concentration comparison
    comparison_matrix.append(_compare_concentration(product_a, product_b))
    
    # Skin type suitability
    comparison_matrix.append(_compare_skin_types(product_a, product_b))
    
    # Ingredients comparison
    comparison_matrix.append(_compare_ingredients(product_a, product_b))
    
    # Benefits comparison
    comparison_matrix.append(_compare_benefits(product_a, product_b))
    
    # Side effects comparison
    comparison_matrix.append(_compare_safety(product_a, product_b))
    
    # Overall score
    scores = _calculate_scores(comparison_matrix)
    
    return {
        "matrix": comparison_matrix,
        "scores": scores,
        "summary": _generate_comparison_summary(product_a, product_b, scores)
    }


def _compare_price(product_a: ProductModel, product_b: ProductModel) -> Dict[str, Any]:
    """Compare price dimension."""
    price_diff = product_a.price - product_b.price
    price_diff_percent = (price_diff / product_b.price) * 100 if product_b.price > 0 else 0
    
    if abs(price_diff) < 100:
        winner = "tie"
        verdict = "Similarly priced"
    elif price_diff < 0:
        winner = "product_b"
        verdict = f"₹{abs(int(price_diff))} cheaper"
    else:
        winner = "product_a"
        verdict = f"₹{int(price_diff)} more affordable"
    
    return {
        "dimension": "Price",
        "product_a": f"₹{product_a.price}",
        "product_b": f"₹{product_b.price}",
        "difference": f"₹{abs(int(price_diff))} ({price_diff_percent:+.0f}%)",
        "winner": winner,
        "verdict": verdict
    }


def _compare_concentration(product_a: ProductModel, product_b: ProductModel) -> Dict[str, Any]:
    """Compare concentration dimension."""
    return {
        "dimension": "Concentration",
        "product_a": product_a.concentration,
        "product_b": product_b.concentration,
        "winner": "contextual",
        "verdict": "Compare based on your skin's needs"
    }


def _compare_skin_types(product_a: ProductModel, product_b: ProductModel) -> Dict[str, Any]:
    """Compare skin type suitability."""
    a_types = set(product_a.skin_types)
    b_types = set(product_b.skin_types)
    
    a_count = len(a_types)
    b_count = len(b_types)
    
    if a_count > b_count:
        winner = "product_a"
        verdict = f"Suitable for {a_count} skin types"
    elif b_count > a_count:
        winner = "product_b"
        verdict = f"Suitable for {b_count} skin types"
    else:
        winner = "tie"
        verdict = f"Both suitable for {a_count} skin types"
    
    return {
        "dimension": "Skin Type Coverage",
        "product_a": ", ".join(a_types),
        "product_b": ", ".join(b_types),
        "winner": winner,
        "verdict": verdict
    }


def _compare_ingredients(product_a: ProductModel, product_b: ProductModel) -> Dict[str, Any]:
    """Compare ingredients."""
    a_ings = set(ing.lower() for ing in product_a.ingredients)
    b_ings = set(ing.lower() for ing in product_b.ingredients)
    
    common = a_ings & b_ings
    a_unique = a_ings - b_ings
    b_unique = b_ings - a_ings
    
    return {
        "dimension": "Ingredients",
        "product_a": f"{len(product_a.ingredients)} ingredients",
        "product_b": f"{len(product_b.ingredients)} ingredients",
        "common_ingredients": len(common),
        "winner": "contextual",
        "verdict": f"{len(common)} shared ingredients"
    }


def _compare_benefits(product_a: ProductModel, product_b: ProductModel) -> Dict[str, Any]:
    """Compare benefits."""
    a_count = len(product_a.benefits)
    b_count = len(product_b.benefits)
    if a_count > b_count:
        winner = "product_a"
        verdict = f"{a_count} claimed benefits"
    elif b_count > a_count:
        winner = "product_b"
        verdict = f"{b_count} claimed benefits"
    else:
        winner = "tie"
        verdict = f"Both offer {a_count} benefits"

    return {
        "dimension": "Benefits",
        "product_a": f"{a_count} benefits",
        "product_b": f"{b_count} benefits",
        "winner": winner,
        "verdict": verdict
    }


def _compare_safety(product_a: ProductModel, product_b: ProductModel) -> Dict[str, Any]:
    """Compare safety profiles."""
    a_safe = "mild" in product_a.side_effects.lower()
    b_safe = "mild" in product_b.side_effects.lower()
    if a_safe and not b_safe:
        winner = "product_a"
        verdict = "Milder side effect profile"
    elif b_safe and not a_safe:
        winner = "product_b"
        verdict = "Milder side effect profile"
    else:
        winner = "tie"
        verdict = "Similar safety profiles"

    return {
        "dimension": "Safety",
        "product_a": product_a.side_effects,
        "product_b": product_b.side_effects,
        "winner": winner,
        "verdict": verdict
    }


def _calculate_scores(comparison_matrix: List[Dict[str, Any]]) -> Dict[str, Any]:
    """Calculate overall scores based on comparison."""
    a_wins = sum(1 for item in comparison_matrix if item["winner"] == "product_a")
    b_wins = sum(1 for item in comparison_matrix if item["winner"] == "product_b")
    ties = sum(1 for item in comparison_matrix if item["winner"] in ["tie", "contextual"])
    return {
        "product_a_wins": a_wins,
        "product_b_wins": b_wins,
        "ties": ties,
        "total_dimensions": len(comparison_matrix)
    }


def _generate_comparison_summary(
    product_a: ProductModel,
    product_b: ProductModel,
    scores: Dict[str, Any]
) -> str:
    """Generate a summary statement for the comparison."""
    a_wins = scores["product_a_wins"]
    b_wins = scores["product_b_wins"]
    if a_wins > b_wins:
        return f"{product_a.name} leads in {a_wins} out of {scores['total_dimensions']} dimensions"
    elif b_wins > a_wins:
        return f"{product_b.name} leads in {b_wins} out of {scores['total_dimensions']} dimensions"
    else:
        return f"Both products are competitive across {scores['total_dimensions']} key dimensions"
