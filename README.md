# AI Research Assistant - Advanced RAG Chatbot

[![Python](https://img.shields.io/badge/Python-3.10+-3776AB?logo=python&logoColor=white)](https://www.python.org/)
[![Streamlit](https://img.shields.io/badge/Streamlit-1.40-FF4B4B?logo=streamlit&logoColor=white)](https://streamlit.io/)
[![LangChain](https://img.shields.io/badge/LangChain-0.3-1C3C3C)](https://www.langchain.com/)
[![ChromaDB](https://img.shields.io/badge/ChromaDB-Vector%20Store-5B5FC7)](https://www.trychroma.com/)
[![Groq](https://img.shields.io/badge/Groq-Llama%203.1-F55036)](https://groq.com/)
[![License](https://img.shields.io/badge/License-Apache--2.0-blue.svg)](LICENSE)

A production-style document question-answering assistant built with Retrieval-Augmented Generation (RAG). The app lets users upload PDFs or text files, indexes them into a local vector database, retrieves relevant evidence with hybrid search, reranks results, and generates grounded answers with source citations.

> Built by Umar Asghar as a portfolio-grade AI engineering project.

## Live Links

- GitHub: https://github.com/Umarkahout14/rag-chatbot
- Live Demo: https://huggingface.co/spaces/YOUR_HF_USERNAME/rag-chatbot

Replace the Hugging Face URL after deployment.

## What This Project Demonstrates

- End-to-end RAG architecture from document ingestion to cited answer generation
- PDF/TXT loading, chunking, embedding, vector storage, retrieval, reranking, and LLM response generation
- Hybrid retrieval using dense vector search plus BM25 keyword search
- Cross-encoder reranking for improved relevance of retrieved context
- Conversation memory for multi-turn user interaction
- Secure deployment pattern using environment variables for API keys
- Professional Streamlit UI with upload workflow, chat interface, and source previews

## Feature Overview

| Area | Implementation |
|---|---|
| Frontend | Streamlit professional dark UI |
| LLM | Groq API with Llama 3.1 8B Instant |
| Embeddings | sentence-transformers/all-MiniLM-L6-v2 |
| Vector Store | ChromaDB persistent local database |
| Retrieval | Hybrid search: BM25 + vector similarity |
| Reranking | Cross-encoder MS MARCO reranker |
| Documents | PDF and TXT ingestion |
| Memory | Session-based conversation memory |
| Citations | Source number, file path, page, and preview |
| Deployment | Hugging Face Spaces ready |

## Architecture

```mermaid
flowchart LR
    A["User uploads PDF/TXT"] --> B["Document Loader"]
    B --> C["Text Chunker"]
    C --> D["Embedding Model"]
    D --> E["ChromaDB Vector Store"]
    E --> F["Hybrid Retriever"]
    C --> G["BM25 Index"]
    G --> F
    F --> H["Cross-Encoder Reranker"]
    H --> I["Context Formatter"]
    I --> J["Groq Llama 3.1"]
    J --> K["Cited Answer in Streamlit"]
```

## Repository Structure

```text
rag-chatbot/
â”œâ”€â”€ app.py                    # Streamlit UI and chat workflow
â”œâ”€â”€ requirements.txt          # Python dependencies
â”œâ”€â”€ README.md                 # Project overview and setup
â”œâ”€â”€ DEPLOYMENT.md             # Hugging Face deployment guide
â”œâ”€â”€ .env.example              # Environment variable template
â”œâ”€â”€ LICENSE                   # Apache-2.0 license
â”œâ”€â”€ data/
â”‚   â””â”€â”€ sample_docs/          # Optional sample PDFs/TXT files
â””â”€â”€ src/
    â”œâ”€â”€ config.py             # App settings and environment variables
    â”œâ”€â”€ document_loader.py    # PDF/TXT loading
    â”œâ”€â”€ chunker.py            # Text chunking
    â”œâ”€â”€ embeddings.py         # Hugging Face embeddings
    â”œâ”€â”€ vector_store.py       # ChromaDB create/load helpers
    â”œâ”€â”€ retriever.py          # Hybrid BM25 + vector retriever
    â”œâ”€â”€ reranker.py           # Cross-encoder reranking
    â”œâ”€â”€ llm_client.py         # Groq LLM client
    â”œâ”€â”€ rag_chain.py          # RAG orchestration
    â””â”€â”€ memory.py             # Conversation memory
```

## Quick Start

### 1. Clone the repository

```bash
git clone https://github.com/Umarkahout14/rag-chatbot.git
cd rag-chatbot
```

### 2. Create a virtual environment

```bash
python -m venv venv
```

Windows:

```bash
venv\Scripts\activate
```

macOS/Linux:

```bash
source venv/bin/activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Configure environment variables

Create a `.env` file or set the variable in your terminal:

```bash
GROQ_API_KEY=your_groq_api_key_here
```

Windows CMD:

```cmd
set GROQ_API_KEY=your_groq_api_key_here
```

PowerShell:

```powershell
$env:GROQ_API_KEY="your_groq_api_key_here"
```

### 5. Run the app

```bash
streamlit run app.py
```

Then open:

```text
http://localhost:8501
```

## How To Use

1. Start the Streamlit app.
2. Upload one or more PDF/TXT files from the sidebar.
3. Ask a question about the uploaded documents.
4. Review the answer and open the source panel to inspect supporting chunks.
5. Ask follow-up questions to test conversation memory.

## Environment Variables

| Variable | Required | Description |
|---|---:|---|
| `GROQ_API_KEY` | Yes | Groq API key used for Llama 3.1 responses |
| `HF_HOME` | No | Optional Hugging Face cache directory |
| `SENTENCE_TRANSFORMERS_HOME` | No | Optional sentence-transformers cache directory |
| `TRANSFORMERS_CACHE` | No | Optional transformers cache directory |

## Deployment Notes

This project is designed for Hugging Face Spaces with the Streamlit SDK.

Before deploying:

- Do not commit `.env` files or API keys.
- Add `GROQ_API_KEY` as a Hugging Face Repository Secret.
- Keep local vector DB/cache folders ignored.
- Use CPU Basic hardware for the free tier.

Full steps are in [DEPLOYMENT.md](DEPLOYMENT.md).

## Security

The Groq API key is read from an environment variable:

```python
GROQ_API_KEY = os.getenv("GROQ_API_KEY", "")
```

No API key should be committed to GitHub. If a key is accidentally exposed, revoke it immediately and create a new one.

## Known Limitations

- First model load can take time because embedding and reranker models are downloaded from Hugging Face.
- Free CPU deployment can be slower for reranking and embeddings.
- ChromaDB is local/persistent, not a managed production database.
- The app is optimized for demos and portfolio evaluation, not high-traffic multi-user production.

## Roadmap

- Add evaluation dashboard for faithfulness and answer relevance
- Add upload history and document management
- Add streaming responses
- Add Docker support
- Add unit tests for ingestion and retrieval modules
- Add CI workflow for linting and import checks

## Portfolio Summary

This project shows practical AI engineering ability across LLM integration, retrieval systems, vector databases, document processing, deployment hygiene, and UI polish. It is suitable for roles involving applied AI, GenAI engineering, ML tooling, and full-stack AI product development.

## License

Licensed under the Apache License 2.0. See [LICENSE](LICENSE).
