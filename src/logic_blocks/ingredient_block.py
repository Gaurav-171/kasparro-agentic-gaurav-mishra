"""
Ingredient block generator - transforms ingredients into descriptions.

Strategy: Key ingredients get spotlight with function explanations.
"""

from typing import Dict, Any, List
from src.models.product import ProductModel
from src.utils.llm_client import get_llm


# Knowledge base for common skincare ingredients
INGREDIENT_KNOWLEDGE = {
    "vitamin c": {
        "function": "Powerful antioxidant that brightens and protects skin",
        "benefits": ["Brightening", "Antioxidant protection", "Collagen synthesis"]
    },
    "hyaluronic acid": {
        "function": "Humectant that holds up to 1000x its weight in water",
        "benefits": ["Deep hydration", "Plumping effect", "Moisture retention"]
    },
    "niacinamide": {
        "function": "Vitamin B3 that strengthens skin barrier",
        "benefits": ["Oil control", "Pore minimizing", "Barrier support"]
    },
    "retinol": {
        "function": "Vitamin A derivative that promotes cell renewal",
        "benefits": ["Anti-aging", "Texture improvement", "Wrinkle reduction"]
    },
    "salicylic acid": {
        "function": "Beta hydroxy acid that exfoliates deep in pores",
        "benefits": ["Acne control", "Pore cleansing", "Texture smoothing"]
    }
}


def generate_ingredient_block(product: ProductModel, use_llm: bool = True) -> Dict[str, Any]:
    """
    Generate ingredient section content.
    
    Args:
        product: ProductModel instance
        use_llm: Whether to use LLM for unknown ingredients
        
    Returns:
        Dictionary with structured ingredient content
    """
    
    ingredient_details = []
    unknown_ingredients = []
    
    # First pass: check knowledge base
    for ingredient in product.ingredients:
        ing_lower = ingredient.lower()
        if ing_lower in INGREDIENT_KNOWLEDGE:
            info = INGREDIENT_KNOWLEDGE[ing_lower]
            ingredient_details.append({
                "ingredient": ingredient,
                "function": info["function"],
                "benefits": info["benefits"]
            })
        else:
            unknown_ingredients.append(ingredient)
    
    # Second pass: use LLM for unknown ingredients if enabled
    if unknown_ingredients and use_llm:
        llm_details = _get_ingredient_info_from_llm(unknown_ingredients, product)
        ingredient_details.extend(llm_details)
    else:
        for ingredient in unknown_ingredients:
            ingredient_details.append({
                "ingredient": ingredient,
                "function": f"Active ingredient in {product.name}",
                "benefits": ["Part of proprietary formula"]
            })
    
    return {
        "title": "Key Ingredients",
        "ingredients": ingredient_details,
        "summary": f"Formulated with {len(product.ingredients)} science-backed ingredients"
    }


def _get_ingredient_info_from_llm(ingredients: List[str], product: ProductModel) -> List[Dict[str, Any]]:
    """
    Use LLM to get information about unknown ingredients.
    """
    llm = get_llm(temperature=0.3)  # Lower temperature for factual info
    
    prompt = f"""You are a cosmetic chemist. Provide brief, factual information about these skincare ingredients.

Product context: {product.name} ({product.concentration})
Ingredients to explain: {', '.join(ingredients)}

For each ingredient, provide:
1. A one-sentence function (what it does)
2. 2-3 key benefits (brief phrases)

Format as JSON:
{{
    "ingredient_name": {{
        "function": "what it does",
        "benefits": ["benefit1", "benefit2"]
    }}
}}

Respond ONLY with JSON, no other text."""

    try:
        response = llm.invoke(prompt)
        content = response.content
        
        import json
        start_idx = content.find('{')
        end_idx = content.rfind('}') + 1
        if start_idx >= 0 and end_idx > start_idx:
            json_str = content[start_idx:end_idx]
            ingredient_dict = json.loads(json_str)
            
            details = []
            for ingredient, info in ingredient_dict.items():
                details.append({
                    "ingredient": ingredient,
                    "function": info.get("function", "Active ingredient"),
                    "benefits": info.get("benefits", [])
                })
            return details
        
    except Exception as e:
        print(f" LLM ingredient generation failed: {e}")
        return []
