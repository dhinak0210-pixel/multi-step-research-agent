"""
Configuration module for Multi-Step Research Agent.
Loads environment variables and defines all constants.
"""

import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# API Configuration
GROQ_API_KEY = os.getenv("GROQ_API_KEY")

# LLM Configuration
LLM_PROVIDER = "groq"
GROQ_MODEL = "llama-3.3-70b-versatile"

# Search Configuration
MAX_SEARCH_RESULTS = 5
MAX_SCRAPE_URLS = 3

# Research Loop Configuration
MAX_RESEARCH_LOOPS = 3

# Text Processing Configuration
CHUNK_SIZE = 1000
CHUNK_OVERLAP = 200
MAX_CONTENT_LENGTH = 4000

# Vector Database Configuration
COLLECTION_NAME = "research_data"

# Validation - warn but don't raise to allow UI to load
if not GROQ_API_KEY:
    import warnings
    warnings.warn(
        "GROQ_API_KEY not found in environment variables. "
        "Please set it in your .env file or environment. "
        "Get a free key at: https://console.groq.com/keys"
    )
