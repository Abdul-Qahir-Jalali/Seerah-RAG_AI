"""Vector store management using ChromaDB."""

import chromadb
from chromadb.config import Settings as ChromaSettings
from pathlib import Path
from typing import List, Dict, Any, Optional
from src.data_ingestion import Document


class VectorStore:
    """Manage ChromaDB vector database for document storage and retrieval."""
    
    def __init__(self, persist_directory: Path, collection_name: str = "seerah_collection"):
        """Initialize ChromaDB client and collection.
        
        Args:
            persist_directory: Directory to persist ChromaDB data
            collection_name: Name of the collection
        """
        self.persist_directory = persist_directory
        self.collection_name = collection_name
        
        # Create directory if it doesn't exist
        persist_directory.mkdir(parents=True, exist_ok=True)
        
        # Initialize ChromaDB client with persistence
        self.client = chromadb.PersistentClient(
            path=str(persist_directory),
            settings=ChromaSettings(
                anonymized_telemetry=False,
                allow_reset=True
            )
        )
        
        # Get or create collection
        self.collection = self.client.get_or_create_collection(
            name=collection_name,
            metadata={"hnsw:space": "cosine"}  # Use cosine similarity
        )
        
        print(f"✓ ChromaDB initialized at {persist_directory}")
        print(f"✓ Collection '{collection_name}' ready")
    
    def add_documents(
        self,
        documents: List[Document],
        embeddings: List[List[float]],
        batch_size: int = 100
    ) -> None:
        """Add documents to the vector store.
        
        Args:
            documents: List of Document objects
            embeddings: List of embedding vectors
            batch_size: Batch size for adding documents
        """
        total_docs = len(documents)
        print(f"\n📥 Adding {total_docs} documents to ChromaDB...")
        
        # Process in batches
        for i in range(0, total_docs, batch_size):
            batch_docs = documents[i:i + batch_size]
            batch_embeddings = embeddings[i:i + batch_size]
            
            # Prepare data for ChromaDB
            ids = [f"doc_{i + j}" for j in range(len(batch_docs))]
            texts = [doc.page_content for doc in batch_docs]
            metadatas = [doc.metadata for doc in batch_docs]
            
            # Add to collection
            self.collection.add(
                ids=ids,
                documents=texts,
                embeddings=batch_embeddings,
                metadatas=metadatas
            )
            
            if (i + batch_size) % 500 == 0:
                print(f"  Added {min(i + batch_size, total_docs)}/{total_docs} documents...")
        
        print(f"✅ All {total_docs} documents added successfully!")
    
    def similarity_search(
        self,
        query_embedding: List[float],
        top_k: int = 5,
        filter_dict: Optional[Dict[str, Any]] = None
    ) -> List[Dict[str, Any]]:
        """Search for similar documents using vector similarity.
        
        Args:
            query_embedding: Query embedding vector
            top_k: Number of results to return
            filter_dict: Optional metadata filter
            
        Returns:
            List of search results with content and metadata
        """
        results = self.collection.query(
            query_embeddings=[query_embedding],
            n_results=top_k,
            where=filter_dict if filter_dict else None
        )
        
        # Format results
        formatted_results = []
        if results['documents'] and results['documents'][0]:
            for i in range(len(results['documents'][0])):
                formatted_results.append({
                    'content': results['documents'][0][i],
                    'metadata': results['metadatas'][0][i],
                    'distance': results['distances'][0][i] if 'distances' in results else None
                })
        
        return formatted_results
    
    def get_collection_stats(self) -> Dict[str, Any]:
        """Get statistics about the collection.
        
        Returns:
            Dictionary with collection statistics
        """
        count = self.collection.count()
        
        return {
            'total_documents': count,
            'collection_name': self.collection_name,
            'persist_directory': str(self.persist_directory)
        }
    
    def reset_collection(self) -> None:
        """Delete and recreate the collection (use with caution!)."""
        self.client.delete_collection(self.collection_name)
        self.collection = self.client.get_or_create_collection(
            name=self.collection_name,
            metadata={"hnsw:space": "cosine"}
        )
        print(f"✓ Collection '{self.collection_name}' reset")
