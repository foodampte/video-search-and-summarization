# Video Search and Summarization

A fork of [NVIDIA-AI-Blueprints/video-search-and-summarization](https://github.com/NVIDIA-AI-Blueprints/video-search-and-summarization) — an AI-powered pipeline for searching, indexing, and summarizing video content using NVIDIA's AI stack.

## Overview

This blueprint enables users to:
- **Ingest** video files and extract multimodal embeddings (visual + audio + text)
- **Search** across a video library using natural language queries
- **Summarize** video content using large language models
- **Retrieve** relevant video segments with timestamps

## Architecture

```
┌─────────────────────────────────────────────────────┐
│                   Frontend (UI)                     │
└───────────────────────┬─────────────────────────────┘
                        │
┌───────────────────────▼─────────────────────────────┐
│               API Gateway / Backend                 │
└──────┬──────────────────────────┬───────────────────┘
       │                          │
┌──────▼──────┐          ┌────────▼────────┐
│  Ingestion  │          │  Search & Query │
│  Pipeline   │          │  Service        │
└──────┬──────┘          └────────┬────────┘
       │                          │
┌──────▼──────────────────────────▼────────┐
│         Vector Database (Milvus)         │
└──────────────────────────────────────────┘
```

## Prerequisites

- Docker & Docker Compose
- NVIDIA GPU with CUDA 12.x support
- NVIDIA Container Toolkit
- Python 3.10+
- NVIDIA API Key (for NIM microservices)

## Quick Start

### 1. Clone the repository

```bash
git clone https://github.com/your-org/video-search-and-summarization.git
cd video-search-and-summarization
```

### 2. Configure environment variables

```bash
cp .env.example .env
# Edit .env with your NVIDIA API key and other settings
```

### 3. Launch with Docker Compose

```bash
docker compose up --build
```

### 4. Access the application

- **UI**: http://localhost:3000
- **API**: http://localhost:8000
- **API Docs**: http://localhost:8000/docs

## Configuration

Key environment variables:

| Variable | Description | Default |
|---|---|---|
| `NVIDIA_API_KEY` | NVIDIA NIM API key | required |
| `MILVUS_HOST` | Milvus vector DB host | `localhost` |
| `MILVUS_PORT` | Milvus vector DB port | `19530` |
| `VIDEO_STORAGE_PATH` | Path to store uploaded videos | `./data/videos` |
| `LLM_MODEL` | LLM model for summarization | `meta/llama-3.1-8b-instruct` |
| `EMBEDDING_MODEL` | Embedding model for search | `nvidia/nv-embedqa-e5-v5` |

> **Personal note:** I changed the default `LLM_MODEL` from `llama-3.1-70b-instruct` to `llama-3.1-8b-instruct` to reduce API costs while experimenting locally. Switch back to the 70b variant for better summarization quality.

## Development

### Setting up a local dev environment

```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
```

### Running tests

```bash
pytest tests/ -v
```

## Troubleshooting

### Common issues

- **GPU not detected**: Make sure the NVIDIA Container Toolkit is installed and `docker info | grep -i runtime` shows `nvidia` as an available runtime.
- **Milvus connection refused**: The vector DB can take 20–30 seconds to become ready on first launch. Wait for the health check to pass before ingesting videos.
- **API key errors**: Ensure `NVIDIA_API_KEY` is set in your `.env` file and has access to the required NIM endpoints.
