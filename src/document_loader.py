# src/document_loader.py
from langchain_community.document_loaders import PyPDFLoader, TextLoader
from langchain.schema import Document
import os

def load_documents(source_path: str):
    """
    PDF, TXT, ya folder se documents load karein
    """
    documents = []

    if os.path.isdir(source_path):
        # Folder mein sab files process karein
        for filename in os.listdir(source_path):
            file_path = os.path.join(source_path, filename)
            docs = _load_single_file(file_path)
            documents.extend(docs)
    else:
        # Single file
        documents = _load_single_file(source_path)

    print(f"Loaded {len(documents)} documents from {source_path}")
    return documents

def _load_single_file(file_path: str):
    """Single file ko load karein based on extension"""
    if file_path.endswith('.pdf'):
        loader = PyPDFLoader(file_path)
        return loader.load()
    elif file_path.endswith('.txt'):
        loader = TextLoader(file_path, encoding='utf-8')
        return loader.load()
    else:
        print(f"Skipping unsupported file: {file_path}")
        return []

# Test ke liye
if __name__ == "__main__":
    # Test with a sample - pehle koi PDF/Txt daalein data/sample_docs/ mein
    pass
