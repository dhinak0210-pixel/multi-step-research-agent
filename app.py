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
    @import url('https://fonts.googleapis.com/css2?family=Cinzel:wght@400;500;600;700;800&family=Inter:wght@300;400;500;600;700&family=Playfair+Display:ital,wght@0,400;0,500;0,600;1,400&display=swap');

    /* Main App Background & Text */
    .stApp {
        background-color: #0a0a0c !important;
        color: #e4e4e7 !important;
        font-family: 'Inter', sans-serif !important;
    }

    /* Scrollbars */
    ::-webkit-scrollbar {
        width: 5px;
        height: 5px;
    }
    ::-webkit-scrollbar-track {
        background: #0a0a0c !important;
    }
    ::-webkit-scrollbar-thumb {
        background: #c5a880 !important;
        border-radius: 4px !important;
    }
    ::-webkit-scrollbar-thumb:hover {
        background: #e5c59e !important;
    }

    /* Sidebar Background and Border */
    [data-testid="stSidebar"] {
        background-color: #060608 !important;
        border-right: 1px solid #1a1a22 !important;
        padding-top: 2rem !important;
    }

    /* Headers & Fonts */
    h1, h2, h3, h4, h5, h6 {
        font-family: 'Cinzel', serif !important;
        color: #c5a880 !important;
        font-weight: 500 !important;
        letter-spacing: 0.1em !important;
    }

    /* Luxury Metallic Title with Soft Pulsing Glow */
    .luxury-title {
        font-family: 'Cinzel', serif !important;
        font-size: 3.5rem !important;
        font-weight: 800 !important;
        letter-spacing: 0.25em !important;
        background: linear-gradient(135deg, #f5e5c9 0%, #c5a880 50%, #9e7f56 100%) !important;
        -webkit-background-clip: text !important;
        -webkit-text-fill-color: transparent !important;
        text-align: center !important;
        margin-top: 2.5rem !important;
        margin-bottom: 0.4rem !important;
        text-transform: uppercase !important;
        animation: goldGlow 4s infinite alternate !important;
    }

    @keyframes goldGlow {
        0% { filter: drop-shadow(0 0 4px rgba(197, 168, 128, 0.1)); }
        100% { filter: drop-shadow(0 0 16px rgba(197, 168, 128, 0.3)); }
    }

    .luxury-subtitle {
        font-family: 'Playfair Display', serif !important;
        font-style: italic !important;
        font-size: 1.1rem !important;
        color: #a1a1aa !important;
        text-align: center !important;
        margin-bottom: 3.5rem !important;
        letter-spacing: 0.08em !important;
    }

    /* Input Card Container Effect */
    div[data-testid="element-container"]:has(textarea) {
        background-color: rgba(15, 15, 18, 0.7) !important;
        border: 1px solid rgba(197, 168, 128, 0.15) !important;
        padding: 1.5rem !important;
        border-radius: 4px !important;
        box-shadow: 0 8px 32px rgba(0, 0, 0, 0.5) !important;
        backdrop-filter: blur(12px) !important;
    }

    textarea {
        background-color: #0d0d10 !important;
        color: #f4f4f5 !important;
        border: 1px solid rgba(197, 168, 128, 0.1) !important;
        border-radius: 2px !important;
        font-family: 'Inter', sans-serif !important;
        font-size: 0.95rem !important;
        transition: all 0.3s ease !important;
        padding: 1rem !important;
        box-shadow: inset 0 2px 4px rgba(0, 0, 0, 0.6) !important;
    }

    textarea:focus {
        border-color: #c5a880 !important;
        box-shadow: 0 0 8px rgba(197, 168, 128, 0.25) !important;
    }

    /* Unified Button Styling & Transitions */
    div.stButton > button {
        font-family: 'Inter', sans-serif !important;
        font-weight: 500 !important;
        letter-spacing: 0.15em !important;
        text-transform: uppercase !important;
        font-size: 0.8rem !important;
        transition: all 0.3s cubic-bezier(0.25, 0.8, 0.25, 1) !important;
        border-radius: 2px !important;
        width: 100% !important;
        padding: 0.75rem 1.8rem !important;
        margin-bottom: 1rem !important;
    }

    /* Primary Button Style (Initiate Inquiry) */
    button[data-testid="stBaseButton-primary"] {
        background: linear-gradient(135deg, #f5e5c9 0%, #c5a880 100%) !important;
        color: #0a0a0c !important;
        border: none !important;
        font-weight: 600 !important;
        box-shadow: 0 4px 15px rgba(197, 168, 128, 0.2) !important;
    }

    button[data-testid="stBaseButton-primary"]:hover {
        background: linear-gradient(135deg, #ffffff 0%, #c5a880 100%) !important;
        box-shadow: 0 6px 20px rgba(197, 168, 128, 0.4) !important;
        transform: translateY(-2px) !important;
    }

    /* Secondary Button Style (Reset, Example Cards) */
    button[data-testid="stBaseButton-secondary"] {
        background-color: rgba(15, 15, 18, 0.5) !important;
        color: #c5a880 !important;
        border: 1px solid rgba(197, 168, 128, 0.25) !important;
        backdrop-filter: blur(5px) !important;
    }

    button[data-testid="stBaseButton-secondary"]:hover {
        color: #0a0a0c !important;
        background-color: #c5a880 !important;
        border-color: #c5a880 !important;
        box-shadow: 0 6px 15px rgba(197, 168, 128, 0.3) !important;
        transform: translateY(-2px) !important;
    }

    /* Tabs Layout Styling */
    button[data-baseweb="tab"] {
        font-family: 'Cinzel', serif !important;
        color: #71717a !important;
        font-size: 0.9rem !important;
        letter-spacing: 0.15em !important;
        padding: 1rem 2rem !important;
        border-bottom: 2px solid transparent !important;
        transition: all 0.3s ease !important;
        background-color: transparent !important;
    }

    button[data-baseweb="tab"]:hover {
        color: #c5a880 !important;
    }

    button[data-baseweb="tab"][aria-selected="true"] {
        color: #c5a880 !important;
        border-bottom: 2px solid #c5a880 !important;
    }

    /* Metrics Styling */
    div[data-testid="stMetric"] {
        background-color: #0f0f12 !important;
        border: 1px solid #1a1a22 !important;
        padding: 1.2rem 1.5rem !important;
        border-radius: 4px !important;
        box-shadow: 0 4px 20px rgba(0,0,0,0.2) !important;
        transition: all 0.3s ease !important;
    }

    div[data-testid="stMetric"]:hover {
        border-color: rgba(197, 168, 128, 0.3) !important;
        transform: translateY(-2px) !important;
    }

    div[data-testid="stMetricValue"] {
        font-family: 'Cinzel', serif !important;
        color: #c5a880 !important;
        font-size: 2rem !important;
    }

    div[data-testid="stMetricLabel"] {
        font-family: 'Inter', sans-serif !important;
        color: #71717a !important;
        letter-spacing: 0.1em !important;
        text-transform: uppercase !important;
        font-size: 0.75rem !important;
    }

    /* Expanders Styling */
    div[data-testid="stExpander"] {
        background-color: #0f0f12 !important;
        border: 1px solid #1a1a22 !important;
        border-radius: 4px !important;
        box-shadow: 0 4px 12px rgba(0,0,0,0.1) !important;
    }

    /* Elegant Sidebar Timeline Methodology */
    .sidebar-timeline {
        position: relative;
        padding-left: 1.5rem;
        border-left: 1px solid rgba(197, 168, 128, 0.15);
        margin-left: 0.5rem;
        margin-top: 1.5rem;
    }

    .timeline-node {
        position: absolute;
        left: -4px;
        top: 6px;
        width: 7px;
        height: 7px;
        border-radius: 50%;
        background-color: #c5a880;
        box-shadow: 0 0 8px #c5a880;
    }

    .step-num {
        font-family: 'Cinzel', serif;
        color: #c5a880;
        font-size: 1.05rem;
        font-weight: 600;
        margin-right: 0.5rem;
    }

    /* Divider & Borders styling */
    hr {
        border-color: rgba(197, 168, 128, 0.12) !important;
        margin: 2rem 0 !important;
    }

    /* Alerts Box overrides */
    div.stAlert {
        background-color: #0f0f12 !important;
        border: 1px solid rgba(197, 168, 128, 0.15) !important;
        color: #e4e4e7 !important;
        border-radius: 4px !important;
    }

    div.stAlert > div {
        color: #e4e4e7 !important;
    }

    /* Hide default Streamlit overlays */
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
        st.markdown("<h3 style='margin-bottom: 0.5rem;'>METHODOLOGY</h3>", unsafe_allow_html=True)
        
        st.markdown("""
        <div class="sidebar-timeline">
            <div style="position: relative; margin-bottom: 1.8rem;">
                <div class="timeline-node"></div>
                <span class="step-num">01</span> <strong style="color: #f4f4f5; font-size: 0.9rem; letter-spacing: 0.05em;">DECOMPOSITION</strong>
                <div style="color: #8a8a93; font-size: 0.78rem; margin-top: 0.3rem; line-height: 1.4;">
                    AI orchestrator plans and breaks down the core question into targeted sub-questions.
                </div>
            </div>
            <div style="position: relative; margin-bottom: 1.8rem;">
                <div class="timeline-node"></div>
                <span class="step-num">02</span> <strong style="color: #f4f4f5; font-size: 0.9rem; letter-spacing: 0.05em;">ACQUISITION</strong>
                <div style="color: #8a8a93; font-size: 0.78rem; margin-top: 0.3rem; line-height: 1.4;">
                    Parallel web scraping, search queries, and real-time vector database ingestion.
                </div>
            </div>
            <div style="position: relative; margin-bottom: 1.8rem;">
                <div class="timeline-node"></div>
                <span class="step-num">03</span> <strong style="color: #f4f4f5; font-size: 0.9rem; letter-spacing: 0.05em;">EVALUATION</strong>
                <div style="color: #8a8a93; font-size: 0.78rem; margin-top: 0.3rem; line-height: 1.4;">
                    Automated quality loops scoring details and launching follow-up gap sweeps.
                </div>
            </div>
            <div style="position: relative; margin-bottom: 0;">
                <div class="timeline-node"></div>
                <span class="step-num">04</span> <strong style="color: #f4f4f5; font-size: 0.9rem; letter-spacing: 0.05em;">CURATION</strong>
                <div style="color: #8a8a93; font-size: 0.78rem; margin-top: 0.3rem; line-height: 1.4;">
                    Synthesis of a professional markdown intelligence dossier with citation tracing.
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)
        
        st.divider()
        
        st.markdown("<h3>TECHNOLOGY STACK</h3>", unsafe_allow_html=True)
        st.markdown("""
        <div style="font-size: 0.82rem; color: #a1a1aa; line-height: 1.7; padding-left: 0.5rem;">
            • LangGraph Stateful Workflows<br>
            • LangChain Integration Layer<br>
            • Llama 3.3 (Groq API)<br>
            • DuckDuckGo Scraper<br>
            • ChromaDB Vector Storage<br>
            • Streamlit Client Node
        </div>
        """, unsafe_allow_html=True)
        
        st.divider()
        
        st.markdown("<h3>CREDENTIALS</h3>", unsafe_allow_html=True)
        st.markdown("""
        <div style="font-size: 0.82rem; color: #a1a1aa; line-height: 1.5; margin-bottom: 1rem; padding-left: 0.5rem;">
            Configure your Groq API key in your <code>.env</code> file:
        </div>
        <pre style="background-color: #0f0f12; border: 1px solid #1a1a22; padding: 0.6rem; color: #c5a880; font-size: 0.78rem; border-radius: 3px;">GROQ_API_KEY=your_key_here</pre>
        """, unsafe_allow_html=True)


def render_example_questions():
    """Render clickable example questions."""
    st.markdown("<h3 style='text-align: center; margin-top: 3rem; margin-bottom: 1.5rem; letter-spacing: 0.15em;'>SUGGESTED RESEARCH TOPICS</h3>", unsafe_allow_html=True)
    
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
