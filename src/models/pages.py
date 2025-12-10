"""
Page output models - the final JSON structures for each page type.
"""

from datetime import datetime
from typing import List, Dict, Literal, Any
from pydantic import BaseModel, Field

from src.models.question import QuestionAnswerModel
from src.models.product import ProductModel


class FAQPageModel(BaseModel):
    """
    FAQ page output structure.
    """
    
    page_type: Literal["faq"] = "faq"
    product_name: str = Field(..., description="Product name for this FAQ")
    faqs: List[QuestionAnswerModel] = Field(
        ..., description="List of question-answer pairs"
    )
    generated_at: datetime = Field(
        default_factory=datetime.utcnow,
        description="Timestamp of generation"
    )
    
    class Config:
        json_schema_extra = {
            "example": {
                "page_type": "faq",
                "product_name": "GlowBoost Vitamin C Serum",
                "faqs": [
                    {
                        "question": "How do I use this serum?",
                        "answer": "Apply 2-3 drops to clean skin in the morning...",
                        "category": "usage"
                    }
                ],
                "generated_at": "2024-01-15T10:30:00"
            }
        }

class ProductPageModel(BaseModel):
    """
    Product description page output structure.
    """
    
    page_type: Literal["product"] = "product"
    product_name: str = Field(..., description="Product name")
    
    hero_section: Dict[str, Any] = Field(
        ..., description="Hero section with headline and CTA"
    )
    
    benefits_section: Dict[str, Any] = Field(
        ..., description="Benefits with descriptions"
    )
    
    usage_section: Dict[str, Any] = Field(
        ..., description="How to use instructions"
    )
    
    ingredients_section: Dict[str, Any] = Field(
        ..., description="Ingredient information"
    )
    
    safety_section: Dict[str, Any] = Field(
        ..., description="Safety and side effects info"
    )
    
    price_section: Dict[str, Any] = Field(
        ..., description="Pricing and value proposition"
    )
    
    generated_at: datetime = Field(
        default_factory=datetime.utcnow,
        description="Timestamp of generation"
    )
    
    class Config:
        json_schema_extra = {
            "example": {
                "page_type": "product",
                "product_name": "GlowBoost Vitamin C Serum",
                "hero_section": {
                    "headline": "Radiant Skin in a Drop",
                    "tagline": "Professional-grade vitamin C serum for visible brightening"
                },
                "benefits_section": {},
                "usage_section": {},
                "ingredients_section": {},
                "safety_section": {},
                "price_section": {}
            }
        }

class ComparisonPageModel(BaseModel):
    """
    Comparison page output structure.
    """
    
    page_type: Literal["comparison"] = "comparison"
    product_a: ProductModel = Field(..., description="Original product")
    product_b: ProductModel = Field(..., description="Comparison product (fictional)")
    
    comparison_matrix: List[Dict[str, Any]] = Field(
        ..., description="Structured comparison across dimensions"
    )
    
    recommendation: str = Field(
        ..., min_length=50, description="Objective recommendation for users"
    )
    
    generated_at: datetime = Field(
        default_factory=datetime.utcnow,
        description="Timestamp of generation"
    )
    
    class Config:
        json_schema_extra = {
            "example": {
                "page_type": "comparison",
                "product_a": {},
                "product_b": {},
                "comparison_matrix": [],
                "recommendation": "Both products offer excellent vitamin C delivery..."
            }
        }
