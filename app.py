"""
Streamlit UI for Multi-Step Research Agent.
Main entry point for the web interface.
"""

import streamlit as st
import time
from datetime import datetime
from agents.orchestrator import run_research
from utils.logger import log


# Page config
st.set_page_config(
    page_title="Aetheris | Autonomous Research Engine",
    page_icon="✦",
    layout="wide"
)

# Custom CSS for Ultra-Luxury Aesthetic
st.markdown(
    """
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Cinzel:wght@400;500;600;700&family=Inter:wght@300;400;500;600&family=Playfair+Display:ital,wght@0,400;0,500;0,600;1,400&display=swap');

    /* Main App Styles */
    .stApp {
        background-color: #0a0a0c !important;
        color: #e4e4e7 !important;
        font-family: 'Inter', sans-serif !important;
    }

    /* Sidebar styling */
    [data-testid="stSidebar"] {
        background-color: #060608 !important;
        border-right: 1px solid #1a1a22 !important;
        padding-top: 2rem !important;
    }

    /* Headers */
    h1, h2, h3, h4, h5, h6 {
        font-family: 'Cinzel', serif !important;
        color: #c5a880 !important;
        font-weight: 500 !important;
        letter-spacing: 0.1em !important;
    }

    .luxury-title {
        font-family: 'Cinzel', serif !important;
        font-size: 2.8rem !important;
        font-weight: 600 !important;
        letter-spacing: 0.2em !important;
        color: #c5a880 !important;
        text-align: center !important;
        margin-top: 1.5rem !important;
        margin-bottom: 0.2rem !important;
        text-shadow: 0 0 20px rgba(197, 168, 128, 0.1);
    }

    .luxury-subtitle {
        font-family: 'Playfair Display', serif !important;
        font-style: italic !important;
        font-size: 1.1rem !important;
        color: #a1a1aa !important;
        text-align: center !important;
        margin-bottom: 2.5rem !important;
        letter-spacing: 0.05em !important;
    }

    /* Input Fields */
    textarea {
        background-color: #0f0f12 !important;
        color: #f4f4f5 !important;
        border: 1px solid #1a1a22 !important;
        border-radius: 2px !important;
        font-family: 'Inter', sans-serif !important;
        font-size: 0.95rem !important;
        transition: all 0.3s ease !important;
        padding: 1rem !important;
    }

    textarea:focus {
        border-color: #c5a880 !important;
        box-shadow: 0 0 8px rgba(197, 168, 128, 0.2) !important;
    }

    /* Buttons */
    div.stButton > button {
        background-color: transparent !important;
        color: #c5a880 !important;
        border: 1px solid #c5a880 !important;
        padding: 0.7rem 1.8rem !important;
        font-family: 'Inter', sans-serif !important;
        font-weight: 500 !important;
        letter-spacing: 0.15em !important;
        text-transform: uppercase !important;
        font-size: 0.8rem !important;
        transition: all 0.3s cubic-bezier(0.25, 0.8, 0.25, 1) !important;
        border-radius: 2px !important;
        width: 100% !important;
        margin-bottom: 1rem !important;
    }

    div.stButton > button:hover {
        background-color: #c5a880 !important;
        color: #0a0a0c !important;
        border-color: #c5a880 !important;
        box-shadow: 0 0 15px rgba(197, 168, 128, 0.3) !important;
    }

    /* Tabs */
    button[data-baseweb="tab"] {
        font-family: 'Cinzel', serif !important;
        color: #a1a1aa !important;
        font-size: 0.9rem !important;
        letter-spacing: 0.1em !important;
        padding: 1rem 1.5rem !important;
        border-bottom: 2px solid transparent !important;
        transition: all 0.3s ease !important;
    }

    button[data-baseweb="tab"]:hover {
        color: #c5a880 !important;
    }

    button[data-baseweb="tab"][aria-selected="true"] {
        color: #c5a880 !important;
        border-bottom: 2px solid #c5a880 !important;
    }

    /* Metrics and Cards */
    div[data-testid="stMetric"] {
        background-color: #0f0f12 !important;
        border: 1px solid #1a1a22 !important;
        padding: 1rem 1.5rem !important;
        border-radius: 2px !important;
        box-shadow: 0 4px 12px rgba(0,0,0,0.15) !important;
    }

    div[data-testid="stMetricValue"] {
        font-family: 'Cinzel', serif !important;
        color: #c5a880 !important;
        font-size: 1.8rem !important;
    }

    div[data-testid="stMetricLabel"] {
        font-family: 'Inter', sans-serif !important;
        color: #71717a !important;
        letter-spacing: 0.08em !important;
        text-transform: uppercase !important;
        font-size: 0.7rem !important;
    }

    /* Expanders */
    div[data-testid="stExpander"] {
        background-color: #0f0f12 !important;
        border: 1px solid #1a1a22 !important;
        border-radius: 2px !important;
    }

    /* Custom Step List */
    .step-container {
        margin-bottom: 1.5rem;
        padding-bottom: 1rem;
        border-bottom: 1px solid #14141a;
    }

    .step-num {
        font-family: 'Cinzel', serif;
        color: #c5a880;
        font-size: 1.1rem;
        font-weight: 500;
        margin-right: 0.5rem;
    }

    /* Info & Success box overrides */
    div.stAlert {
        background-color: #0f0f12 !important;
        border: 1px solid #1a1a22 !important;
        color: #e4e4e7 !important;
        border-radius: 2px !important;
    }

    div.stAlert > div {
        color: #e4e4e7 !important;
    }

    /* Hide default streamlit indicators */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    </style>
    """,
    unsafe_allow_html=True
)


