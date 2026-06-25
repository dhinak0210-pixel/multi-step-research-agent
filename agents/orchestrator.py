"""
Orchestrator for Multi-Step Research Agent.
Builds and manages the LangGraph state machine.
"""

from typing import TypedDict, Annotated, Sequence
from typing_extensions import TypedDict
from langgraph.graph import StateGraph, END
from agents.planner import plan_research
from agents.researcher import research_step
from agents.reviewer import review_research
from agents.synthesizer import synthesize_report
from tools.vectorstore_tool import clear_collection
from config import MAX_RESEARCH_LOOPS
from utils.logger import log


class ResearchState(TypedDict):
    question: str
    sub_questions: list[str]
    plan_reasoning: str
    current_step: int
    findings: list[dict]
    review: dict
    report: str
    status: str
    loop_count: int
    sources: list[str]


def add_additional_searches(state: ResearchState) -> ResearchState:
    """
    Add additional search queries from review to sub_questions.
    
    Args:
        state: Current research state
    
    Returns:
        Updated state with additional searches added
    """
    review = state.get("review", {})
    additional_searches = review.get("additional_searches", [])
    sub_questions = state.get("sub_questions", [])
    loop_count = state.get("loop_count", 0)
    
    if additional_searches:
        log.info(f"🔄 ADD_SEARCHES: Adding {len(additional_searches)} additional queries")
        sub_questions.extend(additional_searches)
        
        return {
            **state,
            "sub_questions": sub_questions,
            "current_step": 0,
            "loop_count": loop_count + 1
        }
    
    return state


def should_continue_research(state: ResearchState) -> str:
    """
    Determine whether to continue researching or move to review.
    
    Args:
        state: Current research state
    
    Returns:
        "research" if more sub-questions to research, "review" otherwise
    """
    current_step = state.get("current_step", 0)
    sub_questions = state.get("sub_questions", [])
    
    if current_step < len(sub_questions):
        log.info(f"🔄 ORCHESTRATOR: Continuing research (step {current_step + 1}/{len(sub_questions)})")
        return "research"
    else:
        log.info("✅ ORCHESTRATOR: All sub-questions researched, moving to review")
        return "review"


def should_do_more_research(state: ResearchState) -> str:
    """
    Determine whether to do more research loops or synthesize report.
    
    Args:
        state: Current research state
    
    Returns:
        "research" if more research needed, "synthesize" otherwise
    """
    loop_count = state.get("loop_count", 0)
    review = state.get("review", {})
    is_sufficient = review.get("is_sufficient", True)
    
    # Check if we've reached max loops
    if loop_count >= MAX_RESEARCH_LOOPS:
        log.info(f"⏹️ ORCHESTRATOR: Max loops ({MAX_RESEARCH_LOOPS}) reached, synthesizing report")
        return "synthesize"
    
    # Check if research is sufficient
    if is_sufficient:
        log.info("✅ ORCHESTRATOR: Research quality sufficient, synthesizing report")
        return "synthesize"
    
    # Need more research - add additional searches
    additional_searches = review.get("additional_searches", [])
    
    if additional_searches:
        log.info(f"🔄 ORCHESTRATOR: Adding {len(additional_searches)} additional search queries")
        # Note: state mutation happens in a separate node, this just decides routing
        return "research"
    else:
        log.warning("⚠️ ORCHESTRATOR: No additional searches suggested, synthesizing anyway")
        return "synthesize"


def build_research_graph():
    """
    Build the LangGraph state machine for research workflow.
    
    Returns:
        Compiled StateGraph
    """
    log.info("🔧 ORCHESTRATOR: Building research graph")
    
    # Create state graph
    workflow = StateGraph(ResearchState)
    
    # Add nodes
    workflow.add_node("planner", plan_research)
    workflow.add_node("researcher", research_step)
    workflow.add_node("reviewer", review_research)
    workflow.add_node("add_searches", add_additional_searches)
    workflow.add_node("synthesizer", synthesize_report)
    
    # Set entry point
    workflow.set_entry_point("planner")
    
    # Add edges
    workflow.add_edge("planner", "researcher")
    
    # Add conditional edge from researcher
    workflow.add_conditional_edges(
        "researcher",
        should_continue_research,
        {
            "research": "researcher",
            "review": "reviewer"
        }
    )
    
    # Add conditional edge from reviewer
    workflow.add_conditional_edges(
        "reviewer",
        should_do_more_research,
        {
            "research": "add_searches",
            "synthesize": "synthesizer"
        }
    )
    
    # Add edge from add_searches back to researcher
    workflow.add_edge("add_searches", "researcher")
    
    # Add edge from synthesizer to END
    workflow.add_edge("synthesizer", END)
    
    # Compile graph
    compiled_graph = workflow.compile()
    log.info("✅ ORCHESTRATOR: Research graph built successfully")
    
    return compiled_graph


def run_research(question: str) -> dict:
    """
    Run the complete research workflow.
    
    Args:
        question: Research question to investigate
    
    Returns:
        Final research state with report
    """
    log.info("=" * 60)
    log.info("🚀 ORCHESTRATOR: Starting research workflow")
    log.info(f"📝 Question: {question}")
    log.info("=" * 60)
    
    # Clear previous collection
    clear_collection()
    
    # Build graph
    graph = build_research_graph()
    
    # Create initial state
    initial_state: ResearchState = {
        "question": question,
        "sub_questions": [],
        "plan_reasoning": "",
        "current_step": 0,
        "findings": [],
        "review": {},
        "report": "",
        "status": "initialized",
        "loop_count": 0,
        "sources": []
    }
    
    try:
        # Invoke graph
        log.info("⏳ ORCHESTRATOR: Invoking research graph")
        final_state = graph.invoke(initial_state)
        
        log.info("=" * 60)
        log.info("✅ ORCHESTRATOR: Research workflow completed")
        log.info(f"📊 Status: {final_state.get('status')}")
        log.info(f"📝 Report length: {len(final_state.get('report', ''))} characters")
        log.info(f"🔍 Sources visited: {len(final_state.get('sources', []))}")
        log.info("=" * 60)
        
        return final_state
        
    except Exception as e:
        log.error(f"❌ ORCHESTRATOR: Error during research workflow: {e}")
        raise
