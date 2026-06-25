"""
Reviewer agent for Multi-Step Research Agent.
Evaluates research quality and determines if more research is needed.
"""

import json
from models.llm import get_llm
from prompts.reviewer_prompt import REVIEWER_PROMPT
from utils.helpers import parse_json_response, truncate_text
from utils.logger import log


def review_research(state: dict) -> dict:
    """
    Review research findings to determine if sufficient information has been gathered.
    
    Args:
        state: Current research state
    
    Returns:
        Updated state with review results
    """
    log.info("📊 REVIEWER: Starting research review")
    
    question = state.get("question", "")
    findings = state.get("findings", [])
    
    try:
        # Get LLM
        llm = get_llm(temperature=0.1)
        
        # Convert findings to JSON string
        findings_json = json.dumps(findings, indent=2)
        findings_json = truncate_text(findings_json, 8000)
        
        # Format prompt
        formatted_prompt = REVIEWER_PROMPT.format(
            question=question,
            findings=findings_json
        )
        
        # Invoke LLM
        log.info("🧠 REVIEWER: Evaluating research quality with LLM")
        response = llm.invoke(formatted_prompt)
        
        # Parse JSON response
        result = parse_json_response(
            response.content,
            fallback={
                "is_sufficient": True,
                "quality_score": 7,
                "gaps": [],
                "additional_searches": [],
                "reasoning": "Failed to parse LLM response, defaulting to sufficient"
            }
        )
        
        quality_score = result.get("quality_score", 7)
        is_sufficient = result.get("is_sufficient", quality_score >= 7)
        
        log.info(f"✅ REVIEWER: Quality score = {quality_score}/10")
        log.info(f"✅ REVIEWER: Sufficient = {is_sufficient}")
        
        if result.get("gaps"):
            log.info(f"   Gaps identified: {len(result['gaps'])}")
        
        # Return updated state (immutable)
        return {
            **state,
            "review": result,
            "status": "reviewed"
        }
        
    except Exception as e:
        log.error(f"❌ REVIEWER: Error during review: {e}")
        # Fallback: assume sufficient to avoid infinite loops
        log.warning("⚠️ REVIEWER: Using fallback - assuming research is sufficient")
        return {
            **state,
            "review": {
                "is_sufficient": True,
                "quality_score": 7,
                "gaps": [],
                "additional_searches": [],
                "reasoning": "Error during review, defaulting to sufficient"
            },
            "status": "reviewed"
        }