def init_session_state():
    """Initialize session state variables."""
    if "research_result" not in st.session_state:
        st.session_state.research_result = None
    if "research_history" not in st.session_state:
        st.session_state.research_history = []
    if "start_time" not in st.session_state:
        st.session_state.start_time = None


def render_sidebar():
    """Render the sidebar with instructions and tips."""
    with st.sidebar:
        st.markdown("<h3 style='margin-bottom: 1.5rem;'>METHODOLOGY</h3>", unsafe_allow_html=True)
        
        st.markdown("""
        <div class="step-container">
            <span class="step-num">01</span> <strong>Decomposition</strong>
            <div style="color: #a1a1aa; font-size: 0.85rem; margin-top: 0.2rem;">Orchestrator plan breaks the query into targeted sub-questions.</div>
        </div>
        <div class="step-container">
            <span class="step-num">02</span> <strong>Acquisition</strong>
            <div style="color: #a1a1aa; font-size: 0.85rem; margin-top: 0.2rem;">Parallel search, scraping, and vector database indexing.</div>
        </div>
        <div class="step-container">
            <span class="step-num">03</span> <strong>Evaluation</strong>
            <div style="color: #a1a1aa; font-size: 0.85rem; margin-top: 0.2rem;">Automated quality scoring, feedback loops, and gap analysis.</div>
        </div>
        <div class="step-container" style="border-bottom: none; margin-bottom: 0;">
            <span class="step-num">04</span> <strong>Curation</strong>
            <div style="color: #a1a1aa; font-size: 0.85rem; margin-top: 0.2rem;">Synthesis of a comprehensive markdown report with references.</div>
        </div>
        """, unsafe_allow_html=True)
        
        st.divider()
        
        st.markdown("<h3>TECHNOLOGY STACK</h3>", unsafe_allow_html=True)
        st.markdown("""
        <div style="font-size: 0.85rem; color: #a1a1aa; line-height: 1.6;">
            • LangGraph Stateful Graphs<br>
            • LangChain Framework<br>
            • Llama 3.3 (Groq API)<br>
            • DuckDuckGo Engine<br>
            • ChromaDB Vector Client<br>
            • Streamlit Layout
        </div>
        """, unsafe_allow_html=True)
        
        st.divider()
        
        st.markdown("<h3>CREDENTIALS</h3>", unsafe_allow_html=True)
        st.markdown("""
        <div style="font-size: 0.85rem; color: #a1a1aa; line-height: 1.5; margin-bottom: 1rem;">
            Configure your Groq API key in your <code>.env</code> file:
        </div>
        <pre style="background-color: #0f0f12; border: 1px solid #1a1a22; padding: 0.5rem; color: #c5a880; font-size: 0.8rem; border-radius: 2px;">GROQ_API_KEY=your_key_here</pre>
        """, unsafe_allow_html=True)


