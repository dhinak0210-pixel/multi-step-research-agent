"""
Synthesizer agent for Multi-Step Research Agent.
Generates the final comprehensive research report.
"""

import json
from models.llm import get_llm
from prompts.synthesizer_prompt import SYNTHESIZER_PROMPT
from tools.vectorstore_tool import query_collection
from utils.helpers import truncate_text
from utils.logger import log


def synthesize_report(state: dict) -> dict:
    """
    Synthesize all findings into a comprehensive markdown report.
    
    Args:
        state: Current research state
    
    Returns:
        Updated state with final report
    """
    log.info("📝 SYNTHESIZER: Starting report synthesis")
    
    question = state.get("question", "")
    findings = state.get("findings", [])
    sources = state.get("sources", [])
    
    try:
        # Query vector database for relevant context
        log.info("🔎 SYNTHESIZER: Querying vector database for context")
        vector_results = query_collection(question, n_results=15)
        
        # Join chunks into context string
        context_chunks = vector_results.get("documents", [[]])[0]
        context = "\n\n".join(context_chunks)
        context = truncate_text(context, 5000)
        
        # Convert findings to JSON string
        findings_json = json.dumps(findings, indent=2)
        findings_json = truncate_text(findings_json, 8000)
        
        # Format sources list
        sources_text = "\n".join([f"- {url}" for url in sources])
        
        # Get LLM with slightly higher temperature for creativity
        llm = get_llm(temperature=0.3)
        
        # Format prompt
        formatted_prompt = SYNTHESIZER_PROMPT.format(
            question=question,
            all_findings=findings_json,
            context=context,
            sources=sources_text
        )
        
        # Invoke LLM
        log.info("🧠 SYNTHESIZER: Generating report with LLM")
        response = llm.invoke(formatted_prompt)
        
        report = response.content
        
        log.info(f"✅ SYNTHESIZER: Generated report ({len(report)} characters)")
        
        # Return updated state (immutable)
        return {
            **state,
            "report": report,
            "status": "complete"
        }
        
    except Exception as e:
        log.error(f"❌ SYNTHESIZER: Error during synthesis: {e}")
        # Fallback: generate simple report
        fallback_report = f"""# Research Report: {question}

## Executive Summary
An error occurred during report synthesis. Please try again.

## Findings
{json.dumps(findings, indent=2)}

## Sources
{chr(10).join([f"- {url}" for url in sources])}
"""
        return {
            **state,
            "report": fallback_report,
            "status": "complete"
        }
