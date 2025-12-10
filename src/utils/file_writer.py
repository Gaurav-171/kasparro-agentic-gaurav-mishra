"""
File writing utilities for JSON output.

Handles:
- Creating output directories
- Writing JSON with proper formatting
- Error handling and logging
"""

import json
import os
from pathlib import Path
from typing import Any, Dict
from datetime import datetime
from pydantic import BaseModel


def ensure_output_directory(output_dir: str = "output") -> Path:
    """
    Ensure output directory exists, create if it doesn't.
    
    Args:
        output_dir: Directory path to ensure exists
        
    Returns:
        Path object for the output directory
        
    Raises:
        OSError: If directory cannot be created
    """
    output_path = Path(output_dir)
    
    try:
        output_path.mkdir(parents=True, exist_ok=True)
        return output_path
    except OSError as e:
        raise OSError(f"Failed to create output directory: {e}")

def write_json_output(
    data: Any,
    filename: str,
    output_dir: str = "output",
    indent: int = 2
) -> Path:
    """
    Write data to a JSON file with proper formatting.
    
    Args:
        data: Data to write (dict, list, or Pydantic model)
        filename: Output filename
        output_dir: Output directory path
        indent: JSON indentation level
        
    Returns:
        Path to the written file
        
    Raises:
        OSError: If file cannot be written
        TypeError: If data cannot be serialized
        
    Example:
        >>> from src.models.pages import FAQPageModel
        >>> path = write_json_output(faq_page, "faq.json")
        >>> print(f"Written to: {path}")
    """
    # Ensure output directory exists
    output_path = ensure_output_directory(output_dir)
    file_path = output_path / filename
    
    # Convert Pydantic models to dict
    if isinstance(data, BaseModel):
        data_dict = data.model_dump(mode='json')
    elif isinstance(data, dict):
        data_dict = data
    elif isinstance(data, list):
        data_dict = data
    else:
        raise TypeError(f"Cannot serialize type {type(data)}")
    
    # Custom JSON encoder for datetime objects
    def json_serializer(obj):
        if isinstance(obj, datetime):
            return obj.isoformat()
        raise TypeError(f"Object of type {type(obj)} is not JSON serializable")
    
    try:
        with open(file_path, 'w', encoding='utf-8') as f:
            json.dump(data_dict, f, indent=indent, default=json_serializer, ensure_ascii=False)
        
        file_size = file_path.stat().st_size
        print(f" Written to: {file_path} ({file_size} bytes)")
        return file_path
        
    except (OSError, TypeError) as e:
        raise Exception(f"Failed to write JSON file: {e}")

def read_json_input(filepath: str) -> Dict[str, Any]:
    """
    Read JSON input file.
    
    Args:
        filepath: Path to JSON file
        
    Returns:
        Parsed JSON data as dictionary
        
    Raises:
        FileNotFoundError: If file does not exist
        ValueError: If JSON is invalid
    """
    file_path = Path(filepath)
    
    if not file_path.exists():
        raise FileNotFoundError(f"Input file not found: {filepath}")
    
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
        return data
    except json.JSONDecodeError as e:
        raise ValueError(f"Invalid JSON in {filepath}: {e}")

def create_backup(filepath: str) -> Path:
    """
    Create a timestamped backup of an existing file.
    
    Args:
        filepath: Path to file to backup
        
    Returns:
        Path to the backup file
        
    Example:
        >>> backup_path = create_backup("output/faq.json")
        >>> # Creates: output/faq_backup_20240115_103045.json
    """
    file_path = Path(filepath)
    
    if not file_path.exists():
        raise FileNotFoundError(f"File to backup not found: {filepath}")
    
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    backup_name = f"{file_path.stem}_backup_{timestamp}{file_path.suffix}"
    backup_path = file_path.parent / backup_name
    
    try:
        import shutil
        shutil.copy2(file_path, backup_path)
        return backup_path
    except OSError as e:
        raise OSError(f"Failed to create backup: {e}")

def write_json_with_backup(
    data: Any,
    filename: str,
    output_dir: str = "output",
    indent: int = 2
) -> Path:
    """
    Write JSON output with automatic backup of existing file.
    
    Args:
        data: Data to write
        filename: Output filename
        output_dir: Output directory
        indent: JSON indentation
        
    Returns:
        Path to written file
    """
    output_path = ensure_output_directory(output_dir)
    file_path = output_path / filename
    
    # Create backup if file exists
    if file_path.exists():
        create_backup(str(file_path))
    
    # Write new file
    return write_json_output(data, filename, output_dir, indent)


def get_output_summary(output_dir: str = "output") -> Dict[str, Any]:
    """
    Get summary of files in output directory.
    
    Args:
        output_dir: Output directory path
        
    Returns:
        Dictionary with file count, total size, and file list
        
    Example:
        >>> summary = get_output_summary()
        >>> print(f"Total files: {summary['total_files']}")
    """
    output_path = Path(output_dir)
    
    if not output_path.exists():
        return {
            "total_files": 0,
            "total_size_bytes": 0,
            "files": []
        }
    
    files = []
    total_size = 0
    
    for file_path in output_path.glob("*.json"):
        file_size = file_path.stat().st_size
        files.append({
            "name": file_path.name,
            "size_bytes": file_size,
            "modified": datetime.fromtimestamp(file_path.stat().st_mtime).isoformat()
        })
        total_size += file_size
    
    return {
        "total_files": len(files),
        "total_size_bytes": total_size,
        "files": files
    }
