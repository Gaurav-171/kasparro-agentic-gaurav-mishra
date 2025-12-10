"""
Main entry point for the Agentic Content Generation System.

This script:
1. Loads product data
2. Executes the multi-agent workflow
3. Generates all output pages
4. Saves results to JSON files

Usage:
    python main.py
"""

import os
import sys
from pathlib import Path
from datetime import datetime

sys.path.insert(0, str(Path(__file__).parent))

from src.orchestration.execution import execute_workflow, validate_workflow_output
from src.utils.file_writer import (
    write_json_output,
    ensure_output_directory,
    read_json_input,
    get_output_summary
)


def print_banner():
    """Print system banner."""
    banner = """
Multi-Agent Content Generation System
    """
    print(banner)


def print_system_info():
    """Print system configuration information."""
    print("\n System Configuration:")
    print("─" * 60)
    print(f"   Agents: 6")
    print(f"   Logic Blocks: 6")
    print(f"   Page Templates: 3")
    print(f"   Output Formats: JSON")
    print("─" * 60)


def load_input_data(input_path: str = "data/input/product_data.json") -> dict:
    """
    Load product data from JSON file.
    
    Args:
        input_path: Path to input JSON file
        
    Returns:
        Product data dictionary
    """
    try:
        data = read_json_input(input_path)
        print(f" Loaded input: {input_path}")
        return data
    except FileNotFoundError:
        print(f" Input file not found: {input_path}")
        sys.exit(1)
    except ValueError as e:
        print(f" Invalid JSON in input file: {e}")
        sys.exit(1)


def save_outputs(state: dict, output_dir: str = "output"):
    """
    Save all generated outputs to JSON files.
    
    Args:
        state: Final system state with all generated content
        output_dir: Output directory
    """
    ensure_output_directory(output_dir)
    
    outputs = [
        ("faq.json", state.get("faq_page")),
        ("product_page.json", state.get("product_page")),
        ("comparison_page.json", state.get("comparison_page")),
    ]
    
    print("\n Saving outputs:")
    print("─" * 60)
    
    for filename, content in outputs:
        if content:
            write_json_output(content, filename, output_dir)
        else:
            print(f"  Skipped: {filename} (not generated)")


def print_execution_summary(state: dict, start_time: datetime):
    """
    Print execution summary.
    
    Args:
        state: Final system state
        start_time: Workflow start time
    """
    end_time = datetime.now()
    duration = (end_time - start_time).total_seconds()
    
    errors = state.get("errors", [])
    log = state.get("execution_log", [])
    
    print("\n WORKFLOW COMPLETED SUCCESSFULLY!")
    print("=" * 60)
    print(f"  Duration: {duration:.2f} seconds")
    print(f" Status: {' All outputs generated' if not errors else ' Generated with errors'}")
    print(f" Log entries: {len(log)}")
    print(f" Errors: {len(errors)}")
    
    if errors:
        print("\nErrors encountered:")
        for error in errors:
            print(f"   - {error}")
    
    output_summary = get_output_summary()
    print(f"\n Output Summary:")
    print(f"   Files: {output_summary['total_files']}")
    print(f"   Total size: {output_summary['total_size_bytes']} bytes")


def print_output_preview(state: dict):
    """
    Print preview of generated outputs.
    
    Args:
        state: Final system state
    """
    print("\n Generated Content Preview:")
    print("=" * 60)
    
    if "faq_page" in state:
        faq = state["faq_page"]
        print(f"\n FAQ Page:")
        print(f"   Product: {faq.product_name}")
        print(f"   Q&A Pairs: {len(faq.faqs)}")
        if faq.faqs:
            print(f"   Sample Q: {faq.faqs[0].question[:50]}...")
    
    if "product_page" in state:
        product = state["product_page"]
        print(f"\n Product Page:")
        print(f"   Product: {product.product_name}")
        print(f"   Sections: 6 (hero, benefits, ingredients, usage, safety, pricing)")
        if "hero_section" in product.hero_section:
            print(f"   Headline: {product.hero_section.get('headline', 'N/A')}")
    
    if "comparison_page" in state:
        comp = state["comparison_page"]
        print(f"\n Comparison Page:")
        print(f"   Product A: {comp.product_a.name}")
        print(f"   Product B: {comp.product_b.name}")
        print(f"   Dimensions: {len(comp.comparison_matrix)}")


def check_environment():
    """
    Check if required environment variables and files exist.
    """
    print("\n Environment Check:")
    print("─" * 60)
    
    api_key = os.getenv("OPENAI_API_KEY")
    if api_key:
        print(" OPENAI_API_KEY configured")
    else:
        print(" OPENAI_API_KEY not set - set it in .env file")
        print("   Format: OPENAI_API_KEY=sk-xxx...")
        sys.exit(1)
    
    if Path("data/input/product_data.json").exists():
        print(" Input file found: data/input/product_data.json")
    else:
        print("  Input file not found - will try to load")
    
    if Path("output").exists():
        print(" Output directory exists")
    else:
        print(" Output directory will be created")


def main():
    """Main entry point."""
    
   
    print_banner()
    print_system_info()
    
    
    check_environment()
    
    print("\n STARTING WORKFLOW EXECUTION")
    print("=" * 60)
    start_time = datetime.now()
    
    try:
    
        raw_data = load_input_data()
        
      
        print("\n Executing multi-agent workflow...")
        state = execute_workflow(raw_data)
        
        
        validation = validate_workflow_output(state)
        
       
        print_execution_summary(state, start_time)
        
       
        save_outputs(state)
        
       
        print_output_preview(state)
        
      
        if validation["all_required_outputs_present"]:
            print("\n SUCCESS: All outputs generated successfully!")
            print(" Check the 'output' folder for generated files.")
        else:
            print(f"\n  WARNING: Some outputs missing: {validation['missing_outputs']}")
        
        return 0
        
    except Exception as e:
        print(f"\n FATAL ERROR: {str(e)}")
        import traceback
        traceback.print_exc()
        return 1


if __name__ == "__main__":
    sys.exit(main())
