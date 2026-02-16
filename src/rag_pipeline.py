"""Complete RAG pipeline orchestration."""

from typing import List, Dict, Any
from src.embeddings import EmbeddingGenerator
from src.vector_store import VectorStore
from src.llm import GroqLLM
from src.config import settings


class RAGPipeline:
    """End-to-end RAG pipeline for question answering."""
    
    def __init__(self):
        """Initialize RAG pipeline components."""
        print("\n🚀 Initializing RAG Pipeline...\n")
        
        # Initialize components
        self.embedding_generator = EmbeddingGenerator(settings.embedding_model)
        self.vector_store = VectorStore(
            persist_directory=settings.chroma_path,
            collection_name=settings.chroma_collection_name
        )
        self.llm = GroqLLM()
        
        print("\n✅ RAG Pipeline ready!\n")
    
    def retrieve_context(self, question: str, top_k: int = None) -> tuple[str, List[Dict[str, Any]]]:
        """Retrieve relevant context for a question.
        
        Args:
            question: User's question
            top_k: Number of documents to retrieve (uses config default if None)
            
        Returns:
            Tuple of (formatted_context_string, list_of_source_documents)
        """
        if top_k is None:
            top_k = settings.retrieval_top_k
        
        # Generate query embedding
        query_embedding = self.embedding_generator.embed_query(question)
        
        # Retrieve similar documents
        results = self.vector_store.similarity_search(
            query_embedding=query_embedding,
            top_k=top_k
        )
        
        # Format context for LLM
        context_parts = []
        sources = []
        
        for i, result in enumerate(results, 1):
            content = result['content']
            metadata = result['metadata']
            
            # Format based on source type
            if metadata.get('source_type') == 'hadith':
                source_info = f"[Hadith - {metadata.get('collection', 'Unknown')}]"
                context_parts.append(f"{source_info}\n{content}")
            elif metadata.get('source_type') == 'quran':
                source_info = f"[Quran - {metadata.get('reference', 'Unknown')}]"
                context_parts.append(f"{source_info}\n{content}")
            else:
                context_parts.append(content)
            
            # Store source for citation
            sources.append({
                'content': content,
                'metadata': metadata
            })
        
        # Combine all context
        context_string = "\n\n---\n\n".join(context_parts)
        
        return context_string, sources
    
    def query(self, question: str) -> Dict[str, Any]:
        """Process a question and return answer with sources.
        
        Args:
            question: User's question
            
        Returns:
            Dictionary with answer and sources
        """
        # Retrieve context
        context, sources = self.retrieve_context(question)
        
        # Generate answer
        answer = self.llm.generate_answer(question, context)
        
        return {
            'question': question,
            'answer': answer,
            'sources': sources
        }
    
    def query_stream(self, question: str):
        """Process a question and stream the answer.
        
        Args:
            question: User's question
            
        Yields:
            Dictionary chunks with answer_chunk and sources (sent once at start)
        """
        # Retrieve context
        context, sources = self.retrieve_context(question)
        
        # Send sources first
        yield {
            'type': 'sources',
            'sources': sources
        }
        
        # Stream answer
        for chunk in self.llm.generate_answer_stream(question, context):
            yield {
                'type': 'answer_chunk',
                'chunk': chunk
            }
    
    def get_stats(self) -> Dict[str, Any]:
        """Get pipeline statistics.
        
        Returns:
            Dictionary with statistics
        """
        vector_stats = self.vector_store.get_collection_stats()
        
        return {
            'vector_store': vector_stats,
            'embedding_dimension': self.embedding_generator.dimension,
            'llm_model': settings.llm_model,
            'embedding_model': settings.embedding_model
        }
