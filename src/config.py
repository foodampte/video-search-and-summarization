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

    frame_interval_seconds: float = field(
        default_factory=lambda: float(os.getenv("FRAME_INTERVAL_SECONDS", "2.0"))
    )
    max_frames_per_video: int = field(
        default_factory=lambda: int(os.getenv("MAX_FRAMES_PER_VIDEO", "500"))
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
        default_factory=lambda: int(os.getenv("APP_PORT", "8000"))
    )
    debug: bool = field(
        default_factory=lambda: os.getenv("APP_DEBUG", "false").lower() == "true"
    )
    log_level: str = field(
        default_factory=lambda: os.getenv("LOG_LEVEL", "INFO").upper()
    )
    nim: NIMConfig = field(default_factory=NIMConfig)
    vector_store: VectorStoreConfig = field(default_factory=VectorStoreConfig)
    video_processing: VideoProcessingConfig = field(default_factory=VideoProcessingConfig)

    def validate(self) -> None:
        """Validate critical configuration values and raise if misconfigured."""
        if not self.nim.api_key:
            raise EnvironmentError(
                "NVIDIA_API_KEY environment variable is not set. "
                "Obtain an API key from https://build.nvidia.com."
            )
        os.makedirs(self.video_processing.upload_dir, exist_ok=True)
        os.makedirs(self.video_processing.frames_dir, exist_ok=True)


# Module-level singleton — import this throughout the application.
config = AppConfig()
