"""Configuration management for the video search and summarization service.

Loads settings from environment variables with sensible defaults.
"""

import os
from dataclasses import dataclass, field
from typing import Optional


@dataclass
class NIMConfig:
    """Configuration for NVIDIA Inference Microservices (NIM) endpoints."""

    vlm_model: str = field(
        default_factory=lambda: os.getenv("VLM_MODEL", "nvidia/llava-v1.6-mistral-7b")
    )
    vlm_endpoint: str = field(
        default_factory=lambda: os.getenv("VLM_ENDPOINT", "https://ai.api.nvidia.com/v1")
    )
    embedding_model: str = field(
        default_factory=lambda: os.getenv(
            "EMBEDDING_MODEL", "nvidia/nv-embedqa-e5-v5"
        )
    )
    embedding_endpoint: str = field(
        default_factory=lambda: os.getenv(
            "EMBEDDING_ENDPOINT", "https://ai.api.nvidia.com/v1"
        )
    )
    reranker_model: str = field(
        default_factory=lambda: os.getenv(
            "RERANKER_MODEL", "nvidia/nv-rerankqa-mistral-4b-v3"
        )
    )
    reranker_endpoint: str = field(
        default_factory=lambda: os.getenv(
            "RERANKER_ENDPOINT", "https://ai.api.nvidia.com/v1"
        )
    )
    api_key: Optional[str] = field(
        default_factory=lambda: os.getenv("NVIDIA_API_KEY")
    )


@dataclass
class VectorStoreConfig:
    """Configuration for the Milvus vector store."""

    host: str = field(
        default_factory=lambda: os.getenv("MILVUS_HOST", "milvus-standalone")
    )
    port: int = field(
        default_factory=lambda: int(os.getenv("MILVUS_PORT", "19530"))
    )
    collection_name: str = field(
        default_factory=lambda: os.getenv("MILVUS_COLLECTION", "video_embeddings")
    )
    dim: int = field(
        default_factory=lambda: int(os.getenv("EMBEDDING_DIM", "1024"))
    )


@dataclass
class VideoProcessingConfig:
    """Configuration for video ingestion and frame extraction."""

    # Increased from 2.0 to 5.0 seconds — I mostly work with longer videos
    # where dense frame sampling isn't necessary and just slows things down.
    frame_interval_seconds: float = field(
        default_factory=lambda: float(os.getenv("FRAME_INTERVAL_SECONDS", "5.0"))
    )
    # Bumped up from 500 to 1000 to handle feature-length films without hitting
    # the cap mid-video.
    max_frames_per_video: int = field(
        default_factory=lambda: int(os.getenv("MAX_FRAMES_PER_VIDEO", "1000"))
    )
    thumbnail_width: int = field(
        default_factory=lambda: int(os.getenv("THUMBNAIL_WIDTH", "320"))
    )
    thumbnail_height: int = field(
        default_factory=lambda: int(os.getenv("THUMBNAIL_HEIGHT", "180"))
    )
    upload_dir: str = field(
        default_factory=lambda: os.getenv("UPLOAD_DIR", "/tmp/video_uploads")
    )
    frames_dir: str = field(
        default_factory=lambda: os.getenv("FRAMES_DIR", "/tmp/video_frames")
    )


@dataclass
class AppConfig:
    """Top-level application configuration."""

    host: str = field(
        default_factory=lambda: os.getenv("APP_HOST", "0.0.0.0")
    )
    port: int = field(
