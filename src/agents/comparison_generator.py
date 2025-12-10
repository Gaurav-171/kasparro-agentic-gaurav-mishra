"""
Agent 6: Comparison Generator Agent

Responsibility: Generate fictional Product B and create comparison page
Input: product (ProductModel)
Output: comparison_page (ComparisonPageModel)
LLM Usage: YES (generate Product B + recommendation)
"""

from datetime import datetime
from pydantic import BaseModel
from src.models.product import ProductModel
from src.models.pages import ComparisonPageModel
from src.orchestration.state import SystemState, add_error
from src.logic_blocks import generate_comparison_block
from src.utils.llm_client import get_structured_llm, get_llm
import json


class ProductData(BaseModel):
    """Container for product data from LLM."""
    name: str
    concentration: str
    skin_types: list
    ingredients: list
    benefits: list
    usage: str
    side_effects: str
    price: float


def comparison_generator_agent(state: SystemState) -> SystemState:
    """
    Generate comparison page with fictional competitor product.
    
    Args:
        state: System state with parsed product
        
    Returns:
        Updated state with comparison_page
    """
    
    print("\n" + "="*60)
    print("  AGENT 6: Comparison Generator")
    print("="*60)
    
    try:
        product_a = state.get("product")
        
        if not product_a:
            error_msg = "Product not found in state"
            print(f" {error_msg}")
            return add_error(state, error_msg)
        
        print(f" Input: {product_a.name}")
        
       
        print(" Generating fictional competitor product...")
        product_b = _generate_fictional_product(product_a)
        
    
        print(" Generating comparison matrix...")
        comparison_data = generate_comparison_block(product_a, product_b)
        
     
        print(" Generating recommendation...")
        recommendation = _generate_recommendation(product_a, product_b, comparison_data)
        
        # Create comparison page
        comparison_page = ComparisonPageModel(
            product_a=product_a,
            product_b=product_b,
            comparison_matrix=comparison_data.get("matrix", []),
            recommendation=recommendation,
            generated_at=datetime.utcnow()
        )
        
        state["comparison_page"] = comparison_page
        
       
        log = state.get("execution_log", [])
        log.append(f" Agent 6 (Comparison Generator): Generated comparison with {product_b.name}")
        state["execution_log"] = log
        
        print(f" Success: Comparison page generated")
        print(f"   Product A: {product_a.name}")
        print(f"   Product B: {product_b.name}")
        print(f"   Dimensions compared: {len(comparison_data.get('matrix', []))}")
        
        return state
        
    except Exception as e:
        error_msg = f"Comparison generation failed: {str(e)}"
        print(f" {error_msg}")
        state = add_error(state, error_msg)
        return state


def _generate_fictional_product(product_a: ProductModel) -> ProductModel:
    """
    Generate a realistic fictional competitor product.
    """
    llm = get_llm(temperature=0.7)
    
    prompt = f"""You are a market analyst creating a realistic competitor product for comparison purposes.

Original Product:
- Name: {product_a.name}
- Concentration: {product_a.concentration}
- Skin Types: {', '.join(product_a.skin_types)}
- Ingredients: {', '.join(product_a.ingredients)}
- Benefits: {', '.join(product_a.benefits)}
- Usage: {product_a.usage}
- Side Effects: {product_a.side_effects}
- Price: ₹{product_a.price}

Create a REALISTIC fictional competitor product with these requirements:

1. Name: Different brand name (professional skincare style)
   Example formats: "ClarityGlow Serum", "VitaLift Concentrate", "RadianceBoost Formula"

2. Price: Within ±30% of ₹{product_a.price}

3. Concentration: Similar category but different percentage

4. Ingredients: 50-70% overlap

5. Benefits: 50-80% overlap

6. Skin Types: Can be slightly different

7. Side Effects: Realistic and believable

8. Usage: Similar routine but can vary

Make the competitor product REALISTIC - it should feel like a real product that exists in the market, not perfect or dramatically better.

Generate the complete product data now. Respond ONLY with this JSON format, no other text:
{{
    "name": "Product Name",
    "concentration": "percentage",
    "skin_types": ["type1", "type2"],
    "ingredients": ["ing1", "ing2"],
    "benefits": ["benefit1", "benefit2"],
    "usage": "usage instructions",
    "side_effects": "possible side effects",
    "price": number
}}"""
    
    try:
        response = llm.invoke(prompt)
        content = response.content
        
        # Parse JSON
        start_idx = content.find('{')
        end_idx = content.rfind('}') + 1
        if start_idx >= 0 and end_idx > start_idx:
            json_str = content[start_idx:end_idx]
            product_data = json.loads(json_str)
            
            return ProductModel(
                name=product_data.get("name", "Competitor Serum"),
                concentration=product_data.get("concentration", product_a.concentration),
                skin_types=product_data.get("skin_types", product_a.skin_types),
                ingredients=product_data.get("ingredients", product_a.ingredients),
                benefits=product_data.get("benefits", product_a.benefits),
                usage=product_data.get("usage", product_a.usage),
                side_effects=product_data.get("side_effects", product_a.side_effects),
                price=float(product_data.get("price", product_a.price))
            )
    except Exception as e:
        print(f" LLM product generation failed: {e}, using fallback")
        return _generate_fallback_product_b(product_a)


