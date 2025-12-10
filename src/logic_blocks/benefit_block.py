"""
Benefit block generator - transforms benefits into marketing copy.

Strategy: Each benefit gets elaborated with context and value proposition.
"""

from typing import Dict, Any
from src.models.product import ProductModel
from src.utils.llm_client import get_llm


def generate_benefit_block(product: ProductModel, use_llm: bool = True) -> Dict[str, Any]:
    """
    Generate benefit section content from product benefits.
    
    Args:
        product: ProductModel instance
        use_llm: Whether to use LLM for enhancement
        
    Returns:
        Dictionary with benefit block content
        
    Example:
        >>> from src.models.product import ProductModel
        >>> block = generate_benefit_block(product)
        "Key Benefits"
    """
    
    if use_llm:
        return _generate_benefit_block_with_llm(product)
    else:
        return _generate_benefit_block_rule_based(product)

def _generate_benefit_block_rule_based(product: ProductModel) -> Dict[str, Any]:
    """
    Rule-based benefit generation (no LLM).
    
    Simple template-based expansion of benefits.
    """
    benefit_details = []
    
    for benefit in product.benefits:
        benefit_details.append({
            "benefit": benefit,
            "description": f"Experience the power of {benefit.lower()} with our advanced formula.",
            "relevance": "High"
        })
    
    return {
        "title": "Key Benefits",
        "benefits": benefit_details,
        "summary": f"This product delivers {len(product.benefits)} proven benefits for {', '.join(product.skin_types)} skin."
    }


def _generate_benefit_block_with_llm(product: ProductModel) -> Dict[str, Any]:
    """
    LLM-enhanced benefit generation.
    
    Uses GPT-4o-mini to create compelling benefit descriptions.
    """
    llm = get_llm(temperature=0.7)
    
    prompt = f"""You are a skincare copywriter. Given these product benefits, create compelling descriptions.

Product: {product.name}
Benefits: {', '.join(product.benefits)}
Key Ingredients: {', '.join(product.ingredients)}

For each benefit, write ONE sentence (15-25 words) that:
1. Explains HOW the product delivers this benefit
2. Mentions relevant ingredients if applicable
3. Uses aspirational but honest language

Format your response as a JSON object with this structure:
{{
    "benefit_1": "description here",
    "benefit_2": "description here"
}}

Respond ONLY with the JSON object, no other text."""

    try:
        response = llm.invoke(prompt)
        content = response.content
        
        # Parse JSON from response
        import json
        start_idx = content.find('{')
        end_idx = content.rfind('}') + 1
        if start_idx >= 0 and end_idx > start_idx:
            json_str = content[start_idx:end_idx]
            benefit_dict = json.loads(json_str)
            
            benefit_details = []
            for benefit, description in benefit_dict.items():
                benefit_details.append({
                    "benefit": benefit,
                    "description": description,
                    "relevance": "High"
                })
            
            return {
                "title": "Key Benefits",
                "benefits": benefit_details,
                "summary": f"This product delivers {len(benefit_details)} proven benefits for {', '.join(product.skin_types)} skin."
            }
        
    except Exception as e:
        print(f" LLM benefit generation failed: {e}")
        return _generate_benefit_block_rule_based(product)
