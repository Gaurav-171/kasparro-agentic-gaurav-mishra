"""
Agent 5: Product Page Generator Agent

Responsibility: Generate comprehensive product description page
Input: product (ProductModel)
Output: product_page (ProductPageModel)
LLM Usage: YES (for hero section enhancement)
"""

from datetime import datetime
from src.models.product import ProductModel
from src.models.pages import ProductPageModel
from src.orchestration.state import SystemState, add_error
from src.logic_blocks import (
    generate_benefit_block,
    generate_ingredient_block,
    generate_usage_block,
    generate_safety_block,
    generate_price_block,
)
from src.utils.llm_client import get_llm
import json


def product_page_generator_agent(state: SystemState) -> SystemState:
    """
    Generate comprehensive product page.
    
    Args:
        state: System state with parsed product
        
    Returns:
        Updated state with product_page
    """
    
    print("\n" + "="*60)
    print(" AGENT 5: Product Page Generator")
    print("="*60)
    
    try:
        product = state.get("product")
        
        if not product:
            error_msg = "Product not found in state"
            print(f" {error_msg}")
            return add_error(state, error_msg)
        
        print(f" Input: {product.name}")
        
        
        hero_section = _generate_hero_section(product)
        
       
        print("🔨 Generating content sections...")
        benefits_section = generate_benefit_block(product)
        ingredients_section = generate_ingredient_block(product)
        usage_section = generate_usage_block(product)
        safety_section = generate_safety_block(product)
        price_section = generate_price_block(product)
        
       
        product_page = ProductPageModel(
            product_name=product.name,
            hero_section=hero_section,
            benefits_section=benefits_section,
            usage_section=usage_section,
            ingredients_section=ingredients_section,
            safety_section=safety_section,
            price_section=price_section,
            generated_at=datetime.utcnow()
        )
        
        state["product_page"] = product_page
        
   
        log = state.get("execution_log", [])
        log.append(f" Agent 5 (Product Page Generator): Generated complete product page")
        state["execution_log"] = log
        
        print(f" Success: Product page generated")
        print(f"   Sections: hero, benefits, ingredients, usage, safety, price")
        
        return state
        
    except Exception as e:
        error_msg = f"Product page generation failed: {str(e)}"
        print(f" {error_msg}")
        state = add_error(state, error_msg)
        return state


def _generate_hero_section(product: ProductModel) -> dict:
    """
    Generate hero section with LLM.
    """
    llm = get_llm(temperature=0.8)
    
    prompt = f"""You are a copywriter for luxury skincare. Create a compelling hero section for this product page.

Product: {product.name}
Concentration: {product.concentration}
Key Benefits: {', '.join(product.benefits)}
Skin Types: {', '.join(product.skin_types)}

Create a compelling hero section for this product page:

1. Headline (5-8 words): Aspirational, benefit-focused, memorable
2. Tagline (10-15 words): Expands on headline, includes key differentiator
3. CTA text (2-4 words): Action-oriented call to action

Respond in this exact JSON format:
{{
    "headline": "your headline here",
    "tagline": "your tagline here",
    "cta_text": "your CTA here"
}}

Make it compelling and professional. No markdown, just JSON."""
    
    try:
        response = llm.invoke(prompt)
        content = response.content
        
       
        start_idx = content.find('{')
        end_idx = content.rfind('}') + 1
        if start_idx >= 0 and end_idx > start_idx:
            json_str = content[start_idx:end_idx]
            hero_data = json.loads(json_str)
            return hero_data
    except Exception as e:
        print(f" Hero section LLM generation failed: {e}")
    

    return {
        "headline": f"Premium {product.name}",
        "tagline": f"Professional skincare solution for {', '.join(product.skin_types)} skin. Formulated with {product.concentration}.",
        "cta_text": "Shop Now"
    }
