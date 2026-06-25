"""
Web scraping tool for Multi-Step Research Agent.
Extracts and chunks text content from web pages.
"""

import time
import requests
from bs4 import BeautifulSoup
from langchain_text_splitters import RecursiveCharacterTextSplitter
from config import MAX_CONTENT_LENGTH, CHUNK_SIZE, CHUNK_OVERLAP
from utils.logger import log


def scrape_url(url: str) -> str:
    """
    Scrape text content from a URL.
    
    Args:
        url: URL to scrape
    
    Returns:
        Extracted text content (limited to MAX_CONTENT_LENGTH)
        Returns error message string on failure
    """
    log.info(f"📥 Scraping: {url}")
    
    try:
        # Add delay to avoid rate limiting
        time.sleep(0.5)
        
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
        }
        
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()
        
        soup = BeautifulSoup(response.content, "lxml")
        
        # Remove unwanted elements
        for element in soup(["script", "style", "nav", "footer", "header", "aside", "iframe"]):
            element.decompose()
        
        # Extract text
        text = soup.get_text(separator=" ", strip=True)
        
        # Clean up whitespace
        text = " ".join(text.split())
        
        # Limit length
        if len(text) > MAX_CONTENT_LENGTH:
            text = text[:MAX_CONTENT_LENGTH]
            log.info(f"⚠️ Content truncated to {MAX_CONTENT_LENGTH} characters")
        
        log.info(f"✅ Scraped {len(text)} characters from {url}")
        return text
        
    except requests.exceptions.Timeout:
        log.error(f"❌ Timeout while scraping: {url}")
        return f"Error: Timeout while scraping {url}"
    except requests.exceptions.RequestException as e:
        log.error(f"❌ Request failed for {url}: {e}")
        return f"Error: Failed to scrape {url} - {str(e)}"
    except Exception as e:
        log.error(f"❌ Unexpected error scraping {url}: {e}")
        return f"Error: Unexpected error scraping {url} - {str(e)}"


def chunk_text(text: str) -> list[str]:
    """
    Split text into chunks for vector storage.
    
    Args:
        text: Text to chunk
    
    Returns:
        List of text chunks
    """
    if not text or text.startswith("Error:"):
        return []
    
    try:
        text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=CHUNK_SIZE,
            chunk_overlap=CHUNK_OVERLAP,
            length_function=len,
            separators=["\n\n", "\n", ". ", " ", ""]
        )
        
        chunks = text_splitter.split_text(text)
        log.info(f"📝 Split text into {len(chunks)} chunks")
        return chunks
        
    except Exception as e:
        log.error(f"❌ Error chunking text: {e}")
        return []
