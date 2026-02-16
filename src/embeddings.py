"""Embedding generation using Sentence Transformers."""

from sentence_transformers import SentenceTransformer
from typing import List
import numpy as np


class EmbeddingGenerator:
    """Generate embeddings for text using Sentence Transformers."""
    
    def __init__(self, model_name: str = "sentence-transformers/all-MiniLM-L6-v2"):
        """Initialize the embedding model.
        
        Args:
            model_name: Name of the sentence-transformer model
        """
        print(f"Loading embedding model: {model_name}...")
        self.model = SentenceTransformer(model_name)
        print("✓ Embedding model loaded successfully")
    
    def embed_documents(self, texts: List[str], batch_size: int = 32) -> List[List[float]]:
        """Generate embeddings for a list of documents.
        
        Args:
            texts: List of text strings to embed
            batch_size: Batch size for processing
            
        Returns:
            List of embedding vectors
        """
        embeddings = self.model.encode(
            texts,
            batch_size=batch_size,
            show_progress_bar=True,
            normalize_embeddings=True,  # Normalize for better similarity search
            convert_to_numpy=True
        )
        
        # Convert to list of lists for ChromaDB compatibility
        return embeddings.tolist()
    
    def embed_query(self, text: str) -> List[float]:
        """Generate embedding for a single query.
        
        Args:
            text: Query text to embed
            
        Returns:
            Embedding vector
        """
        embedding = self.model.encode(
            text,
            normalize_embeddings=True,
            convert_to_numpy=True
        )
        return embedding.tolist()
    
    @property
    def dimension(self) -> int:
        """Get the dimension of the embedding vectors."""
        return self.model.get_sentence_embedding_dimension()