def _generate_fallback_product_b(product_a: ProductModel) -> ProductModel:
    """
    Generate a fallback fictional product if LLM fails.
    """
    
  
    new_price = product_a.price * 1.15
    
  
    new_ingredients = product_a.ingredients.copy()
    if len(new_ingredients) > 0:
        new_ingredients[0] = new_ingredients[0] + " (Enhanced)"
    
    return ProductModel(
        name=f"Premium {product_a.name.split()[0]} Competitor",
        concentration=f"{int(float(product_a.concentration.split('%')[0]) * 0.95)}% Active",
        skin_types=product_a.skin_types,
        ingredients=new_ingredients,
        benefits=product_a.benefits,
        usage=product_a.usage,
        side_effects=product_a.side_effects,
        price=new_price
    )


def _generate_recommendation(
    product_a: ProductModel,
    product_b: ProductModel,
    comparison_data: dict
) -> str:
    """
    Generate an objective recommendation comparing both products.
    """
    llm = get_llm(temperature=0.3)
    
    # Format comparison matrix for readability
    matrix_text = ""
    for item in comparison_data.get("matrix", []):
        matrix_text += f"- {item.get('dimension')}: {item.get('verdict')}\n"
    
    prompt = f"""You are a skincare expert providing objective product recommendations.

Product A: {product_a.name}
- Price: ₹{product_a.price}
- Concentration: {product_a.concentration}
- Skin Types: {', '.join(product_a.skin_types)}
- Key Benefits: {', '.join(product_a.benefits)}

Product B: {product_b.name}
- Price: ₹{product_b.price}
- Concentration: {product_b.concentration}
- Skin Types: {', '.join(product_b.skin_types)}
- Key Benefits: {', '.join(product_b.benefits)}

Comparison Results:
{matrix_text}

Scores:
- {product_a.name}: {comparison_data.get('scores', {}).get('product_a_wins', 0)} dimensions won
- {product_b.name}: {comparison_data.get('scores', {}).get('product_b_wins', 0)} dimensions won

Write an objective recommendation (3-5 sentences, 100-200 words):

1. Summarize key differences
2. Recommend who should choose Product A (specific use cases)
3. Recommend who should choose Product B (specific use cases)
4. Be balanced and fair - both are good products

Keep it professional, objective, and helpful. No marketing fluff."""
    
    try:
        response = llm.invoke(prompt)
        return response.content
    except Exception as e:
        print(f" Recommendation generation failed: {e}")
        # Fallback recommendation
        return f"Both {product_a.name} and {product_b.name} are excellent skincare products. Choose based on your specific skin type and budget preferences. {product_a.name} offers proven benefits, while {product_b.name} provides an alternative formulation. Patch test before full use."
