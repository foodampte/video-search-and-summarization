#!/usr/bin/env python3
"""
Video Search and Summarization - Main Entry Point

This module serves as the primary entry point for the video search and
summarization application, initializing all required services and
starting the FastAPI web server.
"""

import logging
import os
import sys
from contextlib import asynccontextmanager

import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    handlers=[
        logging.StreamHandler(sys.stdout),
    ],
)
logger = logging.getLogger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Manage application startup and shutdown lifecycle."""
    logger.info("Starting Video Search and Summarization service...")

    # Initialize vector store connection
    logger.info("Connecting to vector store...")
    # TODO: Initialize Milvus/vector DB client here

    # Initialize NIM clients
    logger.info("Initializing NVIDIA NIM clients...")
    # TODO: Set up embedding and VLM NIM clients

    logger.info("Service startup complete.")
    yield

    # Cleanup on shutdown
    logger.info("Shutting down Video Search and Summarization service...")


def create_app() -> FastAPI:
    """Create and configure the FastAPI application instance."""
    app = FastAPI(
        title="Video Search and Summarization",
        description=(
            "AI-powered video search and summarization service using "
            "NVIDIA NIM microservices for multimodal understanding."
        ),
        version="1.0.0",
        lifespan=lifespan,
    )

    # Configure CORS
    # Note: Defaulting to localhost:3000 instead of wildcard "*" for safer local dev
    allowed_origins = os.getenv("ALLOWED_ORIGINS", "http://localhost:3000").split(",")
    app.add_middleware(
        CORSMiddleware,
        allow_origins=allowed_origins,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    # Register API routers
    # from src.routers import videos, search, summarization
    # app.include_router(videos.router, prefix="/api/v1/videos", tags=["videos"])
    # app.include_router(search.router, prefix="/api/v1/search", tags=["search"])
    # app.include_router(summarization.router, prefix="/api/v1/summarize", tags=["summarization"])

    @app.get("/health", tags=["health"])
    async def health_check():
        """Health check endpoint for container orchestration."""
        return {"status": "healthy", "service": "video-search-and-summarization"}

    return app


app = create_app()


if __name__ == "__main__":
    host = os.getenv("APP_HOST", "0.0.0.0")
    port = int(os.getenv("APP_PORT", "8000"))
    reload = os.getenv("APP_RELOAD", "false").lower() == "true"
    workers = int(os.getenv("APP_WORKERS", "1"))

    logger.info("Starting server on %s:%d", host, port)
    uvicorn.run(
        "src.main:app",
        host=host,
        port=port,
        reload=reload,
        workers=workers if not reload else 1,
    )
