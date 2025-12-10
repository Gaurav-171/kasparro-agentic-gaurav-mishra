"""
Agent 2: Question Generator Agent

Responsibility: Generate 15+ categorized user questions
Input: product (ProductModel)
Output: questions (List[QuestionModel])
LLM Usage: YES (structured output)
"""

from typing import List
from pydantic import BaseModel, Field
from src.models.product import ProductModel
from src.models.question import QuestionModel
from src.orchestration.state import SystemState, add_error
from src.utils.llm_client import get_structured_llm


class QuestionList(BaseModel):
    """Container for list of questions."""
    questions: List[QuestionModel] = Field(..., description="List of generated questions")


def question_generator_agent(state: SystemState) -> SystemState:
    """
    Generate categorized questions about the product.
    
    Args:
        state: System state with parsed product
        
    Returns:
        Updated state with questions
    """
    
    print("\n" + "="*60)
    print(" AGENT 2: Question Generator")
    print("="*60)
    
    try:
        product = state.get("product")
        
        if not product:
            error_msg = "Product not found in state"
            print(f" {error_msg}")
            return add_error(state, error_msg)
        
        print(f" Input: {product.name}")
        
        # Get structured LLM
        llm = get_structured_llm(QuestionList, temperature=0.7)
        
        # Create prompt
        prompt = f"""You are a customer research assistant. Generate realistic questions that customers would ask about this skincare product.

Product Information:
- Name: {product.name}
- Concentration: {product.concentration}
- Skin Types: {', '.join(product.skin_types)}
- Key Ingredients: {', '.join(product.ingredients)}
- Benefits: {', '.join(product.benefits)}
- Usage: {product.usage}
- Side Effects: {product.side_effects}
- Price: ₹{product.price}

Generate EXACTLY 18 questions that real customers would ask about this product.

Categories (distribute questions evenly):
1. informational - About the product itself
2. safety - About side effects and precautions
3. usage - How to use the product
4. purchase - About buying, pricing, value
5. comparison - Comparing to other products or ingredients
6. ingredients - About specific ingredients and their effects

Requirements:
- Each question must be natural and conversational
- Questions should be specific to THIS product
- Mix of beginner and informed customer perspectives
- Questions should be 10-25 words each
- Cover diverse aspects of the product

Generate questions now."""
        
        # Call LLM
        result = llm.invoke(prompt)
        
        if isinstance(result, QuestionList):
            questions = result.questions
        else:
            questions = result.questions if hasattr(result, 'questions') else []
        
        state["questions"] = questions
        
        # Add to execution log
        log = state.get("execution_log", [])
        log.append(f" Agent 2 (Question Generator): Generated {len(questions)} questions")
        state["execution_log"] = log
        
        print(f" Success: Generated {len(questions)} questions")
        print(f"   Categories: {set(q.category for q in questions)}")
        
        return state
        
    except Exception as e:
        error_msg = f"Question generation failed: {str(e)}"
        print(f" {error_msg}")
        state = add_error(state, error_msg)
        return state
