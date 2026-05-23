# Local RAG Assistant

A Retrieval-Augmented Generation (RAG) assistant built with:

- FastAPI
- PostgreSQL + pgvector
- Sentence Transformers
- Google Gemini
- Semantic Search

## Features

- PDF document ingestion
- Recursive chunking
- Embedding generation
- Vector similarity search
- Context-aware question answering

## Architecture

User Query


↓


Embedding Model


↓


PostgreSQL + pgvector


↓


Top-K Retrieval


↓


Gemini LLM


↓


Answer Generation

## Run

1. pip install -r requirements.txt
2. python -m scripts.ingest_pdf data/sample.pdf
3. uvicorn app.api:app --reload
