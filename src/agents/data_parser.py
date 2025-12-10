"""
Agent 1: Data Parser Agent

Responsibility: Parse and validate raw input data into ProductModel
Input: raw_data (dict)
Output: product (ProductModel)
LLM Usage: NO (pure validation)
"""

from pydantic import ValidationError
from src.models.product import ProductModel
from src.orchestration.state import SystemState, add_error


def data_parser_agent(state: SystemState) -> SystemState:
    """
    Parse and validate raw input data.
    
    Args:
        state: System state with raw_data
        
    Returns:
        Updated state with parsed product
    """
    
    print("\n" + "="*60)
    print(" AGENT 1: Data Parser")
    print("="*60)
    
    try:
        raw_data = state.get("raw_data", {})
        
        print(f" Input: Raw data with {len(raw_data)} fields")
        
     
        product = ProductModel(**raw_data)
        
        state["product"] = product
        
        
        log = state.get("execution_log", [])
        log.append(f" Agent 1 (Data Parser): Product validated - {product.name}")
        state["execution_log"] = log
        
        print(f" Success: Product validated")
        print(f"   Name: {product.name}")
        print(f"   Price: ₹{product.price}")
        print(f"   Skin Types: {', '.join(product.skin_types)}")
        
        return state
        
    except ValidationError as e:
        error_msg = f"Product validation failed: {str(e)}"
        print(f" {error_msg}")
        state = add_error(state, error_msg)
        return state
    
    except Exception as e:
        error_msg = f"Unexpected error in data parser: {str(e)}"
        print(f" {error_msg}")
        state = add_error(state, error_msg)
        return state
