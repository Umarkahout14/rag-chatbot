# src/retriever.py
from langchain.retrievers import EnsembleRetriever
from langchain_community.retrievers import BM25Retriever
from src.config import TOP_K_RETRIEVE

class HybridRetriever:
    def __init__(self, vectorstore, documents):
        """
        BM25 + Vector Search = Better Recall
        """
        self.vector_retriever = vectorstore.as_retriever(
            search_type="similarity",
            search_kwargs={"k": TOP_K_RETRIEVE}
        )

        self.bm25_retriever = BM25Retriever.from_documents(
            documents,
            k=TOP_K_RETRIEVE
        )

        self.ensemble_retriever = EnsembleRetriever(
            retrievers=[self.bm25_retriever, self.vector_retriever],
            weights=[0.5, 0.5]
        )

        print("Hybrid Retriever ready (BM25 + Vector)")

    def retrieve(self, query: str):
        """Hybrid search se documents retrieve karein"""
        docs = self.ensemble_retriever.invoke(query)
        return docs
