# src/embeddings.py
import os
from pathlib import Path

from langchain_huggingface import HuggingFaceEmbeddings
from src.config import EMBEDDING_MODEL

HF_CACHE_DIR = Path(__file__).resolve().parents[1] / "data" / "hf_cache"
os.environ.setdefault("HF_HOME", str(HF_CACHE_DIR))
os.environ.setdefault("SENTENCE_TRANSFORMERS_HOME", str(HF_CACHE_DIR))

def get_embeddings():
    """
    FREE Hugging Face embeddings model
    """
    HF_CACHE_DIR.mkdir(parents=True, exist_ok=True)

    embeddings = HuggingFaceEmbeddings(
        model_name=EMBEDDING_MODEL,
        cache_folder=str(HF_CACHE_DIR),
        model_kwargs={'device': 'cpu'},
        encode_kwargs={'normalize_embeddings': True}
    )
    print(f"Loaded embedding model: {EMBEDDING_MODEL}")
    return embeddings

if __name__ == "__main__":
    emb = get_embeddings()
    test_text = "This is a test sentence"
    vector = emb.embed_query(test_text)
    print(f"Embedding dimension: {len(vector)}")