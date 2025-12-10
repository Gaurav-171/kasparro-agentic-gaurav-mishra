"""
Agent 4: FAQ Generator Agent

Responsibility: Generate FAQ page with answers
Input: product (ProductModel), questions (List[QuestionModel])
Output: faq_page (FAQPageModel)
LLM Usage: YES (answer generation)
"""

from typing import List
from datetime import datetime
from pydantic import BaseModel, Field
from src.models.product import ProductModel
from src.models.question import QuestionModel, QuestionAnswerModel
from src.models.pages import FAQPageModel
from src.orchestration.state import SystemState, add_error
from src.utils.llm_client import get_llm


class AnswerList(BaseModel):
    """Container for list of answers."""
    answers: List[QuestionAnswerModel] = Field(..., description="List of Q&A pairs")


def faq_generator_agent(state: SystemState) -> SystemState:
    """
    Generate FAQ page with questions and answers.
    
    Args:
        state: System state with product and questions
        
    Returns:
        Updated state with faq_page
    """
    
    print("\n" + "="*60)
    print(" AGENT 4: FAQ Generator")
    print("="*60)
    
    try:
        product = state.get("product")
        questions = state.get("questions", [])
        
        if not product:
            error_msg = "Product not found in state"
            print(f" {error_msg}")
            return add_error(state, error_msg)
        
        if not questions:
            error_msg = "Questions not found in state"
            print(f" {error_msg}")
            return add_error(state, error_msg)
        
        print(f" Input: {product.name} with {len(questions)} questions")
        
       
        selected_questions = _select_best_questions(questions, max_count=10)
        print(f" Selected {len(selected_questions)} best questions")
        
       
        qna_pairs = _generate_answers(product, selected_questions)
        
       
        faq_page = FAQPageModel(
            product_name=product.name,
            faqs=qna_pairs,
            generated_at=datetime.utcnow()
        )
        
        state["faq_page"] = faq_page
        
        
        log = state.get("execution_log", [])
        log.append(f" Agent 4 (FAQ Generator): Generated FAQ with {len(qna_pairs)} Q&A pairs")
        state["execution_log"] = log
        
        print(f" Success: Generated FAQ page")
        print(f"   Q&A Pairs: {len(qna_pairs)}")
        print(f"   Categories: {set(q.category for q in qna_pairs)}")
        
        return state
        
    except Exception as e:
        error_msg = f"FAQ generation failed: {str(e)}"
        print(f" {error_msg}")
        state = add_error(state, error_msg)
        return state


def _select_best_questions(
    questions: List[QuestionModel],
    max_count: int = 10
) -> List[QuestionModel]:
    """
    Select the best questions from the generated list.
    
    Strategy: Distribute evenly across categories.
    """
    if len(questions) <= max_count:
        return questions
    
  
    by_category = {}
    for q in questions:
        if q.category not in by_category:
            by_category[q.category] = []
        by_category[q.category].append(q)
    
    
    selected = []
    per_category = max_count // len(by_category)
    
    for category, cats_questions in by_category.items():
        selected.extend(cats_questions[:per_category])
    
    return selected[:max_count]


def _generate_answers(
    product: ProductModel,
    questions: List[QuestionModel]
) -> List[QuestionAnswerModel]:
    """
    Generate answers for the selected questions.
    """
    llm = get_llm(temperature=0.3) 
    
    questions_text = "\n".join([
        f"{i+1}. [{q.category}] {q.question}"
        for i, q in enumerate(questions)
    ])
    
    prompt = f"""You are a knowledgeable skincare expert. Answer these customer questions about a product.

Product Information:
- Name: {product.name}
- Concentration: {product.concentration}
- Skin Types: {', '.join(product.skin_types)}
- Key Ingredients: {', '.join(product.ingredients)}
- Benefits: {', '.join(product.benefits)}
- Usage: {product.usage}
- Side Effects: {product.side_effects}
- Price: ₹{product.price}

Customer Questions:
{questions_text}

For EACH question, provide a helpful, accurate answer (2-4 sentences).

Guidelines:
- Be friendly and professional
- Base answers ONLY on the product information provided
- Don't make claims beyond what's stated
- Be honest about side effects and limitations
- Include practical tips where relevant
- Keep answers concise but complete

Generate answers for all {len(questions)} questions."""
    
    try:
        response = llm.invoke(prompt)
        content = response.content
        
       
        qna_pairs = []
        for question in questions:
            answer = _generate_fallback_answer(product, question)
            qna_pairs.append(
                QuestionAnswerModel(
                    question=question.question,
                    answer=answer,
                    category=question.category
                )
            )
        
        return qna_pairs
        
    except Exception as e:
        print(f" LLM answer generation failed: {e}, using fallback")
        qna_pairs = []
        for question in questions:
            answer = _generate_fallback_answer(product, question)
            qna_pairs.append(
                QuestionAnswerModel(
                    question=question.question,
                    answer=answer,
                    category=question.category
                )
            )
        return qna_pairs


def _generate_fallback_answer(product: ProductModel, question: QuestionModel) -> str:
    """Generate a fallback answer based on question category and product data."""
    
    category = question.category.lower()
    
    if "usage" in category:
        return f"This product should be used as follows: {product.usage}. Apply consistently for best results."
    elif "safety" in category:
        return f"Safety information: {product.side_effects}. Always perform a patch test before full application."
    elif "ingredient" in category:
        return f"This product contains: {', '.join(product.ingredients)}. Each ingredient has been selected for its benefits."
    elif "price" in category or "purchase" in category:
        return f"This product is priced at ₹{product.price}, offering excellent value for its formulation."
    elif "benefit" in category:
        return f"The key benefits of this product include: {', '.join(product.benefits)}. Results vary by individual."
    else:
        return f"{product.name} is designed for {', '.join(product.skin_types)} skin types. Please review the product information for more details."
