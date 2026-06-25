"""
LLM initialization module for Multi-Step Research Agent.
Provides Groq LLM instance with retry logic.
"""

from langchain_groq import ChatGroq
from config import GROQ_API_KEY, GROQ_MODEL
from utils.logger import log


def get_llm(temperature: float = 0.1, max_retries: int = 3) -> ChatGroq:
    """
    Get configured Groq LLM instance with retry logic.
    
    Args:
        temperature: LLM temperature (default: 0.1 for deterministic responses)
        max_retries: Maximum number of retry attempts
    
    Returns:
        Configured ChatGroq instance
    
    Raises:
        ValueError: If GROQ_API_KEY is not set
    """
    if not GROQ_API_KEY:
        raise ValueError(
            "GROQ_API_KEY is not configured. "
            "Please set it in your .env file or environment. "
            "Get a free key at: https://console.groq.com/keys"
        )
    
    try:
        llm = ChatGroq(
            model=GROQ_MODEL,
            groq_api_key=GROQ_API_KEY,
            temperature=temperature,
            max_retries=max_retries
        )
        log.info(f"✅ LLM initialized: {GROQ_MODEL} (temperature={temperature})")
        return llm
    except Exception as e:
        log.error(f"❌ Failed to initialize LLM: {e}")
        raise
