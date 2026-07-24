# Project Notes

## Recruiter Highlights

- Full-stack AI application with real user workflow
- Uses RAG rather than plain prompting
- Includes source-grounded answers
- Uses vector search, BM25 search, and reranking
- Uses environment variables for secret management
- Ready for Streamlit deployment on Hugging Face Spaces

## Technical Decisions

- Streamlit was selected for fast portfolio-ready deployment.
- ChromaDB was selected for simple local persistence.
- Groq was selected for fast Llama 3.1 inference.
- SentenceTransformers models were selected to keep embeddings and reranking free/local.

## Production Improvements

- Replace local ChromaDB with a hosted vector database.
- Add authentication and per-user document collections.
- Add background jobs for large PDF ingestion.
- Add monitoring, tracing, and evaluation metrics.
- Add tests and CI before production rollout.
