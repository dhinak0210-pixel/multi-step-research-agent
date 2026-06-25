"""
Vector database tool for Multi-Step Research Agent.
Manages ChromaDB collection for storing and retrieving text chunks.
"""

import chromadb
from chromadb.utils import embedding_functions
from config import COLLECTION_NAME
from utils.helpers import generate_id, format_timestamp
from utils.logger import log


# Initialize ChromaDB client (in-memory)
client = chromadb.Client()

# Initialize embedding function
embedding_function = embedding_functions.SentenceTransformerEmbeddingFunction(
    model_name="all-MiniLM-L6-v2"
)


def get_or_create_collection():
    """
    Get or create the ChromaDB collection.
    
    Returns:
        ChromaDB collection object
    """
    try:
        # Try to get existing collection
        collection = client.get_collection(
            name=COLLECTION_NAME,
            embedding_function=embedding_function
        )
        log.info(f"📚 Retrieved existing collection: {COLLECTION_NAME}")
        return collection
    except:
        # Create new collection if it doesn't exist
        collection = client.create_collection(
            name=COLLECTION_NAME,
            embedding_function=embedding_function
        )
        log.info(f"📚 Created new collection: {COLLECTION_NAME}")
        return collection


def store_chunks(chunks: list[str], source_url: str, sub_question: str) -> int:
    """
    Store text chunks in the vector database.
    
    Args:
        chunks: List of text chunks to store
        source_url: URL where chunks were scraped from
        sub_question: Research question these chunks address
    
    Returns:
        Number of chunks stored
    """
    if not chunks:
        return 0
    
    collection = get_or_create_collection()
    
    ids = []
    documents = []
    metadatas = []
    
    for i, chunk in enumerate(chunks):
        chunk_id = generate_id(source_url, i)
        ids.append(chunk_id)
        documents.append(chunk)
        metadatas.append({
            "source_url": source_url,
            "sub_question": sub_question,
            "timestamp": format_timestamp(),
            "chunk_index": i
        })
    
    try:
        collection.add(
            ids=ids,
            documents=documents,
            metadatas=metadatas
        )
        log.info(f"💾 Stored {len(chunks)} chunks from {source_url}")
        return len(chunks)
    except Exception as e:
        # Skip duplicates silently
        if "already exists" in str(e).lower():
            log.info(f"⏭️ Skipping duplicate chunks from {source_url}")
            return 0
        log.error(f"❌ Error storing chunks: {e}")
        return 0


def query_collection(query: str, n_results: int = 10) -> dict:
    """
    Query the vector database for relevant chunks.
    
    Args:
        query: Query string
        n_results: Number of results to return
    
    Returns:
        Dictionary with query results (empty if collection is empty)
    """
    try:
        collection = get_or_create_collection()
        count = collection.count()
        
        if count == 0:
            log.warning("⚠️ Collection is empty, no results to return")
            return {"documents": [[]], "metadatas": [[]]}
        
        results = collection.query(
            query_texts=[query],
            n_results=min(n_results, count)
        )
        
        log.info(f"🔎 Retrieved {len(results['documents'][0])} relevant chunks")
        return results
        
    except Exception as e:
        log.error(f"❌ Error querying collection: {e}")
        return {"documents": [[]], "metadatas": [[]]}


def clear_collection() -> None:
    """
    Clear all data from the collection.
    """
    try:
        client.delete_collection(name=COLLECTION_NAME)
        log.info(f"🗑️ Cleared collection: {COLLECTION_NAME}")
    except Exception as e:
        log.warning(f"⚠️ Error clearing collection: {e}")


def get_collection_count() -> int:
    """
    Get the number of documents in the collection.
    
    Returns:
        Number of documents
    """
    try:
        collection = get_or_create_collection()
        return collection.count()
    except:
        return 0
