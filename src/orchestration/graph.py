"""
LangGraph workflow definition.

Defines the DAG (Directed Acyclic Graph) for agent orchestration.
"""

from typing import Literal
from langgraph.graph import StateGraph, END
from src.orchestration.state import SystemState


def create_workflow_graph() -> StateGraph:
    """
    Create the main workflow graph.
    
    Workflow:
    1. Parse data (Agent 1)
    2. Generate questions (Agent 2)
    3. Generate FAQ (Agent 4)
    4. Generate Product page (Agent 5)
    5. Generate Comparison (Agent 6)
    
    Note: Sequential execution avoids LangGraph concurrent update errors
    """
    
    workflow = StateGraph(SystemState)
    
    # Import agents
    from src.agents import (
        data_parser_agent,
        question_generator_agent,
        faq_generator_agent,
        product_page_generator_agent,
        comparison_generator_agent
    )
    
    # Add nodes
    workflow.add_node("parse_data", data_parser_agent)
    workflow.add_node("generate_questions", question_generator_agent)
    workflow.add_node("generate_faq", faq_generator_agent)
    workflow.add_node("generate_product_page", product_page_generator_agent)
    workflow.add_node("generate_comparison", comparison_generator_agent)
    
    # Sequential execution to avoid concurrent state updates
    workflow.add_edge("parse_data", "generate_questions")
    
    # Check for errors before continuing
    workflow.add_conditional_edges(
        "generate_questions",
        should_continue_after_questions,
        {
            "continue": "generate_faq",
            "error": END
        }
    )
    
    # Sequential generation of pages (prevents concurrent updates)
    workflow.add_edge("generate_faq", "generate_product_page")
    workflow.add_edge("generate_product_page", "generate_comparison")
    workflow.add_edge("generate_comparison", END)
    
    # Set entry point
    workflow.set_entry_point("parse_data")
    
    return workflow


def should_continue_after_questions(
    state: SystemState
) -> Literal["continue", "error"]:
    """
    Determine whether to continue after question generation.
    
    Args:
        state: Current system state
        
    Returns:
        "continue" if successful, "error" if there are errors
    """
    errors = state.get("errors", [])
    
    if len(errors) > 0:
        print(f" Errors detected: {errors}")
        return "error"
    
    if "questions" not in state:
        error_msg = "No questions were generated"
        state["errors"] = state.get("errors", []) + [error_msg]
        return "error"
    
    return "continue"


def create_parallel_workflow_graph() -> StateGraph:
    """
    Create an alternative workflow with more parallelization.
    
    Note: This is a future extension - keeping sequential for now
    to ensure dependencies are met.
    """
    return create_workflow_graph()


def visualize_workflow(workflow: StateGraph, output_path: str = "workflow_graph.png"):
    """
    Visualize the workflow graph (requires graphviz).
    
    Args:
        workflow: StateGraph instance
        output_path: Path to save visualization
    """
    try:
        import matplotlib.pyplot as plt
        print(f" Workflow visualization would be saved to {output_path}")
        print("Note: Install graphviz for full visualization support")
    except ImportError:
        print(" Visualization requires: pip install graphviz")


def get_workflow_info(workflow: StateGraph) -> dict:
    """
    Get information about the workflow.
    
    Args:
        workflow: StateGraph instance
        
    Returns:
        Dictionary with workflow info
    """
    return {
        "entry_point": "parse_data",
        "nodes": [
            "parse_data",
            "generate_questions",
            "generate_faq",
            "generate_product_page",
            "generate_comparison"
        ],
        "flow": "Sequential parsing → Parallel generation",
        "error_handling": "Stops at question generation if errors occur"
    }


def test_workflow_state_flow():
    """Test that the workflow state flows correctly."""
    from src.orchestration.state import create_initial_state, add_error
    
    # Create initial state
    state = create_initial_state({"test": "data"})
    
    # Verify initial state
    assert "raw_data" in state
    assert "errors" in state
    assert state["errors"] == []
    
    # Add an error
    state = add_error(state, "Test error")
    assert len(state["errors"]) == 1
    
    print(" State flow test passed")
    return True
