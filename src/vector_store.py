# src/vector_store.py
from langchain_community.vectorstores import Chroma
from src.embeddings import get_embeddings
from src.config import CHROMA_PERSIST_DIR, COLLECTION_NAME
import os

def create_vector_store(chunks, collection_name=COLLECTION_NAME):
    """
    ChromaDB mein vectors store karein
    """
    # Ensure directory exists
    os.makedirs(CHROMA_PERSIST_DIR, exist_ok=True)

    embeddings = get_embeddings()

    vectorstore = Chroma.from_documents(
        documents=chunks,
        embedding=embeddings,
        persist_directory=CHROMA_PERSIST_DIR,
        collection_name=collection_name
    )

    # Persist to disk
    vectorstore.persist()

    print(f"Stored {len(chunks)} chunks in ChromaDB at {CHROMA_PERSIST_DIR}")
    return vectorstore

def load_vector_store(collection_name=COLLECTION_NAME):
    """
    Pehle se bani hui vector store load karein
    """
    embeddings = get_embeddings()

    vectorstore = Chroma(
        persist_directory=CHROMA_PERSIST_DIR,
        embedding_function=embeddings,
        collection_name=collection_name
    )

    print(f"Loaded existing vector store from {CHROMA_PERSIST_DIR}")
    return vectorstore

# Test
if __name__ == "__main__":
    from src.document_loader import load_documents
    from src.chunker import chunk_documents

    docs = load_documents("data/sample_docs")
    if docs:
        chunks = chunk_documents(docs)
        vs = create_vector_store(chunks)
    else:
        print("No documents found. Add PDFs to data/sample_docs/")
