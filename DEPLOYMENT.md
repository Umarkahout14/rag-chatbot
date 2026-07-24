# Deployment Guide

This guide explains how to deploy the AI Research Assistant to Hugging Face Spaces.

## 1. Push To GitHub

From the project root:

```bash
git add .
git commit -m "Add recruiter documentation"
git push origin main
```

Repository:

```text
https://github.com/Umarkahout14/rag-chatbot
```

## 2. Create Hugging Face Space

Go to:

```text
https://huggingface.co/spaces
```

Create a new Space with:

| Setting | Value |
|---|---|
| Space name | `rag-chatbot` |
| SDK | Streamlit |
| Hardware | CPU Basic |
| Visibility | Public |
| License | Apache-2.0 |

## 3. Add Secret

Open the Space settings and add:

| Secret name | Value |
|---|---|
| `GROQ_API_KEY` | Your Groq API key |

Do not paste API keys into source code.

## 4. Connect GitHub Repository

In the Hugging Face Space settings, link:

```text
Umarkahout14/rag-chatbot
```

Hugging Face will rebuild automatically when GitHub receives new commits.

## 5. Verify

After deployment, check:

- Build logs
- Container logs
- App loads successfully
- Upload works
- Chat returns source citations

Expected live URL format:

```text
https://huggingface.co/spaces/YOUR_HF_USERNAME/rag-chatbot
```

## Troubleshooting

| Problem | Fix |
|---|---|
| `GROQ_API_KEY missing` | Add the Hugging Face secret |
| Module import error | Check `requirements.txt` |
| Hugging Face model download timeout | Restart the Space build |
| App slow on first run | Wait for model downloads/cache |
| No documents found | Upload documents from the sidebar |