def render_example_questions():
    """Render clickable example questions."""
    st.markdown("<h3 style='margin-top: 2rem; margin-bottom: 1rem;'>SUGGESTED RESEARCH TOPICS</h3>", unsafe_allow_html=True)
    
    examples = [
        "What are the latest breakthroughs in nuclear fusion energy and when might commercial fusion power plants be operational?",
        "How is artificial intelligence transforming the job market and which industries are most affected in 2024?",
        "What are the most effective carbon capture technologies currently available and what are their costs and limitations?",
        "What is the current state of quantum computing and what are the main challenges to practical applications?",
        "How are CRISPR gene editing technologies being used in medicine and what are the ethical considerations?",
        "What are the economic impacts of climate change on developing countries and what adaptation strategies are being implemented?"
    ]
    
    cols = st.columns(3)
    for i, example in enumerate(examples):
        with cols[i % 3]:
            if st.button(example[:55] + "...", key=f"example_{i}", use_container_width=True):
                st.session_state.question = example


def render_progress_placeholder():
    """Render progress display during research."""
    progress_placeholder = st.empty()
    status_placeholder = st.empty()
    
    return progress_placeholder, status_placeholder


def update_progress(progress_placeholder, status_placeholder, stage, progress, message):
    """Update progress display."""
    status_placeholder.info(message)
    progress_placeholder.progress(progress / 100)


def render_results(result):
    """Render research results in tabs."""
    if not result:
        return
    
    # Create tabs
    tab1, tab2, tab3 = st.tabs(["INTELLIGENCE REPORT", "COGNITIVE TRACE", "METRICS"])
    
    # Tab 1: Final Report
    with tab1:
        st.markdown(result.get("report", "No report generated"))
        
        # Download button
        report_text = result.get("report", "")
        st.download_button(
            label="EXPORT REPORT (.md)",
            data=report_text,
            file_name=f"research_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.md",
            mime="text/markdown"
        )
        
        # Word count
        word_count = len(report_text.split())
        st.markdown(f"<div style='color: #71717a; font-size: 0.8rem; margin-top: 10px;'>Report Volume: {word_count} words</div>", unsafe_allow_html=True)
    
    # Tab 2: Research Details
    with tab2:
        st.markdown("<h3>Research Plan</h3>", unsafe_allow_html=True)
        st.markdown(f"**Reasoning:** {result.get('plan_reasoning', 'N/A')}")
        
        st.markdown("<h3 style='margin-top: 1.5rem;'>Sub-Questions</h3>", unsafe_allow_html=True)
        for i, sq in enumerate(result.get("sub_questions", []), 1):
            st.markdown(f"{i}. {sq}")
        
        st.divider()
        
        st.markdown("<h3>Findings</h3>", unsafe_allow_html=True)
        findings = result.get("findings", [])
        for i, finding in enumerate(findings, 1):
            with st.expander(f"Finding {i:02d}: {finding.get('sub_question', 'N/A')}"):
                st.markdown(f"**Summary:** {finding.get('summary', 'N/A')}")
                st.markdown(f"**Gaps:** {finding.get('gaps', 'N/A')}")
                
                key_findings = finding.get("key_findings", [])
                if key_findings:
                    st.markdown("**Key Findings:**")
                    for kf in key_findings:
                        st.markdown(f"- {kf.get('finding', 'N/A')}")
                        st.caption(f"  Source: {kf.get('source', 'N/A')} | Confidence: {kf.get('confidence', 'N/A')}")
    
    # Tab 3: Session Stats
    with tab3:
        # Metric cards
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.metric("Sub-Questions", len(result.get("sub_questions", [])))
        
        with col2:
            st.metric("Findings Gathered", len(result.get("findings", [])))
        
        with col3:
            st.metric("Sources Indexed", len(result.get("sources", [])))
        
        with col4:
            st.metric("Refinement Loops", result.get("loop_count", 0))
        
        st.divider()
        
        col5, col6 = st.columns(2)
        
        with col5:
            if st.session_state.start_time:
                elapsed = time.time() - st.session_state.start_time
                st.metric("Execution Duration", f"{elapsed:.1f}s")
        
        with col6:
            review = result.get("review", {})
            quality_score = review.get("quality_score", 0)
            st.metric("Curation Quality Score", f"{quality_score}/10")
        
        st.divider()
        
        st.markdown("<h3>RETRIEVED SOURCES</h3>", unsafe_allow_html=True)
        sources = result.get("sources", [])
        for source in sources:
            st.markdown(f"- [{source}]({source})")
        
        st.divider()
        
        with st.expander("System State (Debug)"):
            st.json(result)


