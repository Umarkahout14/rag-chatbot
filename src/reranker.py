# src/reranker.py
import os
from pathlib import Path

from sentence_transformers import CrossEncoder
from src.config import TOP_K_RERANK

HF_CACHE_DIR = Path(__file__).resolve().parents[1] / "data" / "hf_cache"
os.environ.setdefault("HF_HOME", str(HF_CACHE_DIR))
os.environ.setdefault("SENTENCE_TRANSFORMERS_HOME", str(HF_CACHE_DIR))
os.environ.setdefault("TRANSFORMERS_CACHE", str(HF_CACHE_DIR))

class Reranker:
    def __init__(self):
        """
        Cross-encoder se results rerank karein
        """
        HF_CACHE_DIR.mkdir(parents=True, exist_ok=True)
        cache_dir = str(HF_CACHE_DIR)
        self.model = CrossEncoder(
            "cross-encoder/ms-marco-MiniLM-L-6-v2",
            max_length=512,
            tokenizer_args={"cache_dir": cache_dir},
            automodel_args={"cache_dir": cache_dir}
        )
        print("Cross-encoder reranker loaded")

    def rerank(self, query: str, documents: list, top_k: int = None):
        """
        Documents ko query ke hisaab se rerank karein
        """
        if top_k is None:
            top_k = TOP_K_RERANK

        if not documents:
            return []

        pairs = [[query, doc.page_content] for doc in documents]
        scores = self.model.predict(pairs)
        scored_docs = list(zip(documents, scores))
        scored_docs.sort(key=lambda x: x[1], reverse=True)
        return [doc for doc, _ in scored_docs[:top_k]]
