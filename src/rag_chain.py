# src/rag_chain.py
from src.vector_store import load_vector_store, create_vector_store
from src.llm_client import GroqLLM
from src.retriever import HybridRetriever
from src.reranker import Reranker
from src.config import TOP_K_RETRIEVE, TOP_K_RERANK

class RAGChatbot:
    def __init__(self):
        print("Initializing Advanced RAG Chatbot...")

        self.vectorstore = load_vector_store()
        self.all_docs = self.vectorstore.get()

        from langchain.schema import Document
        documents = []
        if self.all_docs and "documents" in self.all_docs:
            for i, doc_text in enumerate(self.all_docs["documents"]):
                if doc_text:
                    metadata = self.all_docs["metadatas"][i] if self.all_docs["metadatas"] else {}
                    documents.append(Document(page_content=doc_text, metadata=metadata))

        if documents:
            self.hybrid_retriever = HybridRetriever(self.vectorstore, documents)
        else:
            self.hybrid_retriever = None

        self.reranker = Reranker()
        self.llm = GroqLLM()

        print("Advanced RAG Chatbot ready!")

    def ask(self, question: str, chat_history: list = None) -> dict:
        """
        Complete RAG pipeline: Hybrid Retrieve -> Rerank -> Generate
        """
        if not self.hybrid_retriever:
            return {
                "answer": "No documents found. Please upload some PDFs or TXT files first!",
                "sources": [],
                "num_sources": 0,
                "retrieval_method": "none"
            }

        docs = self.hybrid_retriever.retrieve(question)
        reranked_docs = self.reranker.rerank(question, docs)

        context_parts = []
        sources = []
        for i, doc in enumerate(reranked_docs, 1):
            context_parts.append(f"[Source {i}]: {doc.page_content}")
            sources.append({
                "number": i,
                "source": doc.metadata.get("source", "Unknown"),
                "page": doc.metadata.get("page", "N/A"),
                "content_preview": doc.page_content[:150] + "..."
            })

        context = "\n\n".join(context_parts)

        answer = self.llm.generate(
            prompt=question,
            context=context,
            chat_history=chat_history
        )

        return {
            "answer": answer,
            "sources": sources,
            "num_sources": len(reranked_docs),
            "retrieval_method": "hybrid + rerank"
        }

    def add_documents(self, file_path: str):
        """
        Naye documents add karein
        """
        from src.document_loader import load_documents
        from src.chunker import chunk_documents

        docs = load_documents(file_path)
        if docs:
            chunks = chunk_documents(docs)
            self.vectorstore.add_documents(chunks)
            self.vectorstore.persist()

            all_docs = self.vectorstore.get()
            from langchain.schema import Document
            documents = []
            if all_docs and "documents" in all_docs:
                for i, doc_text in enumerate(all_docs["documents"]):
                    if doc_text:
                        metadata = all_docs["metadatas"][i] if all_docs["metadatas"] else {}
                        documents.append(Document(page_content=doc_text, metadata=metadata))

            if documents:
                self.hybrid_retriever = HybridRetriever(self.vectorstore, documents)

            print(f"Added {len(chunks)} new chunks")
            return True
        return False
