"""
Execution utilities for the workflow.

Workflow Execution:
- Sequential execution: parse_data → questions → faq → product → comparison
- This avoids LangGraph concurrent update errors on immutable state fields
- Each agent modifies different fields, no conflicts
- Total execution time: ~30-60 seconds depending on LLM latency
"""

from typing import Dict, Any
from src.orchestration.graph import create_workflow_graph
from src.orchestration.state import SystemState, create_initial_state, get_state_summary


def execute_workflow(raw_data: Dict[str, Any]) -> SystemState:
    """
    Execute the complete workflow sequentially.
    
    Args:
        raw_data: Raw product data dictionary
        
    Returns:
        Final system state with all generated content
    """
    # Create initial state
    state = create_initial_state(raw_data)
    
    # Create and execute workflow
    workflow = create_workflow_graph()
    compiled_workflow = workflow.compile()
    
    # Run workflow
    final_state = compiled_workflow.invoke(state)
    
    return final_state


def execute_workflow_step_by_step(raw_data: Dict[str, Any]) -> Dict[str, SystemState]:
    """
    Execute workflow with detailed state at each step.
    
    Args:
        raw_data: Raw product data
        
    Returns:
        Dictionary with state after each agent
    """
    from src.agents import (
        data_parser_agent,
        question_generator_agent,
        faq_generator_agent,
        product_page_generator_agent,
        comparison_generator_agent
    )
    
    states = {}
    
    # Step 1: Parse data
    state = create_initial_state(raw_data)
    state = data_parser_agent(state)
    states["after_parser"] = state.copy()
    
    # Step 2: Generate questions
    state = question_generator_agent(state)
    states["after_questions"] = state.copy()
    
    # Step 3: Generate FAQ
    state = faq_generator_agent(state)
    states["after_faq"] = state.copy()
    
    # Step 4: Generate product page
    state = product_page_generator_agent(state)
    states["after_product"] = state.copy()
    
    # Step 5: Generate comparison
    state = comparison_generator_agent(state)
    states["after_comparison"] = state.copy()
    
    return states


def validate_workflow_output(state: SystemState) -> Dict[str, Any]:
    """
    Validate that all required outputs were generated.
    
    Args:
        state: Final system state
        
    Returns:
        Validation report
    """
    required_outputs = [
        "product",
        "questions",
        "faq_page",
        "product_page",
        "comparison_page"
    ]
    
    validation = {
        "all_required_outputs_present": True,
        "missing_outputs": [],
        "errors": state.get("errors", []),
        "state_summary": get_state_summary(state)
    }
    
    for output in required_outputs:
        if output not in state:
            validation["all_required_outputs_present"] = False
            validation["missing_outputs"].append(output)
    
    return validation
