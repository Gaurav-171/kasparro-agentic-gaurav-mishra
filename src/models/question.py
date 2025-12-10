"""
Question and Q&A models for content generation.
"""

from typing import Literal
from pydantic import BaseModel, Field


class QuestionModel(BaseModel):
    """
    A categorized user question about the product.
    """
    
    category: Literal[
        "informational",
        "safety",
        "usage",
        "purchase",
        "comparison",
        "ingredients"
    ] = Field(..., description="Question category")
    
    question: str = Field(..., min_length=10, description="The question text")
    
    class Config:
        json_schema_extra = {
            "example": {
                "category": "safety",
                "question": "Is this product safe for sensitive skin?"
            }
        }

class QuestionAnswerModel(BaseModel):
    """
    A question with its generated answer (for FAQ pages).
    """
    
    question: str = Field(..., description="The question text")
    answer: str = Field(..., min_length=20, description="The answer text")
    category: str = Field(..., description="Question category")
    
    class Config:
        json_schema_extra = {
            "example": {
                "question": "Is this product safe for sensitive skin?",
                "answer": "While this product is generally well-tolerated, sensitive skin individuals may experience mild tingling. Start with lower frequency and monitor your skin's response.",
                "category": "safety"
            }
        }
