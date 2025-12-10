"""
Product data model - the core data structure for all agents.
"""

from typing import List
from pydantic import BaseModel, Field, field_validator


class ProductModel(BaseModel):
    """
    Validated product data model.
    
    This is the single source of truth for product information.
    All agents consume this model.
    """
    
    name: str = Field(..., description="Product name")
    concentration: str = Field(..., description="Active ingredient concentration")
    skin_types: List[str] = Field(..., description="Suitable skin types")
    ingredients: List[str] = Field(..., description="Key ingredients list")
    benefits: List[str] = Field(..., description="Product benefits")
    usage: str = Field(..., description="How to use instructions")
    side_effects: str = Field(..., description="Potential side effects")
    price: float = Field(..., gt=0, description="Price in INR")
    
    @field_validator('skin_types', 'ingredients', 'benefits')
    @classmethod
    def validate_non_empty_list(cls, v: List[str]) -> List[str]:
        if not v:
            raise ValueError("List cannot be empty")
        return v
    
    @field_validator('name', 'concentration', 'usage', 'side_effects')
    @classmethod
    def validate_non_empty_string(cls, v: str) -> str:
        if not v or not v.strip():
            raise ValueError("String cannot be empty")
        return v.strip()
    
    class Config:
        json_schema_extra = {
            "example": {
                "name": "GlowBoost Vitamin C Serum",
                "concentration": "10% Vitamin C",
                "skin_types": ["Oily", "Combination"],
                "ingredients": ["Vitamin C", "Hyaluronic Acid"],
                "benefits": ["Brightening", "Fades dark spots"],
                "usage": "Apply 2–3 drops in the morning before sunscreen",
                "side_effects": "Mild tingling for sensitive skin",
                "price": 699
            }
        }
