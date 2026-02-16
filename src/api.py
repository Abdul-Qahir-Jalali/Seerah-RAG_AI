"""FastAPI backend for RAG-based Q&A system."""

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Optional
import uvicorn

from src.rag_pipeline import RAGPipeline
from src.config import settings


# Initialize FastAPI app
app = FastAPI(
    title="Seerah RAG API",
    description="RAG-based Question Answering for Islamic texts",
    version="1.0.0"
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, specify exact origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize RAG pipeline (lazy loading)
rag_pipeline: Optional[RAGPipeline] = None


def get_rag_pipeline() -> RAGPipeline:
    """Get or create RAG pipeline instance."""
    global rag_pipeline
    if rag_pipeline is None:
        rag_pipeline = RAGPipeline()
    return rag_pipeline


# Pydantic models
class QueryRequest(BaseModel):
    question: str
    top_k: Optional[int] = None


class QueryResponse(BaseModel):
    question: str
    answer: str
    sources: list


class HealthResponse(BaseModel):
    status: str
    total_documents: int
    llm_model: str
    embedding_model: str


# API endpoints
@app.get("/")
async def root():
    """Root endpoint."""
    return {
        "message": "Seerah RAG API",
        "docs": "/docs",
        "health": "/api/health"
    }


@app.get("/api/health", response_model=HealthResponse)
async def health_check():
    """Health check endpoint with system statistics."""
    try:
        pipeline = get_rag_pipeline()
        stats = pipeline.get_stats()
        
        return HealthResponse(
            status="healthy",
            total_documents=stats['vector_store']['total_documents'],
            llm_model=stats['llm_model'],
            embedding_model=stats['embedding_model']
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Health check failed: {str(e)}")


@app.post("/api/query", response_model=QueryResponse)
async def query(request: QueryRequest):
    """Process a question and return answer with sources."""
    try:
        if not request.question or not request.question.strip():
            raise HTTPException(status_code=400, detail="Question cannot be empty")
        
        pipeline = get_rag_pipeline()
        result = pipeline.query(request.question)
        
        return QueryResponse(
            question=result['question'],
            answer=result['answer'],
            sources=result['sources']
        )
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Query processing failed: {str(e)}")


@app.get("/api/stats")
async def get_stats():
    """Get detailed system statistics."""
    try:
        pipeline = get_rag_pipeline()
        return pipeline.get_stats()
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to get stats: {str(e)}")


# Main entry point
if __name__ == "__main__":
    uvicorn.run(
        "src.api:app",
        host=settings.api_host,
        port=settings.api_port,
        reload=True
    )
