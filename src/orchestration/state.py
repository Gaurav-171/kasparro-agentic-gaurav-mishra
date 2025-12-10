"""
System state definition for LangGraph.

This is the shared state that flows through all agents.
Each agent reads from and writes to this state.
"""

from typing import TypedDict, Optional, List
from src.models.product import ProductModel
from src.models.question import QuestionModel
from src.models.pages import FAQPageModel, ProductPageModel, ComparisonPageModel


class SystemState(TypedDict, total=False):
    """
    Shared state for the multi-agent workflow.
    
    total=False means all fields are optional.
    """
    
    # Input
    raw_data: dict
    
    # Parsed data
    product: ProductModel
    
    # Generated content
    questions: List[QuestionModel]
    faq_page: FAQPageModel
    product_page: ProductPageModel
    comparison_page: ComparisonPageModel
    
    # Metadata
    errors: List[str]
    execution_log: List[str]


def create_initial_state(raw_data: dict) -> SystemState:
    """
    Create initial system state with raw input data.
    
    Args:
        raw_data: Raw product data as dictionary
        
    Returns:
        Initial SystemState
    """
    return {
        "raw_data": raw_data,
        "errors": [],
        "execution_log": ["🚀 Workflow started"]
    }


def add_error(state: SystemState, error_message: str) -> SystemState:
    """
    Add an error to the state.
    
    Args:
        state: Current system state
        error_message: Error message to add
        
    Returns:
        Updated state
    """
    errors = state.get("errors", [])
    errors.append(error_message)
    state["errors"] = errors
    
    log = state.get("execution_log", [])
    log.append(f" Error: {error_message}")
    state["execution_log"] = log
    
    return state


def has_errors(state: SystemState) -> bool:
    """
    Check if state has any errors.
    
    Args:
        state: System state to check
        
    Returns:
        True if there are errors
    """
    errors = state.get("errors", [])
    return len(errors) > 0


def get_state_summary(state: SystemState) -> dict:
    """
    Get a summary of the current state.
    
    Args:
        state: Current system state
        
    Returns:
        Summary dictionary
    """
    return {
        "has_product": "product" in state,
        "has_questions": "questions" in state,
        "has_faq": "faq_page" in state,
        "has_product_page": "product_page" in state,
        "has_comparison": "comparison_page" in state,
        "error_count": len(state.get("errors", [])),
        "log_entries": len(state.get("execution_log", []))
    }
