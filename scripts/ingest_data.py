"""Data ingestion script to populate ChromaDB with Hadith and Quran data."""

import sys
from pathlib import Path

# Add project root to path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

from src.config import settings
from src.data_ingestion import DataIngestion
from src.embeddings import EmbeddingGenerator
from src.vector_store import VectorStore
from tqdm import tqdm


def main():
    """Main ingestion pipeline."""
    print("=" * 60)
    print("  SEERAH RAG DATA INGESTION PIPELINE")
    print("=" * 60)
    
    try:
        # Step 1: Load data
        print("\n[Step 1/4] Loading data from JSON files...")
        data_ingestion = DataIngestion(settings.data_path)
        documents = data_ingestion.load_all_data()
        
        if not documents:
            print("❌ No documents loaded! Please check your data directory.")
            return
        
        # Step 2: Initialize embedding generator
        print("\n[Step 2/4] Initializing embedding model...")
        embedding_generator = EmbeddingGenerator(settings.embedding_model)
        
        # Step 3: Generate embeddings
        print("\n[Step 3/4] Generating embeddings for all documents...")
        print(f"Processing {len(documents)} documents...")
        
        texts = [doc.page_content for doc in documents]
        embeddings = embedding_generator.embed_documents(texts, batch_size=32)
        
        print(f"✓ Generated {len(embeddings)} embeddings")
        
        # Step 4: Store in ChromaDB
        print("\n[Step 4/4] Storing in ChromaDB...")
        vector_store = VectorStore(
            persist_directory=settings.chroma_path,
            collection_name=settings.chroma_collection_name
        )
        
        # Check if collection already has data
        stats = vector_store.get_collection_stats()
        if stats['total_documents'] > 0:
            print(f"\n⚠️  Warning: Collection already contains {stats['total_documents']} documents!")
            response = input("Do you want to reset and re-ingest? (yes/no): ")
            if response.lower() == 'yes':
                vector_store.reset_collection()
            else:
                print("Ingestion cancelled.")
                return
        
        vector_store.add_documents(documents, embeddings, batch_size=100)
        
        # Final statistics
        final_stats = vector_store.get_collection_stats()
        
        print("\n" + "=" * 60)
        print("  INGESTION COMPLETE!")
        print("=" * 60)
        print(f"\n📊 Final Statistics:")
        print(f"   - Total documents: {final_stats['total_documents']}")
        print(f"   - Collection: {final_stats['collection_name']}")
        print(f"   - Storage: {final_stats['persist_directory']}")
        print(f"\n✅ Your RAG system is ready to use!")
        print(f"\nNext steps:")
        print(f"  1. Start the API server: uv run uvicorn src.api:app --reload")
        print(f"  2. Open frontend in browser")
        print(f"  3. Start asking questions!")
        print()
        
    except Exception as e:
        print(f"\n❌ Error during ingestion: {str(e)}")
        import traceback
        traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    main()
