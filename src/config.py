# src/config.py - Updated for Deployment
import os

# Hugging Face deploy ke liye environment variable se lein
GROQ_API_KEY = os.getenv("GROQ_API_KEY", "")

# Agar local test karna ho toh environment variable set karein:
# set GROQ_API_KEY=gsk_your_key_here

# Model Settings
LLM_MODEL = "llama-3.1-8b-instant"
EMBEDDING_MODEL = "sentence-transformers/all-MiniLM-L6-v2"

# ChromaDB
CHROMA_PERSIST_DIR = "./data/chroma_db"
COLLECTION_NAME = "rag_collection"

# Retrieval Settings
CHUNK_SIZE = 500
CHUNK_OVERLAP = 50
TOP_K_RETRIEVE = 5
TOP_K_RERANK = 3
