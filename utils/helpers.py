"""
Helper functions for Multi-Step Research Agent.
Utility functions used across multiple modules.
"""

import json
import hashlib
from typing import Any, Dict
from utils.logger import log


def parse_json_response(response_text: str, fallback: Dict[str, Any] = None) -> Dict[str, Any]:
    """
    Parse JSON from LLM response, handling markdown code fences.
    
    Args:
        response_text: Raw response text from LLM
        fallback: Fallback dict if parsing fails
    
    Returns:
        Parsed JSON dict or fallback
    """
    if fallback is None:
        fallback = {}
    
    try:
        # Remove markdown code fences if present
        text = response_text.strip()
        if text.startswith("```json"):
            text = text[7:]
        elif text.startswith("```"):
            text = text[3:]
        if text.endswith("```"):
            text = text[:-3]
        text = text.strip()
        
        return json.loads(text)
    except json.JSONDecodeError as e:
        log.warning(f"Failed to parse JSON response: {e}")
        log.warning(f"Response text: {response_text[:200]}...")
        return fallback
    except Exception as e:
        log.error(f"Unexpected error parsing JSON: {e}")
        return fallback


def truncate_text(text: str, max_length: int = 8000, suffix: str = "...[truncated for length]") -> str:
    """
    Truncate text to maximum length with suffix.
    
    Args:
        text: Text to truncate
        max_length: Maximum length
        suffix: Suffix to add when truncated
    
    Returns:
        Truncated text
    """
    if len(text) <= max_length:
        return text
    return text[:max_length - len(suffix)] + suffix


def generate_id(url: str, index: int) -> str:
    """
    Generate a unique ID from URL and index.
    
    Args:
        url: Source URL
        index: Chunk index
    
    Returns:
        Unique ID string
    """
    hash_input = f"{url}_{index}".encode()
    return hashlib.md5(hash_input).hexdigest()[:16]


def format_timestamp() -> str:
    """
    Get current timestamp as ISO format string.
    
    Returns:
        ISO format timestamp
    """
    from datetime import datetime
    return datetime.utcnow().isoformat() + "Z"
