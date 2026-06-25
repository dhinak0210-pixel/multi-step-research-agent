"""
Planner agent for Multi-Step Research Agent.
Breaks research questions into sub-questions.
"""

from models.llm import get_llm
from prompts.planner_prompt import PLANNER_PROMPT
from utils.helpers import parse_json_response
from utils.logger import log


def plan_research(state: dict) -> dict:
    """
    Plan research by breaking the main question into sub-questions.
    
    Args:
        state: Current research state
    
    Returns:
        Updated state with sub_questions and plan_reasoning
    """
    log.info("📋 PLANNER: Starting research planning")
    
    question = state.get("question", "")
    
    try:
        # Get LLM with slightly higher temperature for creativity
        llm = get_llm(temperature=0.2)
        
        # Format prompt with question
        formatted_prompt = PLANNER_PROMPT.format(question=question)
        
        # Invoke LLM
        log.info("🧠 PLANNER: Invoking LLM to generate sub-questions")
        response = llm.invoke(formatted_prompt)
        
        # Parse JSON response
        result = parse_json_response(
            response.content,
            fallback={
                "sub_questions": [question],
                "reasoning": "Failed to parse LLM response, using original question"
            }
        )
        
        sub_questions = result.get("sub_questions", [question])
        plan_reasoning = result.get("reasoning", "No reasoning provided")
        
        log.info(f"✅ PLANNER: Generated {len(sub_questions)} sub-questions")
        for i, sq in enumerate(sub_questions, 1):
            log.info(f"   {i}. {sq}")
        
        # Return updated state (immutable)
        return {
            **state,
            "sub_questions": sub_questions,
            "plan_reasoning": plan_reasoning,
            "current_step": 0,
            "findings": [],
            "status": "planned",
            "loop_count": 0,
            "sources": []
        }
        
    except Exception as e:
        log.error(f"❌ PLANNER: Error during planning: {e}")
        # Fallback: use original question as single sub-question
        log.warning("⚠️ PLANNER: Using fallback - original question as single sub-question")
        return {
            **state,
            "sub_questions": [question],
            "plan_reasoning": "Error during planning, using original question",
            "current_step": 0,
            "findings": [],
            "status": "planned",
            "loop_count": 0,
            "sources": []
        }
