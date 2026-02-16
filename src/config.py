"""Application configuration using Pydantic settings."""

from pydantic_settings import BaseSettings, SettingsConfigDict
from pathlib import Path


class Settings(BaseSettings):
    """Application settings loaded from environment variables."""
    
    # Groq API Configuration
    groq_api_key: str
    
    # Model Configuration
    embedding_model: str = "sentence-transformers/all-MiniLM-L6-v2"
    llm_model: str = "llama-3.3-70b-versatile"
    llm_temperature: float = 0.1
    
    # ChromaDB Configuration
    chroma_db_path: str = "./chroma_db"
    chroma_collection_name: str = "seerah_collection"
    
    # API Configuration
    api_host: str = "0.0.0.0"
    api_port: int = 8000
    
    # RAG Configuration
    retrieval_top_k: int = 5
    chunk_size: int = 1000
    chunk_overlap: int = 200
    
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False
    )
    
    @property
    def data_path(self) -> Path:
        """Path to data directory."""
        return Path(__file__).parent.parent / "data"
    
    @property
    def chroma_path(self) -> Path:
        """Path to ChromaDB directory."""
        return Path(self.chroma_db_path)


# Global settings instance
settings = Settings()
