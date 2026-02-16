"""Groq LLM integration using LangChain."""

from langchain_groq import ChatGroq
from langchain_core.prompts import ChatPromptTemplate
from src.config import settings


class GroqLLM:
    """Groq LLM wrapper for generating answers."""
    
    def __init__(self):
        """Initialize Groq LLM with configuration."""
        self.llm = ChatGroq(
            groq_api_key=settings.groq_api_key,
            model_name=settings.llm_model,
            temperature=settings.llm_temperature,
            max_tokens=2000
        )
        
        # Create prompt template for RAG
        self.prompt_template = ChatPromptTemplate.from_messages([
            ("system", """You are an expert Islamic scholar assistant specializing in Seerah (Prophet's biography), Hadith, and Quran.

Your task is to answer questions accurately based ONLY on the provided context from authentic Islamic sources.

CRITICAL RULES:
1. ONLY use information from the provided context
2. If the context doesn't contain the answer, say: "I cannot find this information in the available sources. Please ask another question or rephrase your query."
3. NEVER make up information or use external knowledge
4. ALWAYS cite your sources by mentioning the book/surah name
5. Provide Arabic text when available
6. Be respectful and scholarly in tone

Context from Islamic sources:
{context}

Remember: Accuracy is paramount. If unsure, admit you don't have the information rather than guessing."""),
            ("human", "{question}")
        ])
        
        print(f"✓ Groq LLM initialized with model: {settings.llm_model}")
    
    def generate_answer(self, question: str, context: str) -> str:
        """Generate an answer based on the question and retrieved context.
        
        Args:
            question: User's question
            context: Retrieved context from vector store
            
        Returns:
            Generated answer
        """
        # Create the prompt
        messages = self.prompt_template.format_messages(
            context=context,
            question=question
        )
        
        # Generate response
        response = self.llm.invoke(messages)
        
        return response.content
    
    def generate_answer_stream(self, question: str, context: str):
        """Generate an answer with streaming support.
        
        Args:
            question: User's question
            context: Retrieved context from vector store
            
        Yields:
            Chunks of the generated answer
        """
        # Create the prompt
        messages = self.prompt_template.format_messages(
            context=context,
            question=question
        )
        
        # Stream response
        for chunk in self.llm.stream(messages):
            if chunk.content:
                yield chunk.content
