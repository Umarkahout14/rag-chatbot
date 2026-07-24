# Contributing

Thanks for your interest in improving this project.

## Development Setup

```bash
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
streamlit run app.py
```

## Guidelines

- Keep API keys out of source code.
- Keep changes focused and easy to review.
- Prefer readable code over clever abstractions.
- Update documentation when behavior changes.
- Test document upload and chat before submitting changes.

## Suggested Checks

```bash
python -m compileall app.py src
pip check
```