def main():
    """Main application function."""
    init_session_state()
    render_sidebar()
    
    # Main page layout
    st.markdown('<div class="luxury-title">AETHERIS</div>', unsafe_allow_html=True)
    st.markdown('<div class="luxury-subtitle">Autonomous Cognitive Research & Intelligence Engine</div>', unsafe_allow_html=True)
    
    st.divider()
    
    # Question input
    question = st.text_area(
        "SPECIFY RESEARCH INQUIRY",
        height=120,
        placeholder="e.g., What are the latest breakthroughs in nuclear fusion energy and when might commercial fusion power plants be operational?",
        value=st.session_state.get("question", "")
    )
    
    # Buttons
    col1, col2 = st.columns([1, 1])
    
    with col1:
        research_button = st.button("INITIATE INQUIRY", type="primary", use_container_width=True)
    
    with col2:
        clear_button = st.button("RESET", use_container_width=True)
    
    # Clear button handler
    if clear_button:
        st.session_state.research_result = None
        st.session_state.question = ""
        st.session_state.start_time = None
        st.rerun()
    
    # Example questions
    render_example_questions()
    
    # Research button handler
    if research_button:
        if len(question) < 20:
            st.warning("Please enter a more substantive query (minimum 20 characters).")
            return
        
        try:
            # Initialize progress display
            progress_placeholder, status_placeholder = render_progress_placeholder()
            
            # Start timer
            st.session_state.start_time = time.time()
            
            # Run research with progress updates
            with st.spinner("Research execution in progress..."):
                update_progress(progress_placeholder, status_placeholder, "planning", 10, "Formulating strategic inquiry matrix...")
                time.sleep(0.5)
                
                result = run_research(question)
                
                update_progress(progress_placeholder, status_placeholder, "researching", 50, "Retrieving digital knowledge resources...")
                time.sleep(0.3)
                
                update_progress(progress_placeholder, status_placeholder, "reviewing", 80, "Evaluating evidence and resolving gaps...")
                time.sleep(0.3)
                
                update_progress(progress_placeholder, status_placeholder, "synthesizing", 95, "Synthesizing final intelligence report...")
                time.sleep(0.3)
                
                update_progress(progress_placeholder, status_placeholder, "complete", 100, "Inquiry successfully completed.")
                
                # Store result
                st.session_state.research_result = result
                
                # Add to history
                st.session_state.research_history.append({
                    "question": question,
                    "timestamp": datetime.now().isoformat(),
                    "result": result
                })
                
                # Keep only last 5
                if len(st.session_state.research_history) > 5:
                    st.session_state.research_history = st.session_state.research_history[-5:]
                
                # Clear placeholders
                progress_placeholder.empty()
                status_placeholder.empty()
                
                st.success("Curation completed.")
        
        except ValueError as e:
            if "GROQ_API_KEY" in str(e):
                st.error("Authentication Failed: Groq API Key Missing")
                st.markdown("""
                Please configure your Groq API key in the `.env` file:
                
                1. Obtain an API key from [console.groq.com](https://console.groq.com)
                2. Set the key in your local workspace `.env` file:
                   `GROQ_API_KEY=your_key_here`
                """)
            else:
                st.error(f"Execution Error: {str(e)}")
        
        except Exception as e:
            st.error(f"An unexpected error occurred: {str(e)}")
            st.error("Please examine system logs for details.")
    
    # Display previous results
    if st.session_state.research_result:
        st.divider()
        render_results(st.session_state.research_result)


if __name__ == "__main__":
    main()
