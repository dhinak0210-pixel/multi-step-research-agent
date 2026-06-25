"""
DuckDuckGo search tool for Multi-Step Research Agent.
Performs web searches without requiring API keys.
"""

import time
from typing import List, Dict
from duckduckgo_search import DDGS
from config import MAX_SEARCH_RESULTS
from utils.logger import log


def search_web(query: str) -> List[Dict[str, str]]:
    """
    Search the web using DuckDuckGo.
    
    Args:
        query: Search query string
    
    Returns:
        List of dicts with keys: title, link, snippet
        Returns empty list on error
    """
    log.info(f"🔍 Searching: {query}")
    
    try:
        # Add delay to avoid rate limiting
        time.sleep(1)
        
        results = []
        with DDGS() as ddgs:
            search_results = list(ddgs.text(
                query,
                max_results=MAX_SEARCH_RESULTS
            ))
        
        for result in search_results:
            results.append({
                "title": result.get("title", ""),
                "link": result.get("href", ""),
                "snippet": result.get("body", "")
            })
        
        log.info(f"✅ Found {len(results)} results for: {query}")
        return results
        
    except Exception as e:
        log.error(f"❌ Search failed for '{query}': {e}")
        return []
