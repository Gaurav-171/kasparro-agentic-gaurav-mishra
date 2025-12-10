"""
Template definition models for declarative page generation.
"""

from typing import List, Dict, Any
from pydantic import BaseModel, Field


class TemplateSection(BaseModel):
    """
    A single section within a template.
    """
    
    section_name: str = Field(..., description="Name of the section")
    required_blocks: List[str] = Field(
        default=[], description="Required logic blocks for this section"
    )
    optional_blocks: List[str] = Field(
        default=[], description="Optional logic blocks for this section"
    )
    llm_enhance: bool = Field(
        default=False, description="Whether to enhance with LLM"
    )
    format_rules: Dict[str, Any] = Field(
        default={}, description="Format rules for output"
    )


class TemplateModel(BaseModel):
    """
    A complete page template definition.
    """
    
    template_type: str = Field(..., description="Type of template (faq, product, comparison)")
    sections: List[TemplateSection] = Field(..., description="List of sections in this template")
    
    class Config:
        json_schema_extra = {
            "example": {
                "template_type": "product",
                "sections": [
                    {
                        "section_name": "hero",
                        "required_blocks": [],
                        "optional_blocks": [],
                        "llm_enhance": True,
                        "format_rules": {}
                    }
                ]
            }
        }
