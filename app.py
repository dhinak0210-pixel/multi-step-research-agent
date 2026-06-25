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
    page_title="Multi-Step Research Agent",
    page_icon="🔬",
    layout="wide"
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
        st.header("⚙️ How It Works")
        
        st.markdown("""
        **1. 📋 Planning**
        AI breaks your question into 3-5 sub-questions
        
        **2. 🔍 Research**
        Web search + scraping for each sub-question
        
        **3. 📊 Review**
        Quality check and gap analysis
        
        **4. 📝 Synthesis**
        Comprehensive markdown report generation
        """)
        
        st.divider()
        
        st.subheader("Tech Stack")
        st.markdown("""
        - **LangGraph** - Agent orchestration
        - **LangChain** - LLM chains
        - **Gemini 1.5 Flash** - AI model
        - **DuckDuckGo** - Web search
        - **ChromaDB** - Vector storage
        - **Streamlit** - Web UI
        """)
        
        st.divider()
        
        st.subheader("💡 Tips")
        st.markdown("""
        - Be specific in your question
        - Include context if needed
        - Ask about recent developments
        - Complex questions work best
        """)
        
        st.divider()
        
        st.subheader("🔑 API Key")
        st.markdown("""
        Get your free Groq API key:
        [console.groq.com/keys](https://console.groq.com/keys)
        
        Add it to your `.env` file:
        ```
        GROQ_API_KEY=your_key_here
        ```
        """)


def render_example_questions():
    """Render clickable example questions."""
    st.subheader("💡 Try These Examples")
    
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
            if st.button(example[:50] + "...", key=f"example_{i}", use_container_width=True):
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
    tab1, tab2, tab3 = st.tabs(["📝 Final Report", "🔍 Research Details", "📊 Session Stats"])
    
    # Tab 1: Final Report
    with tab1:
        st.markdown(result.get("report", "No report generated"))
        
        # Download button
        report_text = result.get("report", "")
        st.download_button(
            label="📥 Download Report as Markdown",
            data=report_text,
            file_name=f"research_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.md",
            mime="text/markdown"
        )
        
        # Word count
        word_count = len(report_text.split())
        st.caption(f"📊 Word count: {word_count}")
    
    # Tab 2: Research Details
    with tab2:
        st.subheader("Research Plan")
        st.markdown(f"**Reasoning:** {result.get('plan_reasoning', 'N/A')}")
        
        st.subheader("Sub-Questions")
        for i, sq in enumerate(result.get("sub_questions", []), 1):
            st.markdown(f"{i}. {sq}")
        
        st.divider()
        
        st.subheader("Findings")
        findings = result.get("findings", [])
        for i, finding in enumerate(findings, 1):
            with st.expander(f"Finding {i}: {finding.get('sub_question', 'N/A')}"):
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
            st.metric("Findings", len(result.get("findings", [])))
        
        with col3:
            st.metric("Sources", len(result.get("sources", [])))
        
        with col4:
            st.metric("Loops", result.get("loop_count", 0))
        
        col5, col6 = st.columns(2)
        
        with col5:
            if st.session_state.start_time:
                elapsed = time.time() - st.session_state.start_time
                st.metric("Time Elapsed", f"{elapsed:.1f}s")
        
        with col6:
            review = result.get("review", {})
            quality_score = review.get("quality_score", 0)
            st.metric("Quality Score", f"{quality_score}/10")
        
        st.divider()
        
        st.subheader("Sources Visited")
        sources = result.get("sources", [])
        for source in sources:
            st.markdown(f"- [{source}]({source})")
        
        st.divider()
        
        with st.expander("🔧 Full State (Debug)"):
            import json
            st.json(result)


def main():
    """Main application function."""
    init_session_state()
    render_sidebar()
    
    # Main page
    st.title("🔬 Multi-Step Research Agent")
    st.markdown("AI-powered autonomous research with web search, scraping, and synthesis")
    
    st.divider()
    
    # Question input
    question = st.text_area(
        "Enter your research question:",
        height=120,
        placeholder="e.g., What are the latest breakthroughs in nuclear fusion energy and when might commercial fusion power plants be operational?",
        value=st.session_state.get("question", "")
    )
    
    # Buttons
    col1, col2 = st.columns([1, 1])
    
    with col1:
        research_button = st.button("🔬 Start Research", type="primary", use_container_width=True)
    
    with col2:
        clear_button = st.button("🗑️ Clear", use_container_width=True)
    
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
            st.warning("⚠️ Please enter a more detailed question (at least 20 characters)")
            return
        
        try:
            # Initialize progress display
            progress_placeholder, status_placeholder = render_progress_placeholder()
            
            # Start timer
            st.session_state.start_time = time.time()
            
            # Run research with progress updates
            with st.spinner("Research in progress..."):
                update_progress(progress_placeholder, status_placeholder, "planning", 10, "📋 Planning research strategy...")
                time.sleep(0.5)
                
                result = run_research(question)
                
                update_progress(progress_placeholder, status_placeholder, "researching", 50, "🔍 Searching the web...")
                time.sleep(0.3)
                
                update_progress(progress_placeholder, status_placeholder, "reviewing", 80, "📊 Reviewing findings...")
                time.sleep(0.3)
                
                update_progress(progress_placeholder, status_placeholder, "synthesizing", 95, "📝 Writing report...")
                time.sleep(0.3)
                
                update_progress(progress_placeholder, status_placeholder, "complete", 100, "✅ Complete!")
                
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
                
                st.success("✅ Research completed successfully!")
        
        except ValueError as e:
            if "GOOGLE_API_KEY" in str(e):
                st.error("❌ API Key Missing")
                st.markdown("""
                Please set your Google Gemini API key in the `.env` file:
                
                1. Get a free key at: [aistudio.google.com/apikey](https://aistudio.google.com/apikey)
                2. Create a `.env` file in the project directory
                3. Add: `GOOGLE_API_KEY=your_key_here`
                """)
            else:
                st.error(f"❌ Error: {str(e)}")
        
        except Exception as e:
            st.error(f"❌ An error occurred: {str(e)}")
            st.error("Please check the logs for more details.")
    
    # Display previous results
    if st.session_state.research_result:
        st.divider()
        render_results(st.session_state.research_result)


if __name__ == "__main__":
    main()
