# 🔬 Multi-Step Research Agent

An autonomous AI-powered research agent that breaks down complex questions, searches the web, scrapes content, and synthesizes comprehensive reports using LangGraph orchestration.

![Screenshot Placeholder](screenshot.png)

## 🎯 Features

- **Autonomous Research Loop**: Uses LangGraph state machine for fully autonomous multi-step research
- **Intelligent Planning**: AI breaks complex questions into 3-5 searchable sub-questions
- **Web Search & Scraping**: DuckDuckGo search with BeautifulSoup content extraction
- **Vector Storage**: ChromaDB with sentence-transformers for semantic retrieval
- **Quality Review**: Automated quality scoring and gap analysis with iterative refinement
- **Report Synthesis**: Professional markdown reports with citations and structured sections
- **Beautiful UI**: Clean Streamlit interface with progress tracking and downloadable reports

## 🏗️ Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                     STREAMLIT UI                              │
└────────────────────────┬────────────────────────────────────┘
                         │
                         ▼
┌─────────────────────────────────────────────────────────────┐
│                   LANGGRAPH ORCHESTRATOR                      │
│  ┌──────────┐    ┌──────────┐    ┌──────────┐    ┌───────┐ │
│  │ PLANNER  │───▶│RESEARCHER│───▶│ REVIEWER │───▶│SYNTH  │ │
│  └──────────┘    └────┬─────┘    └────┬─────┘    └───────┘ │
│                      │ Loop back      │ Loop back          │
│                      └────────────────┘                    │
└─────────────────────────────────────────────────────────────┘
                         │
         ┌───────────────┼───────────────┐
         ▼               ▼               ▼
    ┌─────────┐    ┌─────────┐    ┌─────────┐
    │  SEARCH │    │ SCRAPE  │    │ CHROMA  │
    │  TOOL   │    │  TOOL   │    │    DB   │
    └─────────┘    └─────────┘    └─────────┘
         │               │               │
         └───────────────┴───────────────┘
                         │
                         ▼
                    ┌─────────┐
                    │ GEMINI  │
                    │   LLM   │
                    └─────────┘
```

## 🚀 Quick Start

### 1. Clone or Download

```bash
cd /home/dhina/CascadeProjects/multi-step-research-agent
```

### 2. Get Free Gemini API Key

Visit [aistudio.google.com/apikey](https://aistudio.google.com/apikey) and get your free API key.

### 3. Configure Environment

```bash
cp .env.example .env
```

Edit `.env` and add your API key:

```
GOOGLE_API_KEY=your_actual_api_key_here
```

### 4. Install Dependencies

```bash
pip install -r requirements.txt
```

### 5. Run the Application

```bash
streamlit run app.py
```

The app will open at `http://localhost:8501`

## 📁 Project Structure

```
multi-step-research-agent/
├── .env                          # API key configuration
├── .env.example                  # Environment template
├── .gitignore                    # Git ignore rules
├── requirements.txt              # Python dependencies
├── README.md                     # This file
├── config.py                     # Configuration constants
├── app.py                        # Streamlit UI (main entry)
│
├── agents/                       # LangGraph agent nodes
│   ├── __init__.py
│   ├── orchestrator.py           # State machine builder
│   ├── planner.py                # Research planning
│   ├── researcher.py             # Web search + scrape
│   ├── reviewer.py               # Quality review
│   └── synthesizer.py           # Report generation
│
├── tools/                        # External tool wrappers
│   ├── __init__.py
│   ├── search_tool.py            # DuckDuckGo search
│   ├── scraper_tool.py           # Web scraping
│   └── vectorstore_tool.py       # ChromaDB operations
│
├── models/                       # LLM initialization
│   ├── __init__.py
│   └── llm.py                    # Gemini LLM setup
│
├── prompts/                      # System prompts
│   ├── __init__.py
│   ├── planner_prompt.py         # Planning prompt
│   ├── researcher_prompt.py      # Research analysis prompt
│   ├── reviewer_prompt.py        # Quality review prompt
│   └── synthesizer_prompt.py     # Report generation prompt
│
└── utils/                        # Utilities
    ├── __init__.py
    ├── logger.py                 # Logging setup
    └── helpers.py               # Helper functions
```

## 🔄 How It Works

### Step 1: Planning
The AI planner analyzes your question and breaks it into 3-5 specific, searchable sub-questions ordered logically (fundamentals → specifics).

### Step 2: Research
For each sub-question:
- Searches DuckDuckGo for relevant results
- Scrapes top 3 URLs with BeautifulSoup
- Chunks content and stores in ChromaDB
- Extracts key findings using Gemini LLM

### Step 3: Review
The AI reviewer evaluates:
- Research coverage and completeness
- Quality score (1-10)
- Information gaps
- Whether additional research is needed

If quality score < 7 and loops < 3, it adds new search queries and loops back.

### Step 4: Synthesis
The AI synthesizer:
- Queries ChromaDB for relevant context
- Combines all findings with vector context
- Generates professional markdown report with:
  - Executive Summary
  - Background & Context
  - Key Findings
  - Detailed Analysis
  - Conflicting Views & Limitations
  - Conclusion & Direct Answer
  - Further Research Suggestions
  - Sources & References

## 🛠️ Tech Stack

- **Python 3.11+** - Core language
- **LangGraph** - Agent state machine orchestration
- **LangChain** - LLM chains and tool wrappers
- **Google Gemini 1.5 Flash** - AI model (free tier)
- **DuckDuckGo Search** - Web search (no API key needed)
- **BeautifulSoup4** - HTML parsing
- **ChromaDB** - Local vector database
- **sentence-transformers** - Local embeddings (all-MiniLM-L6-v2)
- **Streamlit** - Web UI framework

## ❓ FAQ

**Q: Is this really free?**
A: Yes! Uses Gemini 1.5 Flash free tier, DuckDuckGo (no API key), and local ChromaDB. No paid services required.

**Q: How long does research take?**
A: Typically 2-5 minutes depending on question complexity and network speed.

**Q: Can I use a different LLM?**
A: Currently configured for Gemini 1.5 Flash. You can modify `models/llm.py` to use other LangChain-supported models.

**Q: Where is data stored?**
A: ChromaDB runs in-memory by default. Data is not persisted between sessions.

**Q: Can I customize the prompts?**
A: Yes! All prompts are in the `prompts/` directory and can be modified to change behavior.

**Q: What if the API rate limits?**
A: The agent includes built-in delays (1s between searches, 0.5s between scrapes) to avoid rate limiting.

## 🤝 Contributing

Contributions are welcome! Areas for improvement:
- Additional LLM provider support
- Persistent vector storage options
- More sophisticated review criteria
- Export to PDF/Word formats
- Research history persistence
- Multi-language support

## 📝 License

This project is provided as-is for educational and research purposes.

## 🐛 Troubleshooting

**API Key Error:**
- Ensure `.env` file exists in project root
- Verify `GOOGLE_API_KEY` is set correctly
- Check your key is valid at [aistudio.google.com](https://aistudio.google.com)

**Import Errors:**
- Ensure all dependencies are installed: `pip install -r requirements.txt`
- Check Python version is 3.11+

**Search Fails:**
- Check internet connection
- DuckDuckGo may temporarily block requests - wait and retry

**Scraping Fails:**
- Some websites block scrapers
- The agent handles failures gracefully and continues

**Report Quality:**
- Try more specific questions
- The agent learns and improves with each iteration
- Check the "Research Details" tab to see intermediate findings

## 📞 Support

For issues or questions, please check the troubleshooting section above or review the code comments.
