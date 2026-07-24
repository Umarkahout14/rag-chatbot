# src/chunker.py
from langchain.text_splitter import RecursiveCharacterTextSplitter
from src.config import CHUNK_SIZE, CHUNK_OVERLAP

def chunk_documents(documents):
    """
    Documents ko chote chunks mein split karein
    """
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=CHUNK_SIZE,
        chunk_overlap=CHUNK_OVERLAP,
        separators=["\n\n", "\n", ". ", "! ", "? ", " ", ""],
        length_function=len
    )

    chunks = splitter.split_documents(documents)

    # Har chunk mein source info add karein
    for i, chunk in enumerate(chunks):
        chunk.metadata["chunk_id"] = i

    print(f"Created {len(chunks)} chunks from {len(documents)} documents")
    return chunks

# Test
if __name__ == "__main__":
    from src.document_loader import load_documents
    docs = load_documents("data/sample_docs")
    chunks = chunk_documents(docs)
    print(f"First chunk: {chunks[0].page_content[:100]}...")
