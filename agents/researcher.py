"""
Researcher agent for Multi-Step Research Agent.
Performs web search and scraping for each sub-question.
"""

import json
from models.llm import get_llm
from prompts.researcher_prompt import RESEARCHER_PROMPT
from tools.search_tool import search_web
from tools.scraper_tool import scrape_url, chunk_text
from tools.vectorstore_tool import store_chunks
from config import MAX_SCRAPE_URLS
from utils.helpers import parse_json_response, truncate_text
from utils.logger import log


def research_step(state: dict) -> dict:
    """
    Research a single sub-question by searching and scraping web content.
    
    Args:
        state: Current research state
    
    Returns:
        Updated state with new finding and incremented current_step
    """
    log.info("🔍 RESEARCHER: Starting research step")
    
    sub_questions = state.get("sub_questions", [])
    current_step = state.get("current_step", 0)
    sources = state.get("sources", [])
    
    # Get current sub-question
    if current_step >= len(sub_questions):
        log.warning("⚠️ RESEARCHER: No more sub-questions to research")
        return {**state, "status": "researching"}
    
    sub_question = sub_questions[current_step]
    log.info(f"🔍 RESEARCHER: Researching sub-question {current_step + 1}/{len(sub_questions)}: {sub_question}")
    
    try:
        # Search web
        search_results = search_web(sub_question)
        
        if not search_results:
            log.warning(f"⚠️ RESEARCHER: No search results for: {sub_question}")
            # Still increment step and add empty finding
            return {
                **state,
                "current_step": current_step + 1,
                "status": "researching"
            }
        
        # Scrape top URLs
        scraped_content = []
        urls_scraped = []
        
        for i, result in enumerate(search_results[:MAX_SCRAPE_URLS]):
            url = result.get("link", "")
            if not url:
                continue
            
            try:
                content = scrape_url(url)
                if content and not content.startswith("Error:"):
                    chunks = chunk_text(content)
                    if chunks:
                        store_chunks(chunks, url, sub_question)
                        scraped_content.append(f"Source: {url}\n{content}")
                        urls_scraped.append(url)
                        sources.append(url)
            except Exception as e:
                log.warning(f"⚠️ RESEARCHER: Failed to scrape {url}: {e}")
                continue
        
        # Build search text for LLM
        search_text = "\n\n".join([
            f"Title: {r.get('title', '')}\nURL: {r.get('link', '')}\nSnippet: {r.get('snippet', '')}"
            for r in search_results
        ])
        
        # Add scraped content if available
        if scraped_content:
            search_text += "\n\n--- Scraped Content ---\n\n" + "\n\n".join(scraped_content[:2])  # Limit to 2 sources for context
        
        # Truncate if too long
        search_text = truncate_text(search_text, 6000)
        
        # Get LLM analysis
        llm = get_llm(temperature=0.1)
        formatted_prompt = RESEARCHER_PROMPT.format(
            sub_question=sub_question,
            search_results=search_text
        )
        
        log.info("🧠 RESEARCHER: Analyzing search results with LLM")
        response = llm.invoke(formatted_prompt)
        
        # Parse JSON response
        result = parse_json_response(
            response.content,
            fallback={
                "sub_question": sub_question,
                "key_findings": [],
                "summary": "Failed to parse LLM response",
                "gaps": "Unknown"
            }
        )
        
        # Append finding to state
        findings = state.get("findings", [])
        findings.append(result)
        
        log.info(f"✅ RESEARCHER: Completed research for sub-question {current_step + 1}")
        log.info(f"   Found {len(result.get('key_findings', []))} key findings")
        log.info(f"   Scraped {len(urls_scraped)} URLs")
        
        # Return updated state (immutable)
        return {
            **state,
            "current_step": current_step + 1,
            "findings": findings,
            "sources": sources,
            "status": "researching"
        }
        
    except Exception as e:
        log.error(f"❌ RESEARCHER: Error during research: {e}")
        # Still increment step to avoid infinite loop
        return {
            **state,
            "current_step": current_step + 1,
            "status": "researching"
        }
