"""
LLM client configuration and wrapper for GPT-4o-mini.

This module provides:
- Centralized LLM configuration
- Structured output support via Pydantic
- Consistent error handling
"""

import os
from typing import Type, TypeVar
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from pydantic import BaseModel

# Load environment variables
load_dotenv()

# Type variable for Pydantic models
T = TypeVar('T', bound=BaseModel)


def get_llm(temperature: float = 0.7, model: str = "gpt-4o-mini") -> ChatOpenAI:
    """
    Get a standard LLM instance for text generation.
    
    Args:
        temperature: Creativity level (0.0-1.0)
        model: Model name
        
    Returns:
        Configured ChatOpenAI instance
        
    Raises:
        ValueError: If OPENAI_API_KEY is not set
    """
    api_key = os.getenv("OPENAI_API_KEY")
    
    if not api_key:
        raise ValueError("OPENAI_API_KEY environment variable not set")
    
    return ChatOpenAI(
        api_key=api_key,
        model=model,
        temperature=temperature
    )


def get_structured_llm(
    pydantic_model: Type[T],
    temperature: float = 0.3,
    model: str = "gpt-4o-mini"
) -> ChatOpenAI:
    """
    Get an LLM instance configured for structured output.
    
    This uses OpenAI's function calling to ensure the response
    matches the provided Pydantic model exactly.
    
    Args:
        pydantic_model: Pydantic model for response validation
        temperature: Creativity level (lower for structured output)
        model: Model name
        
    Returns:
        Configured ChatOpenAI instance with structured output
        
    Example:
        >>> llm = get_structured_llm(QuestionModel)
        >>> # response is automatically parsed as QuestionModel
    """
    api_key = os.getenv("OPENAI_API_KEY")
    
    if not api_key:
        raise ValueError("OPENAI_API_KEY environment variable not set")
    
    llm = ChatOpenAI(
        api_key=api_key,
        model=model,
        temperature=temperature
    )
    
    # Bind the Pydantic model for structured output
    return llm.with_structured_output(pydantic_model)


def get_llm_with_token_limit(
    max_tokens: int = 2000,
    temperature: float = 0.7,
    model: str = "gpt-4o-mini"
) -> ChatOpenAI:
    """
    Get an LLM instance with explicit token limit.
    
    Useful for controlling output length in specific agents.
    
    Args:
        max_tokens: Maximum tokens in response
        temperature: Creativity level
        model: Model name
        
    Returns:
        Configured ChatOpenAI instance with token limit
    """
    api_key = os.getenv("OPENAI_API_KEY")
    
    if not api_key:
        raise ValueError("OPENAI_API_KEY environment variable not set")
    
    return ChatOpenAI(
        api_key=api_key,
        model=model,
        temperature=temperature,
        max_tokens=max_tokens
    )


# Configuration constants
DEFAULT_MODEL = "gpt-4o-mini"
CREATIVE_TEMPERATURE = 0.8
STRUCTURED_TEMPERATURE = 0.3
DETERMINISTIC_TEMPERATURE = 0.0

# Token limits for different use cases
TOKENS_SHORT = 500      # For brief descriptions
TOKENS_MEDIUM = 1500    # For standard content
TOKENS_LONG = 2000      # For detailed content
